import os
from flask_bootstrap import Bootstrap
from ip6Regex import ip6Regex
from os.path import join, dirname, realpath
from getStatusCode import getStatusCode
from allowedFile import allowedFileExtension, allowedFileType
from geolite2 import geolite2
import json
import requests
import itertools
import re
import os
import time
# for file upload module
import os
import json as simplejson
import asyncio

from flask import (
    Flask,
    flash,
    request,
    render_template,
    redirect,
    url_for,
    send_from_directory,
)
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config["UPLOAD_DIR"] = "/upload_service/app/static/data/"
app.config["ASSET_DIR"] = "static/mapAssets/"
app.config["CLEAN_DIR"] = "/upload_service/app/static/cleanData/"
app.config["HTML_DIR"] = "static/"

# app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

IGNORED_FILES = set([".gitignore"])

bootstrap = Bootstrap(app)


# serve static files
@app.route("/data/<string:filename>", methods=["GET"])
def get_file(filename):
    return send_from_directory(
        os.path.join(app.config["UPLOAD_DIR"]), filename=filename
    )


# once files are uploaded, requests can be made to /map to generate maps
@app.route("/map", methods=["GET"])
def logViz():
    class LogViz(object):
        # Class for analysing logs and generating interactive map
        def __init__(
            self,
            logfile,
            loglist,
            clean_dir=app.config["CLEAN_DIR"],
            raw_dir=app.config["UPLOAD_DIR"],
            asset_dir=app.config["ASSET_DIR"],
            html_dir=app.config["HTML_DIR"],
        ):
            super(LogViz, self).__init__()

            # dir with data, rw
            self.clean_dir = clean_dir

            # dir for src data
            self.raw_dir = raw_dir

            # dir with html, rw
            self.html_dir = html_dir
            self.html_file = html_dir + "map.html"

            # "location.js" loaded into the map in /static/index.html
            self.asset_dir = asset_dir

            # path to access.log
            self.access_file = raw_dir + logfile

            # json for each log file with geolocation, os, status code
            self.analysis = self.clean_dir + logfile + "-" + "analysis.json"

            # contains general information and rasterised location data
            self.responseJson = self.clean_dir + logfile + "-" + "locations.json"

            # js file that loads the information and raster data from logs into map
            self.locationsJS = self.asset_dir + "locations.js"

            # list of all log files, containing the log name
            self.loglist = self.asset_dir + "loglist.js"

            # object with IPtotalIPCount number of IPs, also
            # sets the circumference of the data points on the map
            # based on the total # of ips. When there are many ips to render
            # on the Map the data points will have a smaller circumference
            self.information = {"totalIPCount": 0}

        def getIP(self, line):
            # ips in access.log should be in the first part of the line
            checkIp = line.split(" ")[0]
            # ip regex
            rgx = re.compile("(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
            matchIp = rgx.search(checkIp)

            if matchIp is None:
                # if that match failed check the entire line for an IP match
                secondMatchIp = rgx.search(line)
                # if that match also failed, try ipv6
                if secondMatchIp is None:
                    matchIp6 = ip6Regex.search(line)
                    # print('ipv6 IP ', line)
            # make sure we have an ip
            if matchIp or secondMatchIp or matchIp6:
                # return the log line now an IP has been detected
                return checkIp
            else:
                # TODO, handle this case instead of just printing the result
                print("Could not find an IP in this line")

        def removeDuplicates(self):
            # Scans the log file for visits by the same ip and removes them.
            with open(self.access_file, "r") as f:
                # storing all already added IPs
                addedIPs = []
                # creating file that just stores the ips
                self.ip_file = self.clean_dir + "ip.txt"
                # file that stores the log lines without duplicate ips
                self.unique_data_file = self.clean_dir + "noDuplicatesLog.txt"
                with open(self.ip_file, "w") as dump:
                    with open(self.unique_data_file, "w") as clean:

                        # save IP unless its a duplicate found in the last 1000 IPs
                        for line in f:
                            IP = self.getIP(line)
                            if (
                                IP not in addedIPs[max(-len(addedIPs), -1000) :]
                                and IP is not None
                            ):
                                addedIPs.append(IP)
                                clean.write(line)
                            else:
                                pass

                    dump.write("\n".join(addedIPs))
            print("Removed Duplicates.")

        # isolate OS data from a log line
        def getContext(self, line):
            return line.rsplit('"')[5]

        # Gets the OS from a log file entry
        def getOS(self, line):
            context = self.getContext(line).rsplit("(")[1]
            rawOS = context.rsplit(";")[1].lower()
            if "win" in rawOS:
                return "Windows"
            elif "android" in rawOS:
                return "Android"
            elif "mac" in rawOS:
                if "ipad" or "iphone" in context:
                    return "iOS"
                else:
                    return "Mac"
            elif "linux" or "ubuntu" in rawOS:
                return "Linux"
            else:
                return "Other"
                # return rawOS

        def getIPData(self):
            # Removes duplicates and create file w. ip, OS and status code
            self.removeDuplicates()
            with open(self.unique_data_file, "r") as data_file:
                with open(self.analysis, "w") as json_file:
                    result = []
                    for line in data_file:
                        try:
                            entry = {}
                            entry["ip"] = self.getIP(line)
                            entry["OS"] = self.getOS(line)
                            entry["status"] = getStatusCode(line)
                            entry["fullLine"] = str(line)
                            result.append(entry)
                            self.information["totalIPCount"] += 1

                        except Exception as e:
                            pass

                    json.dump(result, json_file)
            print("Cleaned Data.")

        async def getIPLocation(self):
            # Scan ips for geolocation, add coordinates
            self.getIPData()
            with open(self.analysis, "r") as json_file:
                data = json.load(json_file)
                reader = geolite2.reader()
                result = []
                for item in data:
                    ip = item["ip"]
                    ip_info = reader.get(ip)

                    if ip_info is not None:
                        try:
                            item["latitude"] = ip_info["location"]["latitude"]
                            item["longitude"] = ip_info["location"]["longitude"]
                            result.append(item)
                        except Exception as e:
                            pass

            with open(self.analysis, "w") as json_file:
                json.dump(result, json_file)

            print("Added locations")

        async def analyseLog(self, loglist, index, logCount, allLogs):
            tasks = []
            tasks.append(asyncio.ensure_future(self.getIPLocation()))
            tasks.append(asyncio.ensure_future(self.rasterizeData()))
            tasks.append(
                asyncio.ensure_future(self.createJs(loglist, index, logCount, allLogs))
            )
            await asyncio.gather(*tasks, return_exceptions=True)
            print("Rasterised Data")

        async def rasterizeData(self, resLat=200, resLong=250):

            # Split map into resLat*resLong chunks
            # count visits to each, return "raster"
            # list with geolocation(x,y)/status/ip/os/full log line

            latStep, longStep = 180 / resLat, 360 / resLong
            # Build the rasterised coord. system
            gridX, gridY = [], []
            x = -180
            y = -90

            for i in range(resLong):
                gridX.append(x)
                x += longStep
            gridX.reverse()

            for i in range(resLat):
                gridY.append(y + i * latStep)
            gridY.reverse()

            gridItems = itertools.product(gridX, gridY)
            grid = {i: 0 for i in gridItems}

            # assign each data point to its grid square
            with open(self.analysis, "r") as json_file:
                data = json.load(json_file)
                print("assigning data point to its grid square")
                for point in data:
                    lat, lon = point["latitude"], point["longitude"]
                    for x in gridX:
                        if lon >= x:
                            coordX = x
                            break
                    for y in gridY:
                        if lat >= y:
                            coordY = y
                            break
                    grid[(coordX, coordY)] += 1

                # remove squares with 0 entries
                for key in list(grid.keys()):
                    if grid[key] == 0:
                        del grid[key]

                # center squares
                raster = []
                # creating raster and information object
                for key, point in zip(grid, data):
                    x = round(key[0] + longStep / 2, 5)
                    y = round(key[1] + latStep / 2, 5)
                    raster.append(
                        [
                            [x, y],
                            grid[key],
                            point["status"],
                            point["ip"],
                            point["OS"],
                            point["fullLine"],
                        ]
                    )
                # note size of grid squares
                self.information["dx"] = round(longStep / 2, 5)
                self.information["dy"] = round(latStep / 2, 5)
                # generate responseJson
                with open(self.responseJson, "w") as json_dump:
                    json.dump(
                        {"information": self.information, "raster": raster}, json_dump
                    )

        async def createJs(self, loglist, index, logCount, allLogs):
            # create js used to generate each map
            with open(self.responseJson, "r") as response:
                loglistObj = "const LOGLIST = " + str(loglist)
                # add location data for each log file to []
                allLogs.append(json.load(response))
                # write js data for all log files to []
                if index == logCount:
                    dataString = "const LOCATIONS = " + str(allLogs)
                    with open(self.loglist, "w") as f:
                        f.write(loglistObj)
                    # write js data to locations.js
                    with open(self.locationsJS, "w") as f:
                        f.write(dataString)

                    print("Done!")

    # create lists to build on with each log file that is processed
    files, accessLogs, allLogs = [], [], []
    # recursively build list of nginx/ denyhost logs
    for dirname, dirnames, filenames in os.walk(app.config["UPLOAD_DIR"]):
        for subdirname in dirnames:
            files.append(os.path.join(dirname, subdirname))

        for filename in filenames:

            if filename.startswith("access"):
                accessLogs.append(filename)

    logCount = len(accessLogs) - 1
    logMaps = []
    # used to test the execution time of map creation process while using async processing (as opposed to not using async)
    start = time.time()
    # For performance measurement, time.clock() is preferred
    perfStart = time.clock()

    # set up a list of all the LogViz objects for processing later
    for index, accessLog in enumerate(accessLogs):
        logMaps.append(LogViz(accessLog, accessLogs))

    async def genMaps(logMaps):
        for logMap in logMaps:
            await logMap.analyseLog(accessLogs, index, logCount, allLogs)

    asyncio.run(genMaps(logMaps))

    end = time.time()
    print("time spent was ")
    print(end - start)
    print("perf time spent was ")
    print(end - perfStart)
    print("maps have been generated")

    return render_template("map.html")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/map/<ip>", methods=["POST", "GET"])
def callHost(ip):
    print("blocking ", ip, " on the host machine..")

    """
    issue cmd from map_service to block the  IP on the host machine
    (ufw rules require sudo so you may need to enter your password once in the  servers terminal)
    """
    # TODO validate ip
    data = "sudo ufw deny in from " + ip
    try:
        response = requests.post(" http://172.21.0.1:8080", data=data)
    except Exception as e:
        return str(e)

    if response.status_code == 200:
        print("Successfully executed: ")
        print(data)
        return response.content


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)
