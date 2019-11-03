
![logviz logo](logviz-logo.png)

===================

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
docker-compose up
```

## Usage
==========================

1. Upload Log Files: Use the testing logs found in the test-logs directory, or Download Nginx access Log Files from your web server and unzip the files.

2. Upload multiple nginx log files to uploader at http://127.0.0.1:5000

3. click 'GENERATE MAP' and you will be routed to your maps

4. For more information about users OS, IP, request type etc, hover over datapoints on the SVG map

5. To switch to a different log file / map use the "Log Buttons" on the right side of the Map UI
