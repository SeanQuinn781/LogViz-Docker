"""
This is a simple python server that will run commands sent from the mapService on the host machine
This server can be used to issue ufw blocks in real time
it works by binding the port 8080 between the host and the container, allowing HTTP requests to localhost:8080
to ask the python server running shell scripts with popen, run a curl or writing code to make a HTTP request curl -d '{"foo":"bar"}' localhost:8080
"""
import time
import json
import subprocess
import requests
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
PORT_NUMBER = 8080

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/foo': {'status': 200},
            '/bar': {'status': 302},
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

    def do_POST(self):
                    length = int(self.headers.get('content-length'))
                    field_data = self.rfile.read(length)
                    print(field_data)
                    self.send_response(200)
                    self.end_headers()
                    data = field_data
                    print(data)
                    cmd = data
                    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                    p_status = p.wait()
                    (output, err) = p.communicate()
                    print(output)
                    print("Command exit status/return code : ", p_status)

                    self.wfile.write(cmd)
                    return

                    if self.path in paths:
                                    self.respond(paths[self.path])
                    else:
                                    self.respond({'status': 500})

    def handle_http(self, status_code, path):
                    self.send_response(status_code)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    content = '''
                                    <html><head><title>Title goes here.</title></head>
                                    <body><p>This is a test.</p>
                                    <p>You accessed path: {}</p>
                                    </body></html>
                                    '''.format(path)
                    return bytes(content, 'UTF-8')

    def respond(self, opts):
                    response = self.handle_http(opts['status'], self.path)
                    self.wfile.write(response)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
