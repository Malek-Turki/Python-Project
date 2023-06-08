from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Prescription:
    def __init__(self,data):
        self.id=data['id']
        self.patient_id = data['patient_id']
        self.doctor_id = data['doctor_id']
        self.consultation_id = data['consultation_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #?====================create prescription================
    @classmethod
    def create_prescription(cls,data):
        query="""INSERT INTO prescriptions (patient_id,doctor_id,consultation_id)
        VALUE (%(patient_id)s, %(doctor_id)s,%(consultation_id)s);
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(f"oooooooooooooooooooooooooooo{result}ooooooooooooooooooooooooooooooooo")
        return result
    
# #     #?====================get prescription by patient_id and doctor_id================

#     @classmethod
#     def get_prescription(cls,data):
#         query = """ SELECT * FROM prescriptions WHERE patient_id = %(patient_id)s AND doctor_id = %(doctor_id)s ;"""
#         result= connectToMySQL(DATABASE).query_db(query,data)
#         if len(result)<1:
#             return False
#         return cls(result[0])
    
#     #?====================update prescription================
#     @classmethod
#     def update_prescription(cls,data):
#         query="""UPDATE prescriptions SET date = %(date)s, medicine_quantity = %(medicine_quantity)s, medicine_duration = %(medicine_duration)s, notes = %(notes)s WHERE patient_id = %(patient_id)s AND doctor_id = %(doctor_id)s;"""
#         result = connectToMySQL(DATABASE).query_db(query,data)
#         if len(result)<1:
#             return False
#         return cls(result[0])
#     #?====================delete prescription================
#     @classmethod
#     def delete_prescription(cls,data):
#         query="""DELETE FROM prescriptions WHERE patient_id = %(patient_id)s AND doctor_id = %(doctor_id)s;"""
#         result = connectToMySQL(DATABASE).query_db(query,data)
#         if len(result)<1:
#             return False
#         return cls(result[0])
    


    