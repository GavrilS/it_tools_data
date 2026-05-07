'''
Expose Prometheus metrics on already running server. This sample is only an excerpt showing 
the code needed to export the Prometheus metrics from an already running server.
'''
from flask import Flask, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

@app.route('/metrics')
def metrics():
    # Generate the current state of all metrics in a Prometheus format
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__=='__main__':
    app.run(port=5000)
