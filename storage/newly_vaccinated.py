from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class NewlyVaccinated(Base):
    """ Newly Vaccinated """

    __tablename__ = "newly_vaccinated"

    id = Column(Integer, primary_key=True)
    patient_id = Column(String(250), nullable=False)
    patient_name = Column(String(250), nullable=False)
    vaccination_id = Column(String(250), nullable=False)
    timestamp = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, patient_id, patient_name, vaccination_id, timestamp):
        """ Initializes a heart rate reading """
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.vaccination_id = vaccination_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of a heart rate reading """
        dict = {}
        dict['id'] = self.id
        dict['patient_id'] = self.patient_id
        dict['patient_name'] = self.patient_name
        dict['vaccination_id'] = self.vaccination_id
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict
