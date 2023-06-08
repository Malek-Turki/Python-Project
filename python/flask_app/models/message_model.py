from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Message:
    
    def __init__(self,data):
        self.id =data['id']
        self.admin_id = data['admin_id']
        self.doctor_id = data['doctor_id']
        self.subject = data['subject']
        self.email = data['email']
        self.username = data['username']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
        #?==============Create message=================#

    @classmethod
    def create_message(cls, data):
        query = """INSERT INTO messages (username, email, subject, content)
        VALUES ( %(username)s,%(email)s, %(subject)s , %(content)s)"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
        #?======================get all messages for admin dasboard =================
    @classmethod
    def get_all_messages(cls):
        query = """SELECT * FROM messages"""
        results= connectToMySQL(DATABASE).query_db(query)
        messages=[]
        for row in results:
            messages.append(cls(row))
        return messages
    
        #!======================validation message==================
    @staticmethod
    def validate_message(data):
        is_valid = True
        if len(data['email']) < 1:
            is_valid = False
            flash("Email is required", "email")

        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "email")
            is_valid = False
        
        if len(data['username']) < 1:
            is_valid = False
            flash("Enter your name please", "username")
        
        if len(data['subject']) < 10:
            is_valid = False
            flash("Invalid subject, must be greater than 10 characters!", "subject")
        
        if len(data['content']) < 10:
            is_valid = False
            flash("Invalid content, must be greater than 10 characters!", "content")
        
        return is_valid

        
        


        