import sys
from datetime import datetime
from Adafruit_IO import MQTTClient

AIO_FEED_IDS = ["humidity", "luminance", "temperature"]
AIO_USERNAME = "leanhhuy"
AIO_KEY = "aio_QsPr27TV7fjzAsbothVWx7dIrVLI"

humidityData = []
luminanceData = []
temperatureData = []
accountData = []

def  connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)

def subscribe(client,userdata,mid,granted_qos) :
    print("Subscribe " + AIO_FEED_IDS[mid - 1] + " thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)

def  message(client , feed_id , payload):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S %D")
    print("Nhan du lieu tu " + feed_id + ": " + payload + " at " + current_time)
    if feed_id == "humidity":
        humidityData.append([payload, current_time])
    if feed_id == "luminance":
        luminanceData.append([payload, current_time])
    if feed_id == "temperature":
        temperatureData.append([payload, current_time])

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

#--------------------------------------------------

from wsgiref.simple_server import make_server
import json

def application(environ, start_response):
    """
    A simple WSGI application that returns a greeting message.
    """
    if environ['PATH_INFO'] == '/':
        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        message = 'Welcome to python backend server'
        return [message.encode('utf-8')]
    elif environ['PATH_INFO'] == '/humidity':
        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [json.dumps(humidityData).encode('utf-8')]
    elif environ['PATH_INFO'] == '/temperature':
        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [json.dumps(temperatureData).encode('utf-8')]
    elif environ['PATH_INFO'] == '/luminance':
        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [json.dumps(luminanceData).encode('utf-8')]
    elif environ['PATH_INFO'] == '/login' and environ['REQUEST_METHOD'] == 'POST':
        content_length = int(environ.get('CONTENT_LENGTH', '0'))
        raw_data = environ['wsgi.input'].read(content_length)
        data = json.loads(raw_data)
        print(data)

        # Return the result as a JSON-encoded string
        status = '200 OK'
        headers = [('Content-type', 'application/json; charset=utf-8')]
        start_response(status, headers)
        message = {'resultt': data}
        return [json.dumps(message).encode('utf-8')]
    else:
        status = '404 Not Found'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        message = 'Not Found'
        return [message.encode('utf-8')]

if __name__ == '__main__':
    host = 'localhost'
    port = 8000
    server = make_server(host, port, application)
    print(f'Serving on http://{host}:{port}')
    server.serve_forever()