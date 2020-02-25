
![logviz logo](logviz-logo.png)

## Description
View the geolocation, status code, operating system and full request of IP addresses visiting NGINX using tooltips on an SVG map

- Upload and processes multiple Nginx Log files and generate multiple maps at a time

- Backend: Flask for routing, processing logs, and python geoip2/maxmindDB for geolocation

- Frontend: React for UI, d3 for generating svg maps

- Runs two seperate flask containers, upload service and map service

- There is a separate repo for running LogViz in a single flask container, or without Docker using Gunicorn/Nginx/wsgi/systemd: https://www.github.com/seanquinn781/LogViz

![](logviz.gif)

## Built with

Svg raster code:

https://github.com/LeviBorodenko/Logation

File upload:

https://github.com/blueimp/jQuery-File-Upload


## Install/Run

```
1. Create the docker network:

docker network create logviz

2. Build and run the containers:

docker-compose up --build

3. Start the python server:
python3 ufwHost.py
```

## Usage

1. Upload Log Files: Use the testing logs found in the test-logs directory, or Download Nginx access Log Files from your web server and unzip the files.

2. Upload multiple nginx log files to uploader at http://127.0.0.1:3000

3. click 'GENERATE MAP' and you will be routed to your maps

4. For more information about users OS, IP, request type etc, hover over datapoints on the SVG map

5. To switch to a different log file / map use the "Log Buttons" on the right side of the Map UI

## Blocking IPs from the map service on your host machine

1. Start the docker containers and the python web server:
docker-compose up --build
python3 ufwHost.py

2. Allow incoming connections from the map_service to the host:
docker network inspect logviz (find the ip range of your docker network)
allow incoming from your docker container map_service to your docker network gateway (host)
Example:
sudo ufw allow in from 172.21.0.2 to 172.21.0.1

3. Update /map_service/app/main.py to call the host at the correct ip:
response = requests.post("http://172.21.0.1:8080", data=data)
or 
response = requests.post("http://172.18.0.1/16:8080", data=data) 
etc...



3. Go to http://127.0.0.1:3000, upload your log files. Click generate map, hover over the request tooltip and click 'UFW block ip'

4. You will need to run sudo once in the web server terminal to execute the ufw rule

If you don't need ufw blocks you can remove 'external' from the logviz network, and run the containers without the python server

