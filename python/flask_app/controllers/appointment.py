from flask import render_template, redirect, session, request, flash
from flask_app import app
from flask_app.models import doctor_model
from flask_app.models import patient_model
from flask_app.models import appointment_model
#!=============action route to save appointment =============
@app.route('/doctor/appointment/create', methods=['POST'])
def save_appointment():
    if 'doctor_id' not in session:
        return redirect('/oh!doctors')
    # if not appointment_model.appointment.validate_appointment(request.form):
    #     return redirect("patient/appointment/create")
    data = {
        **request.form,
        'doctor_id': session['doctor_id'],
        'patient_id' : request.form['patient_id']
    }
    
    appointment_model.Appointment.create_appointment(data)
    return redirect("/doctor/appointments")