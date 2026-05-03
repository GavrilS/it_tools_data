"""
This is a sample code for an Azure Function that gets triggered by incoming logs in an Azure 
Event Hub and sends the logs to Elasticsearch. The function is using the Python v2 programming 
model.

Requirements:
    - azure-functions
    - elasticsearch

Environment:
    - ES_HOSTS -> the Elasticsearch host
    - ES_API_KEY -> the key used to authenticate to Elastic
    - ES_INDEX -> the index where the logs will be saved
    - EVENT_HUB_NAME -> the name of the Event Hub trigger
    - EVENT_HUB_CONNECTION_STRING -> the connection string to the Event Hub
"""
import azure.functions as func
import logging
import json
import os
from elasticsearch import Elasticsearch

app = func.FunctionApp()

# Elastic config (it's advised to put it in App Settings)
ES_HOSTS = os.getenv("ES_HOSTS", "")
ES_API_KEY = os.getenv("ES_API_KEY", "")
ES_INDEX = os.getenv("ES_INDEX", "")
# Event Hub configs
EVENT_HUB_NAME = os.getenv("EVENT_HUB_NAME", "")
EVENT_HUB_CONNECTION_STRING = os.getenv("EVENT_HUB_CONNECTION_STRING", "")

# Initializing the Elatic client
def set_up_es_client():
    try:
        es = Elasticsearch(
            [ES_HOSTS],
            api_key=ES_API_KEY
        )
        return es
    except Exception as e:
        logging.error(f"Couldn't set up the Elastic connection - {str(e)}")

es = set_up_es_client()

@app.event_hub_trigger(arg_name="events", 
                       event_hub_name=EVENT_HUB_NAME,
                       connection=EVENT_HUB_CONNECTION_STRING) 
def eventhub_to_elastic(events: list[func.EventHubEvent]):
    for event in events:
        try:
            # Decode the event
            body = event.get_body().decode('utf-8')
            log_entry = json.loads(body)

            # Adding Event Hub metadata (optional)
            log_entry['azure_metadata'] = {
                'enqueued_time': event.enqueued_time.isoformat() if event.enqueued_time else None,
                'offset': event.offset,
                'sequence_number': event.sequence_number
            }

            # index the logs in Elastic
            res = es.index(index=ES_INDEX, document=log_entry)
            logging.info(f"Log indexed successfully: {res['result']}")

        except Exception as e:
            logging.error(f"Error processing event: {str(e)}")
