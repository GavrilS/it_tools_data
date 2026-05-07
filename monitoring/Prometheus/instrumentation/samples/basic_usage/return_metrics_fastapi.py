'''
Return Prometheus compatible metrics without starting a separate HTTP server, but using one 
build with fastapi. This is an excerpt showing an example of how to return the metrics.
'''
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

@app.get('/metrics')
def get_metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

