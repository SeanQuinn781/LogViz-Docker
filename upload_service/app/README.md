LOGVIZ
===================

![](logviz.gif)

## Description
File Upload Script which built on Python Flask and [jQuery-File-Upload](https://github.com/blueimp/jQuery-File-Upload/) with multiple file selection, drag&amp;drop support, progress bars, validation and preview images, audio and video for jQuery.


## Simple Setup

1. Install python3 venv

```
sudo apt-get install python3-venv
```

2. Create virtual enviroment 

```
cd LogViz
python3 -m venv LogViz
```

3. Activate virtual environment:
```
source LogViz/bin/activate
```

4. Install python requirements in the environment:  
```
$ pip install -r --user requirements.txt
```

5. Run the app:

```
python app.py
```

Go to http://127.0.0.1:5000


USAGE
==========================


6. Upload Log Files:

Download the Nginx access Log Files from your web server and unzip (or uncomment the unzip function in LogViz/app.py)

7. Upload them to the interface in your browser at http://127.0.0.1:5000 (this app can handle multiple log files at a time and will generate as many maps as log files are uploaded)

8. click 'GENERATE MAP' and you will be routed to your 'LogViz' map

9. For more information about users OS, IP, request type etc, hover over datapoints on the SVG map


## Server setup with Gunicorn / Nginx

See documentation and scripts in /server_config

