from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
# from flask_app.models import 
class Appointment:

    def __init__(self,data):

        self.id = data['id']
        self.date = data['date']
        self.doctor_id = data['doctor_id']
        self.patient_id = data['patient_id']
        self.motif = data['motif']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
#     #?===================create a new appointment==================
    @classmethod
    def create_appointment(cls,data):
        query=""" INSERT INTO appointments (date,motif,patient_id,doctor_id)
        VALUES (%(date)s,%(motif)s,%(patient_id)s,%(doctor_id)s) """
        return connectToMySQL(DATABASE).query_db(query,data)
    

# #     #?===================get all appointments==================

#     @classmethod
#     def get_all_appointments(cls):

#         query=""" SELECT * FROM appointments WHERE  """
#         return connectToMySQL(DATABASE).query_db(query)
    
#     #?===================get appointment by patient_id==================

#     @classmethod
#     def get_appointment_by_patient_id(cls,data):
#         query=""" SELECT * FROM appointment WHERE patient_id=%(patient_id)s AND doctor_id=%(doctor_id)s"""
#         result= connectToMySQL(DATABASE).query_db(query,data)
#         if len(result)<1:
#             return False
#         return cls(result[0])
    
    
    