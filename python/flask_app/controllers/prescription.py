from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import doctor_model
from flask_app.models import patient_model
from flask_app.models import prescription_model
from flask_app.models import consultation_model
from flask_app.models import medicines_model

import requests
#!=============action prescription Page ==============
@app.route('/prescrition/create', methods=['POST'])
def display_presct():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    patient= patient_model.Patient.get_patient_by_id({'id':request.form['patient_id']})
    session['patient_id'] = patient.id

    data = {
        'doctor_id': session['doctor_id'],
        'patient_id' : request.form['patient_id'],
        'consultation_id' : session['consultation_id']
    }
    prescription_id=prescription_model.Prescription.create_prescription(data)
    print(data, "**"*20)
    session['prescription_id']=prescription_id
    print(session['prescription_id'], "--"*20)
    # medicines=medicines_model.Medicine.get_medicine_by_prescription_id({'id':session['prescription_id']})
    return redirect("/prescription")
#!=============display prescription page =============
@app.route('/prescription')
def display_prescription():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    patient= patient_model.Patient.get_patient_by_id({'id':session['patient_id']})
    medicines=medicines_model.Medicine.get_medicine_by_prescription_id({'id':session['prescription_id']})
    return render_template("prescription.html",patient=patient,medicines=medicines)
    
# #!=============action route to add medicine to prescription =============
@app.route('/doctor/prescription/create', methods=['POST'])
def add_medicine():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    # if not prescription_model.prescription.validate_prescription(request.form):
    #     id=session['prescription_id']
    #     return redirect(f"/doctor/prescription/create/{id}")
    data = {
        **request.form,
        'prescription_id' : session['prescription_id']
    }
    medicines_model.Medicine.save_medicine(data)

    return redirect("/prescription")
# #!=============display route to print prescription =============
@app.route("/prescription/print")
def print_prescription():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    medicines=medicines_model.Medicine.get_medicine_by_prescription_id({'id':session['prescription_id']})
    return render_template("print.html")