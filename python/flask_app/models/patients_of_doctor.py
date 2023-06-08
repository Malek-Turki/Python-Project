from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import doctor_model
from flask_app.models import consultation_model
from flask_app.models import appointment_model
from flask_app import DATABASE

class Patients:
    def __init__(self,data):

        self.id = data['id']
        self.doctor_id = data['doctor_id']
        self.patient_id = data['patient_id']
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]

   #?===============Create Patients of doctor=================#
    @classmethod
    def save_patients_doctor(cls,data):
        query="""
        INSERT INTO patients_of_doctor (doctor_id,patient_id)
        VALUES (%(doctor_id)s,%(patient_id)s)"""
        return connectToMySQL(DATABASE).query_db(query,data)
