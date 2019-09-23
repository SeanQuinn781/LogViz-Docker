LogViz
===================

View the geolocation, status code, operating system and full request of IP addresses visiting your web server using tooltips on an SVG map

- Uses Flask and docker to build the file upload and geolocation services 

- Process multiple Nginx Log files with python and the Geoip Maxmind Database to Geolocate the IPs and generate the map

![](logviz.gif)

Originally forked from: 

https://github.com/LeviBorodenko/Logation

Uses the flask file upload for uploading log files to Docker:

https://github.com/blueimp/jQuery-File-Upload



## Install/Run


### Docker
1. Using docker-compose

```
docker-compose up --build
```

2. Using docker without compose

```
docker build -t upload_service .
```

```
docker build -t map_service .
```

run the containers
```
docker run -p 3000:80 -t upload_service
docker run -p 5000:80 -t map_service

```

## Usage

1. Download the Nginx access.log Files from your web server and unzip the files or use the testing log files included in access-logs

2. Upload the log files to your browser at 0.0.0.0:3000. For multiple maps you can upload multiple log files at a time

3. Click 'GENERATE MAP'

4. After the map is generated hover over each datapoint (IP) to find the OS, request type and full request that originated from that IP.

5. To view multiple maps use the 'access.log' buttons on the right side of the map


## Note
There is a separate repo for running LogViz in a single flask app/ container, or on web server using Gunicorn/Nginx/wsgi, see:
https://www.github.com/seanquinn781/LogViz


