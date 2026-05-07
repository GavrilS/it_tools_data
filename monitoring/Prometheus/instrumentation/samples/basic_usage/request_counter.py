from prometheus_client import start_http_server, Counter
import time


# 1. Define the metric
REQUEST_COUNT = Counter('app_requests_total', 'Total number of HTTP requests')

# 2. Update the metric in the code logic
def process_request():
    REQUEST_COUNT.inc()
    print('Request processed.')


if __name__=='__main__':
    # 3. Export the metric
    start_http_server(8000)
    flag = True
    counter = 0
    while flag:
        process_request()
        counter += 1
        if counter > 60:
            flag = False
        time.sleep(1)
