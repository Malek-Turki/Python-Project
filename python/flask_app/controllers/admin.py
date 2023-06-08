from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import admin_model
from flask_app.models import message_model
from flask_app.models import doctor_model
from flask_app.models import payment_model
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)
#!=============Display Admin Page==============
@app.route('/oh!doctors/admin')
def log_admin():
    return render_template("login_admin.html")
#!==============Action route for Login with validation ======================
@app.route('/admin/login',methods=['POST'])
def login_admin():
    admin_from_db = admin_model.Admin.get_by_email(request.form)
    if not admin_from_db:
        flash("Invalid credentials !", "login")
        return redirect('/oh!doctors/admin')
    if not bcrypt.check_password_hash(admin_from_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid credentials !", "login")
        return redirect('/oh!doctors/admin')
    
    return redirect('/oh!doctors/admin/dashboard')
#!#!=============Display Admin registration Page==============
@app.route('/oh!doctors/admin/register')
def reg():
    return render_template("register_admin.html")
#!==============Action route for Register Amdin with validation ======================
@app.route('/admin/register',methods=['POST'])
def register_admin():
    #!verification de validation and hashed password befor saved in db
    if admin_model.Admin.validate_admin(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        #?new data after hashing password
        data = {
            **request.form,
            "password": pw_hash,
        }
        admin_id = admin_model.Admin.create_admin(data)

        #?saved admin id in session for the garde route and...
        session['admin_id']= admin_id

        return redirect('/oh!doctors/admin/dashboard')
    
    return redirect('/oh!doctors/admin/register')
#!=============Display Admin Dashboard Page==============
@app.route('/oh!doctors/admin/dashboard')
def dashboard_admin():
    all_doctors=doctor_model.Doctor.get_all_doctors()
    payments=payment_model.Payment.get_all_payments()
    print(f"????????????????????{payments}********************")
    subscriptions = []
    for pay in payments:
        start_date = pay['created_at']
        end_date = start_date + timedelta(days=365)
        print(end_date)
        subscriptions.append(end_date)
    print(f"????????????????????{subscriptions}********************")

    return render_template("admin_page.html",all_doctors=all_doctors,payments=payments, subscriptions = subscriptions )

#!=============Action route to send message to admin==============
@app.route('/contact_us', methods=['POST'])
def contact_us():
    # if message_model.Message.validate_message(request.form):
    #     return redirect('/oh!doctors')
    data = {
            **request.form,
    }
    message_model.Message.create_message(data)
    return redirect('/oh!doctors')

#!=============action route to logout==============
@app.route('/admin/logout')
def logout_admin():
    session.clear()
    return redirect('/oh!doctors/admin')


#!============valid doctors================================
@app.route('/oh!doctors/admin/valid_doctors')
def valid_doctors():
    is_valid = 1
    data = {"is_valid": is_valid}
    valid_doctors = doctor_model.Doctor.valide_doctor_by_admin(data)
    print(valid_doctors)
    return redirect('/oh!doctors/admin/dashboard')

#!============message admin================================
@app.route('/admin/message')
def message_admin():

    all_messages=message_model.Message.get_all_messages()

    return render_template('admin_message.html',all_messages=all_messages)



