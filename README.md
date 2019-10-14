LogViz
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

1. Download the Nginx access.log Files from your web server and unzip the files or use the testing log files included in access-logs

2. Upload the log files to your browser at 0.0.0.0:3000. For multiple maps you can upload multiple log files at a time

3. Click 'GENERATE MAP'

4. After the map is generated hover over each datapoint (IP) to find the OS, request type and full request that originated from that IP.

5. To view multiple maps use the 'access.log' buttons on the right side of the map


## AWS cluster deploy from https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-cli-tutorial-ec2.html
