import connexion
import yaml
from connexion import NoContent
import logging.config
import requests

import datetime
import json
from pykafka import KafkaClient

import os

MAX_EVENTS = 10
EVENT_FILE = "events.json"
LINE_LIST = []

# Your functions here

'''lab 4'''
#with open('app_conf.yml', 'r') as f:
#    app_config = yaml.safe_load(f.read())

#with open('log_conf.yml', 'r') as f:
#    log_config = yaml.safe_load(f.read())
#    logging.config.dictConfig(log_config)

#logger = logging.getLogger('basicLogger')
'''lab 4'''
if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

def report_new_cases_admitted(body):
    """ Receives new cases event """
    """ Prints the parameter to the console (i.e., the raw Python dictionary) """
    # print(body)
    '''Handle the request here'''
    read_write_ten(body)
    # status_code = requests.post('http://localhost:8090/tracker/new_cases', json=body).status_code

    client = KafkaClient(hosts=str(app_config['events']['hostname'])+':'+str(app_config['events']['port']))
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

    msg = {"type": "new_cases",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}

    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    status_code = 201

    '''lab 4'''
    logger.info("Returned event new cases request with a unique id of " + str(body["patient_id"]))
    logger.info("Returned new cases order response ID:" + str(body["patient_id"]) + " with status " + str(status_code))
    '''lab 4'''

    return NoContent, 201

def report_newly_vaccinated(body):
    """ Receives new vaccination event """
    """ Prints the parameter to the console (i.e., the raw Python dictionary) """
    # print(body)
    '''Handle the request here'''
    read_write_ten(body)
    # status_code = requests.post('http://localhost:8090/tracker/new_vaccinated', json=body).status_code

    client = KafkaClient(hosts=str(app_config['events']['hostname'])+':'+str(app_config['events']['port']))
    topic = client.topics[str.encode(app_config['events']['topic'])]
    producer = topic.get_sync_producer()

    msg = {"type": "newly_vaccinated",
           "datetime":
               datetime.datetime.now().strftime(
                   "%Y-%m-%dT%H:%M:%S"),
           "payload": body}

    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    status_code = 201

    '''lab 4'''
    logger.info("Returned event newly vaccinated request with a unique id of " + str(body["patient_id"]))
    logger.info("Returned newly vaccinated order response ID:" + str(body["patient_id"]) + " with status " + str(status_code))
    '''lab 4'''

    return NoContent, 201

def read_write_ten(body):
    """ writes the last 10 received requests to JSON file """
    LINE_LIST.append(body)

    if len(LINE_LIST) >= MAX_EVENTS:
        """ If events.json has more than 10 lines """
        LINE_LIST.pop(0)
        JSON_file = open(EVENT_FILE, "w")
        for line in LINE_LIST:
            JSON_file.write(str(line) + "\n")
        print(LINE_LIST)

    else:
        """ If events.json has less than 10 lines """
        JSON_file = open(EVENT_FILE, "w")
        for line in LINE_LIST:
            JSON_file.write(str(line) + "\n")
        print(LINE_LIST)

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("BCIT2021-covid_tracker-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)