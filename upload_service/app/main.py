import requests
# for file upload module
import os
import json as simplejson
from flask import Flask, request, render_template, \
    redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap
from flask_pymongo import PyMongo
from werkzeug import secure_filename
from lib.upload_file import uploadfile
from os.path import join, dirname
from allowedFile import allowedFileExtension, allowedFileType

app = Flask(__name__)
app.config['UPLOAD_DIR'] = '/upload_service/app/static/data/'
app.config['ASSET_DIR'] = 'static/mapAssets/'
app.config['CLEAN_DIR'] = '/upload_service/app/static/cleanData/'
app.config['HTML_DIR'] = 'static/'

# app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

IGNORED_FILES = set(['.gitignore'])

bootstrap = Bootstrap(app)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files['file']
        print('IN UPLOAD')
        if files:
            filename = secure_filename(files.filename)
            mime_type = files.content_type
            validFileType = allowedFileType(mime_type)

            if not allowedFileExtension(files.filename) or validFileType == False:
                print('not a valid log file type')
                result = uploadfile(name=filename, type=mime_type, size=0,
                                    not_allowed_msg="File type not allowed in app.py validation")

            else:
                uploaded_file_path = os.path.join(app.config['UPLOAD_DIR'], filename)
                files.save(uploaded_file_path)
                size = os.path.getsize(uploaded_file_path)
                result = uploadfile(name=filename, type=mime_type, size=size)

            return simplejson.dumps({"files": [result.get_file()]})

    # get all logs in ./data directory
    if request.method == 'GET':
        files = [f for f in os.listdir(app.config['UPLOAD_DIR']) if
                 os.path.isfile(os.path.join(app.config['UPLOAD_DIR'], f)) and f not in IGNORED_FILES]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(app.config['UPLOAD_DIR'], f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    return redirect(url_for('index'))


# serve static files
@app.route("/data/<string:filename>", methods=['GET'])
def get_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_DIR']), filename=filename)


@app.route("/delete/<string:filename>", methods=['DELETE'])
def delete(filename):
    # remove the log file
    log_file = os.path.join(app.config['UPLOAD_DIR'], filename)

    # remove the log file
    if os.path.exists(log_file):
        try:
            os.remove(log_file)

            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=3000)
