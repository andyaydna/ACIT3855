import connexion
#import mysql.connector
from connexion import NoContent

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
# from new_cases import NewCases
# from newly_vaccinated import NewlyVaccinated
import datetime
import yaml
import logging.config

import json
from pykafka import KafkaClient
from pykafka.common import OffsetType

# lab9
from flask_cors import CORS, cross_origin

import os
# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
#with open('app_conf.yml', 'r') as f:
#    app_config = yaml.safe_load(f.read())

#with open('log_conf.yml', 'r') as f:
#    log_config = yaml.safe_load(f.read())
#    logging.config.dictConfig(log_config)

#logger = logging.getLogger('basicLogger')
if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
        print("In Test Environment")
        app_conf_file = "/config/app_conf.yml"
        app_conf_file = "/config/log_conf.yml"
else:
        print("In Dev Environment")
        app_conf_file = "/config/app_conf.yml"
        app_conf_file = "/config/log_conf.yml"
with open(app_conf_file, 'r') as f:
        app_config = yaml.safe_load(f.read())
        logging.config.dictConfig(log_config)
logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % app_conf_file)
#DB_ENGINE = create_engine('mysql+pymysql://' + app_config['datastore']['user'] + ':' + app_config['datastore']['password'] + '@' +app_config['datastore']['hostname'] + ':' + str(app_config['datastore']['port']) + '/' + app_config['datastore']['db'])

# Base.metadata.bind = DB_ENGINE
# DB_SESSION = sessionmaker(bind=DB_ENGINE)

MAX_EVENTS = 10
EVENT_FILE = "events.json"
LINE_LIST = []

# Your functions here

def get_new_cases(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    #debugging
    # for events in consumer:
    #     print(events)
    #debugging
    logger.info("Retrieving new cases at index %d" % index)
    try:
        count = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            #lab7
            if msg["type"] == "new_cases":
                if count == index:
                    return msg["payload"], 201
                count += 1
    except:
        logger.error("No more messages found")

    logger.error("Could not find new cases at index %d" % index)
    return {"message": "Not Found"}, 404

def get_newly_vaccinated(index):
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=1000)
    #debugging
    # for events in consumer:
    #     print(events)
    #debugging
    logger.info("Retrieving new cases at index %d" % index)
    try:
        count = 0
        for msg in consumer:
            msg_str = msg.value.decode('utf-8')
            msg = json.loads(msg_str)
            #lab7
            if msg["type"] == "newly_vaccinated":
                if count == index:
                    return msg["payload"], 201
                count += 1
    except:
        logger.error("No more messages found")

    logger.error("Could not find new cases at index %d" % index)
    return {"message": "Not Found"}, 404

app = connexion.FlaskApp(__name__, specification_dir='')
# lab9
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("BCIT2021-covid_tracker-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    # change Storage port 8080 -> 8090
    logger.info("Hostname: " + str(app_config['datastore']['hostname']) + " Port: " + str(app_config['datastore']['port']))
    app.run(port=8070)