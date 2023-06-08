from flask_app import app
from flask_app.controllers import doctors
from flask_app.controllers import admin
from flask_app.controllers import patient
from flask_app.controllers import consultation
from flask_app.controllers import appointment
from flask_app.controllers import prescription
from flask_app.controllers import nurse






if __name__=="__main__":
    app.run(debug=True) 