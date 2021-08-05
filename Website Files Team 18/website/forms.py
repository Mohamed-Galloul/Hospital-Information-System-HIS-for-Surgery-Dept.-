from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                    TextAreaField, SelectField, IntegerField,DateTimeField,DateField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from website.models import Register,Admin,Patient,Doctor,Operation




# forms.py
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    registeredas= SelectField('Register as:',
                        validators=[DataRequired()],
                        choices = [('Admin', 'admin'), ('Doctor', 'doctor'),('Patient', 'patient')])
    submit = SubmitField('Sign Up')

    #check that email and username were not taken before 
    def validate_username(self, username):
        user = Register.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = Register.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ContactUsForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


class AddDoctorForm (FlaskForm):
    id = IntegerField("ID",
                            validators = [DataRequired()])    
    ssn = IntegerField("SSN",
                            validators = [DataRequired()])
    name = StringField("Name", 
                            validators = [DataRequired() , Length (min = 2 , max = 50 )])
    sex= SelectField('Sex',
                        validators=[DataRequired()],
                        choices = [('male', 'Male'), ('female', 'Female')])
    address = StringField ("Address",
                         validators = [DataRequired(), Length(min = 2 , max = 50)])
    age = IntegerField("Age",
                            validators = [DataRequired()])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    phone = IntegerField("Phone",
                            validators = [DataRequired()])    
    sub_department= SelectField('Sub-Department',
                        validators=[DataRequired()],
                         choices = [('Cardiovascular_Surgery','Cardiovascular Surgery'),
                            ('Neurosurgery','Neurosurgery'),
                            ('Pediatric_Surgery','Pediatric Surgery'),
                            ('Bone_Surgery','Bone Surgery')])
    submit = SubmitField("Add Doctor")    

    def validate_id (self, id):
        id = Doctor.query.filter_by(id=id.data).first()
        if id :
            raise ValidationError("This ID is already taken")

    def validate_ssn (self, ssn):
        ssn = Doctor.query.filter_by(ssn = ssn.data).first()
        if ssn :
            raise ValidationError("This SSN is already exist")
        
    def validate_email (self, email) :
        email = Doctor.query.filter_by(email = email.data).first()
        if  email :
            raise ValidationError("This email is taken. Please choose a different one.")


# class UpdateDoctorForm(FlaskForm,idd):
#     id = IntegerField("ID",
#                             validators = [DataRequired()])    
#     ssn = IntegerField("SSN",
#                             validators = [DataRequired()])
#     name = StringField("Name", 
#                             validators = [DataRequired() , Length (min = 2 , max = 50 )])
#     sex= SelectField('Sex',
#                         validators=[DataRequired()],
#                         choices = [('male', 'Male'), ('female', 'Female')])
#     address = StringField ("Address",
#                          validators = [DataRequired(), Length(min = 2 , max = 50)])
#     age = IntegerField("Age",
#                             validators = [DataRequired()])
#     email = StringField('Email',
#                             validators=[DataRequired(), Email()])
#     phone = IntegerField("Phone",
#                             validators = [DataRequired()])    
#     sub_department= SelectField('Sub-Department',
#                         validators=[DataRequired()],
#                          choices = [('Cardiovascular_Surgery','Cardiovascular Surgery'),
#                             ('Neurosurgery','Neurosurgery'),
#                             ('Pediatric_Surgery','Pediatric Surgery'),
#                             ('Bone_Surgery','Bone Surgery')])
#     submit = SubmitField("Update Doctor") 

#     doctor = Doctor.query.get(id=idd) 

#     def validate_username(self, id):
#         if id.data != doctor.id:
#             user = doctor.query.filter_by(id=id.data).first()
#             if user:
#                 raise ValidationError('That ID is taken. Please choose a different one.')

#     def validate_username(self, ssn):
#         if ssn.data != doctor.ssn:
#             user = doctor.query.filter_by(ssn=ssn.data).first()
#             if user:
#                 raise ValidationError('That SSN is taken. Please choose a different one.')

