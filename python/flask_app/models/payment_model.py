from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import doctor_model
from flask import flash
class Payment:
    def __init__(self,data):
        self.id=data['id']
        self.doctor_id=data['doctor_id']
        self.start_date=data['start_date']
        self.end_date=data['end_date']
        self.amount=data['amount']
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]

    #!================create payment================
    @classmethod
    def fix_payment(cls,data):
        query="INSERT INTO payment (doctor_id) VALUES (%(doctor_id)s)"
        return connectToMySQL(DATABASE).query_db(query,data)
    #!================get all payment================
    @classmethod
    def get_all_payments(cls):
        query="SELECT * FROM payment"
        return connectToMySQL(DATABASE).query_db(query)


        