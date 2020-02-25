FROM tiangolo/uwsgi-nginx-flask:python3.7

# copy over our requirements.txt file
COPY requirements.txt /tmp/

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt
RUN pip install --upgrade maxminddb-geolite2

# copy over our app code
COPY ./app /app
