from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class NewCases(Base):
    """ New Cases """

    __tablename__ = "new_cases"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String(250), nullable=False)
    patient_name = Column(String(250), nullable=False)
    case_id = Column(Integer, nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, patient_id, patient_name, case_id, timestamp):
        """ Initializes a blood pressure reading """
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.case_id = case_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of a new cases """
        dict = {}
        dict['id'] = self.id
        dict['patient_id'] = self.patient_id
        dict['patient_name'] = self.patient_name
        dict['case_id'] = self.case_id
        dict['new_cases'] = {}
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict
