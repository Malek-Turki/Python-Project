from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import doctor_model
from flask_app.models import consultation_model
from flask_app.models import appointment_model
from flask_app import DATABASE

class Patient:
    def __init__(self,data):
        self.id=data["id"]
        self.first_name=data['first_name']
        self.last_name=data['last_name']
        self.birth_date = data['birth_date']
        self.gender=data['gender']
        self.address=data['address']
        self.phone=data['phone']
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.patient_consul=[]
        self.patient_doc=[]
        self.patient_appoint=[]

#     #?===============Create Patient=================#
    @classmethod
    def create_patient(cls,data):
        query="""
        INSERT INTO patients (first_name,last_name,birth_date,gender,address,phone)
        VALUES (%(first_name)s,%(last_name)s,%(birth_date)s,%(gender)s,%(address)s,%(phone)s)"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
#     #?=============get patient by  id================
    @classmethod
    def get_patient_by_id(cls, data):
        query = """SELECT * FROM patients WHERE id = %(id)s"""
        result= connectToMySQL(DATABASE).query_db(query,data)
        if len(result)<1:
            return False
        return cls(result[0])
    
    #?=============get all patients by  doctor id================
    @classmethod
    def get_all_patient(cls,data):
        query = """SELECT * FROM patients
            Left join consultations on consultations.patient_id = patients.id
            Left join doctors on doctors.id = consultations.doctor_id
            WHERE doctor_id = %(id)s"""
        results= connectToMySQL(DATABASE).query_db(query,data)
        # print(results)
        if len(results)<1:
            return results
        these_patients=[]
        
        for row in results:
            this_patient = cls(row)
            consultation_data = {
                'id': row['consultations.id'],
               'symptoms' :row['symptoms'],
                'analysis' :row['analysis'],
                'created_at': row['consultations.created_at'],
                'updated_at': row['consultations.updated_at']
            }
            this_patient.patient_consul.append(consultation_data)

    
#     #?=============edit patient================
#     @classmethod
#     def edit_patient(cls,data):
#         query="""UPDATE patients SET first_name = %(first_name)s,last_name = %(last_name)s,birth_date = %(birth_date)s,gender = %(gender)s,address = %(address)s WHERE id = %(id)s"""
#         result = connectToMySQL(DATABASE).query_db(query,data)
#         return result

    #?=============delete patient
    @classmethod
    def delete_patient(cls,data):
        query="""DELETE FROM patients
        Left join patients_of_doctor on patients_of_doctor.patient_id = patients.id
        Left join doctors on doctors.id = patients_of_doctor.doctor_id
        WHERE doctor_id = %(doctor_id)s and patient_id = %(id)s;"""
        result = connectToMySQL(DATABASE).query_db(query,data)
        return result
    
    #?=============get all patient of a doctor================
    @classmethod
    def get_all_patient_by_doctor_id(cls,data):
        query = """SELECT * FROM patients
            Left join patients_of_doctor on patients_of_doctor.patient_id = patients.id
            Left join doctors on doctors.id = patients_of_doctor.doctor_id
            WHERE doctor_id = %(id)s"""
        results= connectToMySQL(DATABASE).query_db(query,data)
        print(results)
        if len(results)<1:
            return results
        these_patients=[]
        
        for row in results:
            this_patient = cls(row)
            doctor_data = {
                'id': row['doctors.id'],
                'first_name':row['doctors.first_name'],
                'last_name':row['doctors.last_name'],
                'address':row['doctors.address'],
                'serial_number':row['serial_number'],
                'photo':row['photo'],
                'speciality':row['speciality'],
                'phone':row['doctors.phone'],
                'email':row['email'],
                'is_valid':row['is_valid'],
                'password':row['password'],
                'created_at':row['doctors.created_at'],
                'updated_at':row['doctors.updated_at']
            }
            this_doctor = doctor_model.Doctor(doctor_data)
            this_patient.patient_doc=this_doctor
            these_patients.append(this_patient)
            

        return these_patients
    
    @classmethod
    def get_all_patient_by_last_consul(cls,data):
        query = """SELECT * FROM patients
            Left join consultations on consultations.patient_id = patients.id
            Left join doctors on doctors.id = consultations.doctor_id
            WHERE doctor_id = %(id)s 
            ORDER BY consultations.id DESC limit 1"""
        results= connectToMySQL(DATABASE).query_db(query,data)
        print(f"******************{results}*********************************")
        if len(results)<1:
            return results
        these_patients=[]
        
        for row in results:
            this_patient = cls(row)
            consultation_data = {
                'id': row['consultations.id'],
                'symptoms' :row['symptoms'],
                'analysis' :row['analysis'],
                'conclusion' :row['conclusion'],
                'created_at' :row['consultations.created_at'],
                'updated_at' : row['consultations.updated_at'],
                'doctor_id':row['doctor_id'],
                'patient_id' :row['patient_id']
            }
            this_consultation = consultation_model.Consultation(consultation_data)
            this_patient.patient_consul=this_consultation
            doctor_data = {
                'id': row['doctors.id'],
                'first_name':row['doctors.first_name'],
                'last_name':row['doctors.last_name'],
                'address':row['doctors.address'],
                'serial_number':row['serial_number'],
                'photo':row['photo'],
                'speciality':row['speciality'],
                'phone':row['doctors.phone'],
                'email':row['email'],
                'is_valid':row['is_valid'],
                'password':row['password'],
                'created_at':row['doctors.created_at'],
                'updated_at':row['doctors.updated_at']
            }
            this_doctor = doctor_model.Doctor(doctor_data)
            this_patient.patient_doc=this_doctor
            these_patients.append(this_patient)
            print(these_patients)

        return these_patients
    

    #?=============get all patient by appointments================
    @classmethod
    def get_all_appointments_patient(cls,data):
        query = """SELECT * FROM patients
            Left join appointments on appointments.patient_id = patients.id
            Left join doctors on doctors.id = appointments.doctor_id
            WHERE doctor_id = %(id)s"""
        results= connectToMySQL(DATABASE).query_db(query,data)
        # print(results)
        if len(results)<1:
            return results
        these_patients_appointments=[]
        
        for row in results:
            this_patient = cls(row)
            appointment_data = {
                'id': row['appointments.id'],
                'motif' :row['motif'],
                'date' :row['date'],
                'created_at' :row['appointments.created_at'],
                'updated_at' : row['appointments.updated_at'],
                'doctor_id':row['doctor_id'],
                'patient_id' :row['patient_id']
            }
            this_appointment = appointment_model.Appointment(appointment_data)
            this_patient.patient_appoint=this_appointment
            doctor_data = {
                'id': row['doctors.id'],
                'first_name':row['doctors.first_name'],
                'last_name':row['doctors.last_name'],
                'address':row['doctors.address'],
                'serial_number':row['serial_number'],
                'photo':row['photo'],
                'speciality':row['speciality'],
                'phone':row['doctors.phone'],
                'email':row['email'],
                'is_valid':row['is_valid'],
                'password':row['password'],
                'created_at':row['doctors.created_at'],
                'updated_at':row['doctors.updated_at']
            }
            this_doctor = doctor_model.Doctor(doctor_data)
            this_patient.patient_doc=this_doctor
            these_patients_appointments.append(this_patient)
            print(these_patients_appointments[0].patient_appoint)

        return these_patients_appointments
#     #!================validation patient================
    @staticmethod
    def validate_patient(data):
        is_valid = True
        if len(data['first_name']) < 2:
            is_valid = False
            flash("Invalid first name, must be greater than 2 characters!", "first_name")

        if len(data['last_name']) < 2:
            is_valid = False
            flash("Invalid last name, must be greater than 2 characters!", "last_name")
        
        if len(data['birth_date'])=="":
            is_valid = False
            flash("Invalid birth date, must be not blank!!", "birth_date")
        
        if len(data['gender']) < 1:
            is_valid = False
            flash("Invalid gender, must Choose gender!", "gender")
        
        if len(data['address']) < 8:
            is_valid = False
            flash("Invalid address, must be greater than 8 characters!", "address")
        
        if len(data['phone']) < 8:
            is_valid = False
            flash("Invalid phone number, must be 8 numbers!", "phone")

        
        
        return is_valid




    


