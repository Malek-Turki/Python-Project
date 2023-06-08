from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import doctor_model
from flask_app.models import patient_model
from flask_app.models import consultation_model
from flask_app.models import patients_of_doctor





#!=============Display patients file Page ==============

@app.route('/doctor/patients')
def patients():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    data={
        'id':session['doctor_id']
    }
    # patients=patient_model.Patient.get_all_patient_by_last_consul(data)
    patients=patient_model.Patient.get_all_patient_by_doctor_id(data)
    print(f"********{patients}************")
    return render_template('patients_file.html',patients=patients)
#!=============Display add patient file Page ==============
@app.route('/patient/add')
def add_patient():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')

    return render_template("add_patient.html")
#!=============Action route to add patient by doctor Page ==============
@app.route('/patient/create', methods=[ 'POST'])
def add_patient_file():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    if not patient_model.Patient.validate_patient(request.form):
        return redirect('/patient/add')
    patient_id = patient_model.Patient.create_patient(request.form)
    data={
        'patient_id':patient_id,
        'doctor_id':session['doctor_id']
    }
    patients_of_doctor.Patients.save_patients_doctor(data)
    return redirect('/doctor/patients')
#!=============Display patient consultations file Page ==============
@app.route('/doctor/patient/<int:patient_id>')
def display_patient(patient_id):
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    patient = patient_model.Patient.get_patient_by_id({'id':patient_id})
    data={
        'patient_id':patient_id,
        'doctor_id':session['doctor_id']
    }
    patient_consult=consultation_model.Consultation.get_consultation(data)
    # print(f"********{patient_consult}************")
    return render_template('patient_file.html', patient=patient,patient_consult=patient_consult)


