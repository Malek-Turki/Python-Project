from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import doctor_model
from flask_app.models import patient_model
from flask_app.models import consultation_model
#!=============Display consultation Page ==============
@app.route('/doctor/patient/consultation/<int:patient_id>')
def display_cons_file(patient_id):
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    data={
        'doctor_id': session['doctor_id'],
        'patient_id' : patient_id
    }
    all_consultations = consultation_model.Consultation.get_consultation(data)
    patient= patient_model.Patient.get_patient_by_id({'id':patient_id})
    return render_template("consultation.html",patient=patient,all_consultations=all_consultations)
#!=============action route to save consultation =============
@app.route('/patient/consultation/create', methods=['POST'])
def save_consultation():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    # if not consultation_model.Consultation.validate_consultation(request.form):
    #     return redirect("patient/consultation/create")
    data = {
        **request.form,
        'doctor_id': session['doctor_id'],
        'patient_id' : request.form['patient_id']
    }
    id=request.form['patient_id']
    consultation_id=consultation_model.Consultation.create_consultation(data)
    session['consultation_id']=consultation_id
    return redirect(f"/doctor/patient/{id}")
# #!=============action route to delete consultation =============
# @app.route('/patient/consultation/delete/<int:consultation_id>')
# def delete_patient_consultation(consultation_id):
#     if 'doctor_id' not in session:
#         return redirect('/oh!doctors')
#     data = {
#         'id': consultation_id
#     }
#     consultation_model.Consultation.delete_consultation(data)
#     id=request.form['patient_id']
#     return redirect(f"/doctor/patient/{id}")
# #!=============display route to update consultation =============
# @app.route('/consultation/edit/<int:consultation_id>')
# def edit(consultation_id):
#     if 'doctor_id' not in session:#to secure
#         return redirect('/oh!doctors')
#     consultation = consultation_model.Consultation.get_consultation_by_id({'id':consultation_id})
#     return render_template('edit_consultation.html',consultation=consultation)
# #!=============action route to update consultation =============
# @app.route('/patient/consultation/edit', methods=['POST'])
# def update_consultation():
#     if 'doctor_id' not in session:
#         return redirect('/oh!doctors')
#     if not consultation_model.Consultation.validate_consultation(request.form):
#         id = request.form['consultation_id']
#         return redirect(f"/patient/consultation/edit/{id}")
#     data = {
#         **request.form,
#         'doctor_id': session['doctor_id'],
#         'patient_id' : request.form['patient_id']
#     }
#     consultation_model.Consultation.update_consultation(data)
#     return redirect("/doctor/patient")

    







