from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models import admin_model
from flask import flash
# import pandas as pd
# import matplotlib.pyplot as plt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class Doctor:
    def __init__(self, data):
        self.id=data['id']
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.serial_number=data['serial_number']
        self.photo=data['photo']
        self.address=data['address']
        self.speciality=data['speciality']
        self.phone=data['phone']
        self.email=data['email']
        self.is_valid=data['is_valid']
        self.admin_id= 1
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

        #?==============Create Doctor=================#

    @classmethod
    def create_doctor(cls, data):
        query = """INSERT INTO doctors (first_name, last_name,serial_number, email, password)
        VALUES (%(first_name)s, %(last_name)s,%(serial_number)s, %(email)s, %(password)s)"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
        #?============== Read All Doctors =================#

    @classmethod
    def get_all_doctors(cls):
        query = """SELECT * FROM doctors"""
        results= connectToMySQL(DATABASE).query_db(query)
        doctors=[]
        for row in results:
            doctors.append(cls(row))
        return doctors

            #?=============Read one doctor by email =================#
    
    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * FROM doctors WHERE email = %(email)s"""
        result= connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
                #?=============Read one doctor by smn =================#
    
    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM doctors WHERE id = %(id)s"""
        result= connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    #?======================get all doctors for admin dasboard =================
    @classmethod
    def get_all_doctors(cls):
        query = """SELECT * FROM doctors"""
        results= connectToMySQL(DATABASE).query_db(query)
        doctors=[]
        for row in results:
            doctors.append(cls(row))
        return doctors
    
    #?======================appointmens_doctor_by_year=======================
    # @classmethod
    # def appointmens_doctor_by_year(cls, data):
    #     query = """SELECT YEAR(date) AS YEAR, COUNT(*) AS num_patients FROM appointments 
    #     WHERE doctor_id = %(id)s 
    #     GROUP BY YEAR(date)""" 
        
    #     results= connectToMySQL(DATABASE).query_db(query,data)
    #     cursor=connectToMySQL(DATABASE).cursor()
    #     cursor.execute(query)
    #     results = cursor.fetchall()

    #     # Convert the results to a pandas DataFrame
    #     df = pd.DataFrame(results, columns=["year", "num_patients"])

    #     # Create a line plot using matplotlib
    #     plt.plot(df["year"], df["num_patients"])
    #     plt.xlabel("Year")
    #     plt.ylabel("Number of patients")
    #     plt.title("Number of patients seen by doctor %(id)s per year" )
    #     plt.show()
    #     return df

            

    #?============valide doctor by admin =================
    @classmethod
    def valide_doctor_by_admin(cls, data):
        query = """UPDATE doctors SET is_valid=%(is_valid)s"""
        return connectToMySQL(DATABASE).query_db(query,data)
    #?============update doctor profile =================
    @classmethod
    def update_doctor_profile(cls, data):
        query = """UPDATE doctors SET first_name=%(first_name)s, last_name=%(last_name)s,photo=%(photo)s, address=%(address)s, speciality=%(speciality)s, phone=%(phone)s, email=%(email)s 
        WHERE id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)

    
    
    
    #!=======================================Validation====================================#
    @staticmethod #!!!!!!!! static method juste pour validation
    def validate_doctor(data):  
        is_valid = True
        if len(data['first_name']) < 2:
            is_valid = False
            flash("Invalid first name, must be greater than 2 characters!", "first_name")

        if len(data['last_name']) < 2:
            is_valid = False
            flash("Invalid last name, must be greater than 2 characters!", "last_name")
        
        if len(data['serial_number']) < 8:
            is_valid = False
            flash("Serial number is required", "serial_number")

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

            potential_user = Doctor.get_by_email(email_dict)
            if potential_user: #! email is not unique
                is_valid = False
                flash("email already taken ! Please login","email")
        if len(data['password']) < 1:
            is_valid = False
            flash("Invalid password, must be greater than 8 characters!", "password")
        # elif not data['password'] == data['confirm_password']:
        #     is_valid = False 
        #     flash("Password and confirm_password must match!", "confirm_password")
            

        return is_valid
