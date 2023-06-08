from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import doctor_model
from flask_app.models import nurse_model
from flask_app.models import patient_model
from flask_app.models import payment_model
from base64 import b64encode
import datetime 


from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)

@app.route('/')
def index():
    return redirect("/oh!doctors")
#!=============Display Index Page==============
@app.route('/oh!doctors')
def home():
    
    return render_template("index.html")


#!=============Action route to contact admin from the index Page==============
@app.route('/doctors/contact_us',methods=['POST'])
def contact_admin():
    
    return redirect("index.html")
#!=============Display Doctors registration Page==============
@app.route('/doctors/register')
def register_doc():
    return render_template("register.html")


#!==============Action Route for registration=================
@app.route ('/doctor/register', methods=['POST'])
def register():
    #!verification de validation and hashed password befor saved in db
    if doctor_model.Doctor.validate_doctor(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        #?new data after hashing password
        data = {
            **request.form,
            "password": pw_hash,
        }
    #!verification de validation doctor SMN befor saved in db
    
        doctor_id = doctor_model.Doctor.create_doctor(data)
        #?saved doctor id in session for the garde route and...
        session['doctor_id']= doctor_id
        return redirect('/oh!doctors')
    return redirect('/doctors/register')
#!=============Display Doctors login Page==============
@app.route('/doctors/login')
def login_doc():
    return render_template("login_doctor.html")
#!==============Action route for Login with validation (SMN + password) ======================
@app.route('/doctor/login',methods=['POST'])
def login():
    doctor_from_db = doctor_model.Doctor.get_by_email(request.form)

    if not doctor_from_db:
        flash("Invalid credentials !", "log")
        return redirect('/doctors/login')
    if not bcrypt.check_password_hash(doctor_from_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid credentials !", "log")
        return redirect('/doctors/login')
    if doctor_from_db.is_valid==0:
        flash("wait until yor account is validated!", "log")
        return redirect('/doctors/login')
    session['doctor_id']=doctor_from_db.id
    return redirect('/doctor/dashboard')
#!=============Display Doctors doctor Dashboard Page==============
@app.route('/doctor/dashboard')
def dashboard():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    # doctor_info = doctor_model.Doctor.get_by_id(doctor_id)
    return render_template("doctor_dashboard.html")


#!=============Display appointments file Page ==============

@app.route('/doctor/appointments')
def doc_appointemnts():
    data={

        'id':session['doctor_id']
    }
    all_appointments=patient_model.Patient.get_all_appointments_patient(data)
    print(f"********{all_appointments}************")
    date = datetime.datetime.now()
    
    return render_template('appointments.html',all_appointments=all_appointments, datetime=date)

#!=============Display route for appointment=================
@app.route('/appointment/add')
def appoint():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    all_patients=patient_model.Patient.get_all_patient_by_doctor_id({'id': session['doctor_id']})
    return render_template("add_appointment.html",all_patients=all_patients)

#!=============Display route  for profile page=================
@app.route('/doctor/profile')
def profile():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    # all_patients=patient_model.Patient.get_all_patient_by_last_consul({'id': session['doctor_id']})
    doctor=doctor_model.Doctor.get_by_id({'id': session['doctor_id']})
    # image_data = b64encode(doctor.photo).decode("utf-8")
    
    return render_template("profile.html",doctor=doctor)
#!=============Display route  for edit profile page=================
@app.route('/doctor/edit/profile/<int:doctor_id>')
def edit_profile(doctor_id):
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    # all_patients=patient_model.Patient.get_all_patient_by_last_consul({'id': session['doctor_id']})
    doctor=doctor_model.Doctor.get_by_id({'id': doctor_id})
    return render_template("edit_profile.html",doctor=doctor)

#!==============Action route for edit profile ======================
@app.route('/edit/profile',methods=['POST'])
def edit_prof():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    # all_patients=patient_model.Patient.get_all_patient_by_last_consul({'id': session['doctor_id']})
   
    doctor_model.Doctor.update_doctor_profile(request.form)
    return redirect('/doctor/profile')

#!=============display route for nurses accounts=================
@app.route('/doctor/nurses')
def nurses():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    all_nurses=nurse_model.Nurse.get_all_nurse_account({'id': session['doctor_id']})
    return render_template("new_nurse.html",all_nurses=all_nurses)

#!=============action route for create nurse account=================
@app.route('/doctor/nurse/create',methods=['POST'])
def create_nurse():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    data = {
            **request.form,
            'doctor_id':session['doctor_id']
    }
    nurse_model.Nurse.create_nurse_account(data)
    return redirect('/doctor/nurses')
#!=============display route for Payment=================
@app.route('/doctor/payment')
def payment():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    doctor=doctor_model.Doctor.get_by_id({'id': session['doctor_id']})
    return render_template("payment.html",doctor=doctor)
#!=============action route to fix payment=================
@app.route('/doctor/payment/fix',methods=['POST'])
def fix_payment():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    data = {
            **request.form,
            'doctor_id':session['doctor_id']
    }
    payment_model.Payment.fix_payment(data)
    return redirect('/doctor/profile')

#!=============delete patient================
@app.route('/doctor/delete/patient/<int:patient_id>')
def delete_patient(patient_id):
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    data={
        'id': patient_id,
        'doctor_id':session['doctor_id']
    }
    patient_model.Patient.delete_patient(data)
    return redirect('/doctor/patients')

















#!=============Action route for logout=================
@app.route('/doctor/logout')
def logout():
    session.clear()
    return redirect('/oh!doctors')




