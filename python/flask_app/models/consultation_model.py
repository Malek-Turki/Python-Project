from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import prescription_model
class Consultation:
    
    def __init__(self,data):
        self.symptoms=data['symptoms']
        self.analysis=data['analysis']
        self.conclusion=data['conclusion']
        self.doctor_id = data['doctor_id']
        self.patient_id = data['patient_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.presc=[]
    
    #?=============create consultation==============
    @classmethod
    def create_consultation(cls,data):
        query = """ INSERT INTO consultations (patient_id,doctor_id,symptoms,analysis,conclusion)
        Values (%(patient_id)s,%(doctor_id)s,%(symptoms)s,%(analysis)s,%(conclusion)s);"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
#     #?=============get last consultation  id================
    @classmethod
    def get_last_consultation_by_id(cls,data):
        query = """ SELECT * FROM consultations
        left join prescription on consultations.id=prescriptions.consultation_id
        WHERE doctor_id = %(id)s  and patient_id = %(patient_id)s
        ORDER BY consultations.id DESC limit 1"""
        results= connectToMySQL(DATABASE).query_db(query,data)
        if len(results)<1:
            return results
        these_consultations=[]
        
        for row in results:
            this_consultation = cls(row)
            prescription_data = {
                'id': row['prescriptions.id'],
                'doctor_id' :row['prescriptions.doctor_id'],
                'patient_id' :row['prescriptions.patient_id'],
                'consultation_id' :row['consultation_id'],
                'created_at' :row['prescriptions.created_at'],
                'updated_at' : row['prescriptions.updated_at']
            }
            this_prescription= prescription_model.Prescription(prescription_data)
            this_consultation.presc=this_prescription
            
            print(this_consultation)

        return this_consultation

    
    #?=============get consultation by patient_id and doctor_id==============
    @classmethod
    def get_consultation(cls,data):
        query = """ SELECT * FROM consultations WHERE patient_id = %(patient_id)s AND doctor_id = %(doctor_id)s ;"""
        result= connectToMySQL(DATABASE).query_db(query,data)
        return result
#     #?=============delete patient consultation============
#     @classmethod
#     def delete_consultation(cls,data):
#         query = """ DELETE FROM consultations WHERE patient_id = %(patient_id)s AND doctor_id = %(doctor_id)s ;"""
#         return connectToMySQL(DATABASE).query_db(query,data)
#     #?=============update patient consultation============
#     @classmethod
#     def update_consultation(cls,data):
#         query = """ UPDATE consultations SET patient_id = %(patient_id)s,doctor_id = %(doctor_id)s,date = %(date)s,symptoms = %(symptoms)s,analysis = %(analysis)s,conclusion = %(conclusion)s WHERE patient_id = %(patient_id)s AND doctor_id = %(doctor_id)s ;"""
#         return connectToMySQL(DATABASE).query_db(query,data)
#     #!================validation patient================
#     @staticmethod
#     def validate_consultation(data):
#         is_valid = True
#         if len(data['symptoms']) < 2:
#             is_valid = False
#             flash("Invalid symptoms, must be greater than 2 characters!", "symptoms")
#         if len(data['analysis']) < 2:
#             is_valid = False
#             flash("Invalid analysis, must be greater than 2 characters!", "analysis")
#         if len(data['conclusion']) < 2:
#             is_valid = False
#             flash("Invalid conclusion, must be greater than 2 characters!", "conclusion")
        
#         return is_valid

    
    
    

