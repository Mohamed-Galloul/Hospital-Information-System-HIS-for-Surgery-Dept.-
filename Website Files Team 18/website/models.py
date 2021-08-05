from website import db, login_manager,app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(email):
    user = Admin.query.get(str(email))
    if user == None:
        user = Doctor.query.get(str(email))
        if user == None:
            user = Patient.query.get(str(email))
    return user




#models.py
class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ssn = db.Column(db.Integer, unique=True ,nullable=False)
    name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.Enum('male','female'), nullable=False)
    address = db.Column(db.String(50), nullable=False)    
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Admin('{self.id}', '{self.ssn}', '{self.email}')"


class Doctor(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ssn = db.Column(db.Integer, unique=True ,nullable=False)
    name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.Enum('male','female'), nullable=False)
    address = db.Column(db.String(50), nullable=False)          
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    sub_department = db.Column(db.Enum('Cardiovascular_Surgery','Neurosurgery','Pediatric_Surgery','Bone_Surgery'),nullable=False)
    operations = db.relationship('Operation', backref='surgeon', lazy=True)

    def __repr__(self):
        return f"Doctor('{self.id}', '{self.ssn}', '{self.email}')"


class Patient(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ssn = db.Column(db.Integer, unique=True ,nullable=False)
    name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.Enum('male','female'), nullable=False)
    address = db.Column(db.String(50), nullable=False)          
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    medical_history = db.Column(db.String(50), nullable=False)    
    image_file = db.Column(db.String(50), nullable=False,default= 'default.jpg')
    operations = db.relationship('Operation', backref='ppatient', lazy=True)

    def __repr__(self):
        return f"Patient('{self.id}', '{self.ssn}', '{self.email}')"


class Operation(db.Model,UserMixin):
    code = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date ,nullable=False,default= '2021-01-15')
    start_time = db.Column(db.Time ,nullable=False,default= '00:00:00')
    end_time = db.Column(db.Time ,nullable=False,default= '01:00:00')
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def __repr__(self):
        return f"Operation('{self.code}', '{self.date}', '{self.start_time}','{self.end_time}')"

 
class Register(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20),unique=True ,nullable=False)
    email = db.Column(db.String(50),unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    registered_as = db.Column(db.Enum('Admin','Doctor','Patient'), nullable=False)

    def __repr__(self):
        return f"Register('{self.email}', '{self.registered_as}')"


class ContactUs(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50) ,nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text(150), nullable=False)