#     def validate_email(self, email):
#         if email.data != doctor.email:
#             user = doctor.query.filter_by(email=email.data).first()
#             if user:
#                 raise ValidationError('That Email is taken. Please choose a different one.')   



class AddPatientForm (FlaskForm):
    id = IntegerField("ID",
                            validators = [DataRequired()])    
    ssn = IntegerField("SSN",
                            validators = [DataRequired()])
    name = StringField("Name", 
                            validators = [DataRequired() , Length (min = 2 , max = 50 )])
    sex= SelectField('Sex',
                        validators=[DataRequired()],
                        choices = [('male', 'Male'), ('female', 'Female')])
    address = StringField ("Address",
                         validators = [DataRequired(), Length(min = 2 , max = 50)])
    age = IntegerField("Age",
                            validators = [DataRequired()])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    phone = IntegerField("Phone",
                            validators = [DataRequired()])    

    medical_history = StringField ("Medical History",
                         validators = [DataRequired(), Length(min = 2 , max = 50)])

    image_file = FileField('Select Patient Scan ', validators=[FileAllowed(['jpg', 'png']), Optional()])    

    submit = SubmitField("Add Patient")    

    def validate_id (self, id):
        id = Patient.query.filter_by(id=id.data).first()
        if id :
            raise ValidationError("This ID is already taken")

    def validate_ssn (self, ssn):
        ssn = Patient.query.filter_by(ssn = ssn.data).first()
        if ssn :
            raise ValidationError("This SSN is already exist")
        
    def validate_email (self, email) :
        email = Patient.query.filter_by(email = email.data).first()
        if  email :
            raise ValidationError("This email is taken. Please choose a different one.")


class UploadPatientScanForm (FlaskForm):

    image_file = FileField('Select Patient Scan ', validators=[FileAllowed(['jpg', 'png'])])    
    submit = SubmitField("Upload Patient Scan")  




class AddAdminForm (FlaskForm):
    id = IntegerField("ID",
                            validators = [DataRequired()])    
    ssn = IntegerField("SSN",
                            validators = [DataRequired()])
    name = StringField("Name", 
                            validators = [DataRequired() , Length (min = 2 , max = 50 )])
    sex= SelectField('Sex',
                        validators=[DataRequired()],
                        choices = [('male', 'Male'), ('female', 'Female')])
    address = StringField ("Address",
                         validators = [DataRequired(), Length(min = 2 , max = 50)])
    age = IntegerField("Age",
                            validators = [DataRequired()])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    phone = IntegerField("Phone",
                            validators = [DataRequired()])    

    submit = SubmitField("Add Admin")    

    def validate_id (self, id):
        id = Admin.query.filter_by(id=id.data).first()
        if id :
            raise ValidationError("This ID is already taken")

    def validate_ssn (self, ssn):
        ssn = Admin.query.filter_by(ssn = ssn.data).first()
        if ssn :
            raise ValidationError("This SSN is already exist")
        
    def validate_email (self, email) :
        email = Admin.query.filter_by(email = email.data).first()
        if  email :
            raise ValidationError("This email is taken. Please choose a different one.")




class AddOperationForm (FlaskForm):
    code = IntegerField("Code",
                            validators = [DataRequired()])    
    location = StringField("Location", 
                            validators = [DataRequired() , Length (min = 2 , max = 50 )])
    date = DateField("Date",format='%Y-%m-%d',validators = [Optional()])
    
    start_time = DateTimeField("Start Time",format='%H-%M-%S',validators = [Optional()])
    
    end_time = DateTimeField("End Time",format='%H-%M-%S',validators = [Optional()])

    patient_id = IntegerField("Patient ID", 
                            validators = [DataRequired()])
    doctor_id = IntegerField("Doctor ID", 
                            validators = [DataRequired()])

    submit = SubmitField("Add Operation")    

    def validate_code (self, code):
        code = Operation.query.filter_by(code=code.data).first()
        if code :
            raise ValidationError("This Code is already taken for another operation")



