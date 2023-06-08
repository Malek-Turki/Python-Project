from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
# from flask_app.models import 
class Medicine:

    def __init__(self,data):

        self.id = data['id']
        self.prescription_id = data['prescription_id']
        self.medicine_name = data['medicine_name']
        self.medicine_form = data['medicine_form']
        self.medicine_quantity = data['medicine_quantity']
        self.medicine_duration = data['medicine_duration']
        self.medicine_dosage = data['medicine_dosage']
        self.notes = data['notes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save_medicine(cls,data):
        query = """ INSERT INTO medicines_of_prescription (prescription_id,medicine_name,medicine_form,medicine_quantity,medicine_duration,medicine_dosage,notes)
        Values (%(prescription_id)s,%(medicine_name)s,%(medicine_form)s,%(medicine_quantity)s,%(medicine_duration)s,%(medicine_dosage)s,%(notes)s);"""
        return connectToMySQL(DATABASE).query_db(query,data) 

# #!===============get medicines by prescription id==================

    @classmethod
    def get_medicine_by_prescription_id(cls,data):
        query = "SELECT * FROM  medicines_of_prescription WHERE prescription_id=%(id)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(f"*******************{result}4444444444444444444444444444444444444444")
        return result

