from flask import Flask,render_template,redirect,request,session
app = Flask(__name__) 
app.secret_key = 'keep it secret, keep it safe'
DATABASE = "project_db_schema"