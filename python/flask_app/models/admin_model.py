from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import doctor_model
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class Admin:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #?==============Create Admin=================#

    @classmethod
    def create_admin(cls, data):
        query = """INSERT INTO admin ( email, password)
        VALUES ( %(email)s, %(password)s)"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    #?=============Read admin by email =================#
    
    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * FROM admin WHERE email = %(email)s"""
        result= connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    
    #!======================validation admin==================
    @staticmethod
    def validate_admin(data):
        is_valid = True
        
        if len(data['email']) < 1:
            is_valid = False
            flash("Email is required", "email")

        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "email")
            is_valid = False
        else:
            email_dict = {
                'email' : data['email']
            }

            potential_user = Admin.get_by_email(email_dict)
            if potential_user: #! email is not unique
                is_valid = False
                flash("email already taken ! Please login","email")
        if len(data['password']) < 1:
            is_valid = False
            flash("Invalid password, must be greater than 8 characters!", "password")
        elif not data['password'] == data['confirm_password']:
            is_valid = False 
            flash("Password and confirm_password must match!", "confirm_password")
            

        return is_valid




        
    