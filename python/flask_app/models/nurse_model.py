from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
# from flask_app.models import 
from flask import flash


class Nurse:

    def __init__(self,data):
        self.id = data['id']
        self.nurse_name = data['nurse_name']
        self.nurse_phone = data['nurse_phone']
        self.log_code = data['log_code']
        self.doctor_id = data['doctor_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #?===============Create Nurse Account=================#
    
    @classmethod
    def create_nurse_account(cls,data):
        query="""
        INSERT INTO nurses (nurse_name,nurse_phone,log_code,doctor_id)
        VALUES (%(nurse_name)s,%(nurse_phone)s,%(log_code)s,%(doctor_id)s);"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #?===============get Nurse Account=================#
    @classmethod
    def get_all_nurse_account(cls,data):
        query="""
        SELECT * FROM nurses;"""
        result= connectToMySQL(DATABASE).query_db(query,data)
        nurses=[]
        for row in result:
            nurses.append(cls(row))
        return nurses
    
    #?=============Read one nurse by code =================#
    
    @classmethod
    def get_nurse_by_code(cls, data):
        query = """SELECT * FROM nurses WHERE log_code = %(log_code)s"""
        result= connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    
   