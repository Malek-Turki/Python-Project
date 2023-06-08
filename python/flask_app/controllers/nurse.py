from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import doctor_model
from flask_app.models import nurse_model
from flask_app.models import patient_model
from flask_app.models import patients_of_doctor
from flask_app.models import appointment_model
import datetime


#!=============Display route to login nurse   Page==============
@app.route('/assistants/login')
def add_nurse():
    
    return render_template("login_nurse.html")
#!==============Action route for Login with validation (code) ======================
@app.route('/assistant/login',methods=['POST'])
def login_nurse():
    nurse_in_db=nurse_model.Nurse.get_nurse_by_code(request.form)
    if not nurse_in_db:
        flash("Invalid credentials !", "log")
        return redirect('/assistants/login')
    session['nurse_doctor_id']=nurse_in_db.doctor_id
    return redirect('/nurse/dashboard')

#!=============Display appointments file Page ==============

@app.route('/nurse/dashboard')
def appointemnts_for_nurse_dashboard():
    data={

        'id':session['nurse_doctor_id']
    }
    all_appointments=patient_model.Patient.get_all_appointments_patient(data)
    print(f"********{all_appointments}************")
    date = datetime.datetime.now()
    return render_template('appointment_nurse.html',all_appointments=all_appointments,datetime=date)

#!=============Display route for appointment=================
@app.route('/nurse/appointment/add')
def appoint_by_nurse():
    all_patients=patient_model.Patient.get_all_patient_by_doctor_id({'id': session['nurse_doctor_id']})
    return render_template("add_appointment_by_nurse.html",all_patients=all_patients)
#!==============Action route to add appointment by nurse =================
@app.route('/nurse/appointment/create', methods=['POST'])
def save_appointment_by_nurse():
    # if not appointment_model.appointment.validate_appointment(request.form):
    #     return redirect("patient/appointment/create")
    data = {
        **request.form,
        'doctor_id': session['nurse_doctor_id'],
        'patient_id' : request.form['patient_id']
    }
    
    appointment_model.Appointment.create_appointment(data)
    return redirect("/nurse/dashboard")



#!=============Display add patient file Page ==============
@app.route('/nurse/patient/add')
def add_patient_by_nurse():
    return render_template("add_patient_by_nurse.html")
#!==============Action route to add patient by nurse =================
@app.route('/nurse/patient/create', methods=[ 'POST'])
def create_patient_by_nurse():
    patient_id = patient_model.Patient.create_patient(request.form)
    data={
        'patient_id':patient_id,
        'doctor_id':session['nurse_doctor_id']
    }
    patients_of_doctor.Patients.save_patients_doctor(data)
    return redirect('/nurse/dashboard')
#!=============Action route for logout=================
@app.route('/nurse/logout')
def nurse_logout():
    session.clear()
    return redirect('/oh!doctors')




