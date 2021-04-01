import connexion
#import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
from connexion import NoContent

# lab9
from flask_cors import CORS, cross_origin

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
# from base import Base
# from new_cases import NewCases
# from newly_vaccinated import NewlyVaccinated
import datetime
import yaml
import logging.config
import json
import requests

import os
# DB_ENGINE = create_engine("sqlite:///readings.sqlite")
'''lab 4'''
#with open('app_conf.yml', 'r') as f:
#    app_config = yaml.safe_load(f.read())

#with open('log_conf.yml', 'r') as f:
#    log_config = yaml.safe_load(f.read())
#    logging.config.dictConfig(log_config)

#logger = logging.getLogger('basicLogger')
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

# DB_ENGINE = create_engine('mysql+pymysql://' + app_config['datastore']['user'] + ':' + app_config['datastore']['password'] + '@' +app_config['datastore']['hostname'] + ':' + str(app_config['datastore']['port']) + '/' + app_config['datastore']['db'])
'''lab 4'''

# Base.metadata.bind = DB_ENGINE
# DB_SESSION = sessionmaker(bind=DB_ENGINE)

# MAX_EVENTS = 10
# EVENT_FILE = "events.json"
# LINE_LIST = []

# Your functions here
# def report_new_cases_admitted(body):
#     """ Receives new cases event """
#     session = DB_SESSION()
#     newCases = NewCases(body['patient_id'],
#                        body['patient_name'],
#                        body['case_id'],
#                        body['timestamp'],)
#     session.add(newCases)
#     session.commit()
#     session.close()
#     '''lab 4'''
#     logger.debug("Received event new cases request with a unique id of " + str(body["patient_id"]))
#     '''lab 4'''
#     return NoContent, 201

"""lab5-start"""
# def get_new_cases(timestamp):
#     session = DB_SESSION()
#     timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
#     print(timestamp_datetime)
#     readings = session.query(NewCases).filter(NewCases.date_created >= timestamp_datetime)
#     results_list = []
#     for reading in readings:
#         results_list.append(reading.to_dict())
#     session.close()
#     logger.info("Query for new cases after %s returns %d results" % (timestamp, len(results_list)))
#     return results_list, 200
"""lab5-end"""

# def report_newly_vaccinated(body):
#     """ Receives new vaccination event """
#     session = DB_SESSION()
#     newlyVaccinated = NewlyVaccinated(body['patient_id'],
#                    body['patient_name'],
#                    body['vaccination_id'],
#                    body['timestamp'],)
#     session.add(newlyVaccinated)
#     session.commit()
#     session.close()
#     '''lab 4'''
#     logger.debug("Received event newly vaccinated request with a unique id of " + str(body["patient_id"]))
#     '''lab 4'''
#     return NoContent, 201

"""lab5-start"""
# def get_newly_vaccinated(timestamp):
#     session = DB_SESSION()
#     timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
#     print(timestamp_datetime)
#     readings = session.query(NewlyVaccinated).filter(NewlyVaccinated.date_created >= timestamp_datetime)
#     results_list = []
#     for reading in readings:
#         results_list.append(reading.to_dict())
#     session.close()
#     logger.info("Query for newly vaccinated after %s returns %d results" % (timestamp, len(results_list)))
#     return results_list, 200
"""lab5-end"""

"""lab5-start"""
def get_stats():
    "Log an INFO message indicating request has started"
    logger.info("request has started")
    "Read in the current statistics from the JSON file (defined in your configuration)"
    try:
        with open(app_config['datastore']['filename'], 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        string = "Statistics does not exist"
        return string, 404
    "Log a DEBUG message with the contents of the Python Dictionary"
    logger.debug(data)
    "Log an INFO message indicating request has completed"
    logger.info("request has completed")
    "Return the Python dictionary as the context and 200 as the response code"
    return data, 200

def populate_stats():
    """Log an INFO message indicating periodic processing has started"""
    logger.info('Start Periodic Processing')

    """Read in the current statistics from the JSON file (filename defined in your configuration)"""
    with open(app_config['datastore']['filename'], 'r') as f:
        data = json.load(f)
        print(data)

    """Get the current datetime"""
    now = str(datetime.datetime.now())
    now = now.replace(' ', 'T')
    now = now[:-7] + "Z"

    "Query the two GET endpoints from your Data Store Service (using requests.get) to get all new events from the last datetime you requested them (from your statistics) to the current datetime"
    endpoint_one = app_config['eventstore_one']['url']
    endpoint_one = endpoint_one + "?timestamp=" + str(now)
    print(endpoint_one)

    status_code_one = requests.get(endpoint_one)
    print(endpoint_one)
    print(status_code_one)

    status_code_one_json = status_code_one.json()
    print(status_code_one, "this is the status code 1 json")

    if status_code_one.status_code != 200:
        logger.error("error %d" % status_code_one.status_code)
    else:
        logger.info("received: %d" % len(status_code_one_json))

    endpoint_two = app_config['eventstore_two']['url']
    endpoint_two = endpoint_two + "?timestamp=" + str(now)

    status_code_two = requests.get(endpoint_two)
    print(endpoint_two)
    print(status_code_two)

    status_code_two_json = status_code_two.json()
    print(status_code_two, "this is the status code 2 json")

    if status_code_two.status_code != 200:
        logger.error("error %d" % status_code_two.status_code)
    else:
        logger.info("received: %d" % len(status_code_two_json))

    "Based on the new events from the Data Store Service:"
    with open(app_config['datastore']['filename'], 'r') as f:
        data = json.load(f)

    num_new_cases_readings = data["num_new_cases_readings"]
    num_newly_vaccinated_readings = data["num_newly_vaccinated_readings"]
    longest_patient_name = data["longest_patient_name"]
    shortest_patient_name = data["shortest_patient_name"]

    for x in status_code_one_json:
        num_new_cases_readings += 1
        length = len(x["patient_name"])
        print(length, "LOOK AT ME")
        if length > len(longest_patient_name):
            longest_patient_name = x["patient_name"]
        if length < len(shortest_patient_name):
            shortest_patient_name = x["patient_name"]
    for x in status_code_two_json:
        num_newly_vaccinated_readings += 1

    data = {}
    data["num_new_cases_readings"] = num_new_cases_readings
    data["num_newly_vaccinated_readings"] = num_newly_vaccinated_readings
    data["longest_patient_name"] = longest_patient_name
    data["shortest_patient_name"] = shortest_patient_name

    data["last_Updated"] = now

    with open(app_config['datastore']['filename'], 'w') as f:
        json.dump(data, f)

    logger.debug(data)

    "Log an INFO message indicating period processing has ended"
    logger.info("period processing has ended")
    # /tracker/get_new_cases?timestamp=%Y-%m-%dT%H:%M:%SZ

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats,
    'interval',

    seconds=app_config['scheduler']['period_sec'])

    sched.start()
"""lab5-end"""

app = connexion.FlaskApp(__name__, specification_dir='')
# lab9
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("BCIT2021-covid_tracker-1.0.0-swagger.yaml",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    # change Storage port 8080 -> 8090
    init_scheduler()
    app.run(port=8100, use_reloader=False)