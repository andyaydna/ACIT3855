import connexion
import mysql.connector
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_ #lab11
from base import Base
from new_cases import NewCases
from newly_vaccinated import NewlyVaccinated
import datetime
import yaml
import logging.config

import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

import os
# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
'''lab 4'''
#with open('app_conf.yml', 'r') as f:
#    app_config = yaml.safe_load(f.read())

#with open('log_conf.yml', 'r') as f:
#    log_config = yaml.safe_load(f.read())
#    logging.config.dictConfig(log_config)

#logger = logging.getLogger('basicLogger')

#DB_ENGINE = create_engine('mysql+pymysql://' + app_config['datastore']['user'] + ':' + app_config['datastore']['password'] + '@' +app_config['datastore']['hostname'] + ':' + str(app_config['datastore']['port']) + '/' + app_config['datastore']['db'])
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

# Base.metadata.bind = DB_ENGINE
# DB_SESSION = sessionmaker(bind=DB_ENGINE)

MAX_EVENTS = 10
EVENT_FILE = "events.json"
LINE_LIST = []

# Your functions here
def report_new_cases_admitted(body):
    """ Receives new cases event """
    session = DB_SESSION()
    newCases = NewCases(body['patient_id'],
                       body['patient_name'],
                       body['case_id'],
                       body['timestamp'],)
    session.add(newCases)
    session.commit()
    session.close()
    '''lab 4'''
    logger.debug("Received event new cases request with a unique id of " + str(body["patient_id"]))
    '''lab 4'''
    return NoContent, 201

"""lab5-start"""
def get_new_cases(timestamp, end_timestamp): # lab11
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%S") # lab11
    print(timestamp_datetime)
    readings = session.query(NewCases).filter( # lab11
        and_(NewCases.date_created >= timestamp_datetime,
            NewCases.date_created < end_timestamp_datetime))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for new cases after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200
"""lab5-end"""

def report_newly_vaccinated(body):
    """ Receives new vaccination event """
    session = DB_SESSION()
    newlyVaccinated = NewlyVaccinated(body['patient_id'],
                   body['patient_name'],
                   body['vaccination_id'],
                   body['timestamp'],)
    session.add(newlyVaccinated)
    session.commit()
    session.close()
    '''lab 4'''
    logger.debug("Received event newly vaccinated request with a unique id of " + str(body["patient_id"]))
    '''lab 4'''
    return NoContent, 201

"""lab5-start"""
def get_newly_vaccinated(timestamp, end_timestamp): # lab11
    session = DB_SESSION()
    timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%S") # lab11
    print(timestamp_datetime)
    readings = session.query(NewlyVaccinated).filter( # lab11
        and_(NewlyVaccinated.date_created >= timestamp_datetime,
            NewlyVaccinated.date_created < end_timestamp_datetime))
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info("Query for newly vaccinated after %s returns %d results" % (timestamp, len(results_list)))
    return results_list, 200
"""lab5-end"""

"""lab7-start"""
def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])
    client = KafkaClient(hosts=hostname)
    topic = client.topics[str.encode(app_config["events"]["topic"])]

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "new_cases":  # Change this to your event type
            # Store the event1 (i.e., the payload) to the DB
            report_new_cases_admitted(payload)
        elif msg["type"] == "newly_vaccinated":  # Change this to your event type
            # Store the event2 (i.e., the payload) to the DB
            report_newly_vaccinated(payload)
    # Commit the new message as being read
    consumer.commit_offsets()
"""lab7-end"""

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("BCIT2021-covid_tracker-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    # change Storage port 8080 -> 8090
    logger.info("Hostname: " + str(app_config['datastore']['hostname']) + " Port: " + str(app_config['datastore']['port']))

    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()

    #this shit
    app.run(port=8090)