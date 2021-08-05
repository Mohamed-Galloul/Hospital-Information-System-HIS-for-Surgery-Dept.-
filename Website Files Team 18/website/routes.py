import os
# import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from website import app, db
from website.forms import (RegistrationForm, LoginForm, ContactUsForm,
                           AddDoctorForm, AddPatientForm, UploadPatientScanForm,
                           AddAdminForm, AddOperationForm)

from website.models import Register, ContactUs, Admin, Patient, Doctor, Operation
from flask_login import login_user, current_user, logout_user, login_required


# routes.py
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Register(username=form.username.data, email=form.email.data,
                        password=form.password.data, registered_as=form.registeredas.data)
        db.session.add(user)
        db.session.commit()
        flash(
            f'Account has been created for {form.username.data} as an {form.registeredas.data} You are now able to log in!', 'success')
        return redirect(url_for('home'))  # login

    return render_template('register.html', title='Register', form=form)


@app.route("/contact-us", methods=['GET', 'POST'])
def contact_us():
    form = ContactUsForm()
    if form.validate_on_submit():
        message = ContactUs(name=form.name.data, email=form.email.data,
                            phone=form.phone.data, message=form.message.data)
        db.session.add(message)
        db.session.commit()
        flash('Thank you for contacting with us your request/message has been reported', 'success')
        return redirect(url_for('home'))
    return render_template('contact_us.html', title='Contact Us', form=form)




# admin login
@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            if user.registered_as == 'Admin':
                wanted_user = Admin.query.filter_by(email=user.email).first()

                login_user(wanted_user, remember=form.remember.data)
                flash(
                    f'Successful Login for {user.username} as an {user.registered_as}', 'success')

                return redirect(url_for('admin'))


            else:
                flash(
                    'This user is not registered as an Admin please choose your correct login path', 'danger')
                return redirect(url_for('home'))

        else:
            flash('Unsuccessful Login. Please check email and password', 'danger')
    return render_template('login_all.html', title='Login Admin', form=form, USER='ADMIN')


@login_required
@app.route("/admin")
def admin():
    return render_template('admin.html', title='Admin', USER='ADMIN')


# doctor login
@app.route("/login-doctor", methods=['GET', 'POST'])
def login_doctor():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            if user.registered_as == 'Doctor':
                wanted_user = Doctor.query.filter_by(email=user.email).first()


                login_user(wanted_user, remember=form.remember.data)
                flash(
                    f'Successful Login for {user.username} as a {user.registered_as}', 'success')

                return render_template( 'doctor_account.html', doctor = wanted_user, title='Login Doctor', form=form, USER='DOCTOR')

            else:
                flash(
                    'This user is not registered as an Doctor please choose your correct login path', 'danger')
                return redirect(url_for('home'))

        else:
            flash('Unsuccessful Login. Please check email and password', 'danger')
    return render_template('login_all.html', title='Login Doctor', form=form, USER='DOCTOR')


@login_required
@app.route("/doctor-account")
def doctor_account(doctor):
    return render_template('doctor_account.html', doctor=doctor, title='Doctor Account', USER='DOCTOR')


# patient login
@app.route("/login-patient", methods=['GET', 'POST'])
def login_patient():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            if user.registered_as == 'Patient':
                wanted_user = Patient.query.filter_by(email=user.email).first()

                login_user(wanted_user, remember=form.remember.data)
                flash(f'Successful Login for {user.username} as a {user.registered_as}', 'success')


                return render_template( 'patient_account.html', patient = wanted_user, title='Login Patient', form=form, USER='PATIENT')

            else:
                flash(
                    'This user is not registered as an Patient please choose your correct login path', 'danger')
                return redirect(url_for('home'))

        else:
            flash('Unsuccessful Login. Please check email and password', 'danger')
    return render_template('login_all.html', title='Login Patient', form=form, USER='PATIENT')


@login_required
@app.route("/patient-account", methods=['GET', 'POST'])
def patient_account(patient):
    return render_template('patient_account.html', patient = patient, title='Patient Account', USER='PATIENT')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



# admin main page
# admin deals with doctor records
@login_required
@app.route("/admin/veiw-doctors")
def admin_view_doctors():
    all_doctors = Doctor.query.all()
    return render_template("admin_view_doctors.html", all_doctors=all_doctors, USER='ADMIN')


@login_required
@app.route("/admin/add-new-doctor", methods=['GET', 'POST'])
def admin_add_new_doctor():
    form = AddDoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(id=form.id.data, ssn=form.ssn.data, name=form.name.data,
                        sex=form.sex.data, address=form.address.data, age=form.age.data,
                        email=form.email.data, phone=form.phone.data,
                        sub_department=form.sub_department.data)
        db.session.add(doctor)
        db.session.commit()
        flash(
            f'{doctor.name} record has been added to doctors table in the database!', 'success')
        return redirect(url_for('admin_view_doctors'))
    return render_template("admin_add_new_doctor.html", form=form,
                           legend="Add New Doctor", title="Add New Doctor", USER='ADMIN')


@login_required
@app.route("/admin/veiw-doctor-operations/<int:id>")
def admin_view_doctor_operations(id):
    doctor = Doctor.query.filter_by(id=id).first()
    return render_template("admin_view_doctor_operations.html", title='Veiw Doctor Operations',
                           doctor=doctor, USER='ADMIN')


# @login_required
# @app.route('admin/update-doctor', methods = ['GET', 'POST'])
# def admin_update_doctor(idd):
#     form = UpdateDoctorForm(idd)

#     if request.method == 'POST':
#         doctor_data = Doctor.query.get(id)
#         doctor_data.id = form.id.data
#         doctor_data.ssn = form.ssn.data
#         doctor_data.name = form.name.data
#         doctor_data.sex = form.sex.data
#         doctor_data.address = form.address.data
#         doctor_data.age = form.age.data
#         doctor_data.email = form.email.data
#         doctor_data.phone = form.phone.data
#         doctor_data.sub_department = form.sub_department.data

#         db.session.commit()
#         flash(f'Doctor {doctor_data.name} account has been successfully updated!', 'success')
#         return redirect(url_for('admin_view_doctors'))

#     elif request.method == 'GET':
#             form.id.data = doctor_data.id
#             form.ssn.data = doctor_data.ssn
#             form.name.data = doctor_data.name
#             form.sex.data = doctor_data.sex
#             form.address.data = doctor_data.address
#             form.age.data = doctor_data.age
#             form.email.data = doctor_data.email
#             form.phone.data = doctor_data.phone
#             form.sub_department.data = doctor_data.sub_department

#     return render_template("admin_add_new_doctor.html", title = 'Update Doctor',
#                         USER = 'ADMIN')


@login_required
@app.route("/admin/delete-doctor/<int:id>", methods=['GET', 'POST'])
def admin_delete_doctor(id):
    doctor = Doctor.query.filter_by(id=id).first()
    for operation in doctor.operations:
        db.session.delete(operation)
        db.session.commit()

    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for('admin_view_doctors'))


# admin deals with patient records
@login_required
@app.route("/admin/veiw-patients")
def admin_view_patients():
    all_patients = Patient.query.all()
    return render_template("admin_view_patients.html", all_patients=all_patients, USER='ADMIN')


@login_required
@app.route("/admin/add-new-patient", methods=['GET', 'POST'])
def admin_add_new_patient():
    form = AddPatientForm()
    if form.validate_on_submit():
        patient = Patient(id=form.id.data, ssn=form.ssn.data, name=form.name.data,
                          sex=form.sex.data, address=form.address.data, age=form.age.data,
                          email=form.email.data, phone=form.phone.data,
                          medical_history=form.medical_history.data, image_file=form.image_file.data)

        db.session.add(patient)
        db.session.commit()
        flash(f' {patient.name} has been add to patients table in database please upload patient scan !', 'success')
        return redirect(url_for('admin_view_patients', id=patient.id))
    return render_template("admin_add_new_patient.html", form=form,
                           title="Add New Patient", USER='ADMIN')



@login_required
@app.route("/admin/upload-patient-scan/<int:id>/", methods=['GET', 'POST'])
def admin_upload_patient_scan(id):
    patient = Patient.query.filter_by(id=id).first()
    form = UploadPatientScanForm()
    if form.validate_on_submit():
        if form.image_file.data:

            picture_file = save_picture(form.image_file.data)
            patient.image_file = picture_file

        db.session.commit()
        flash(
            f'{patient.image_file} Scan File has been uploaded for {patient.name}!', 'success')
        return redirect(url_for('admin_view_patients'))
    image_file = url_for(
        'static', filename='patients_scans/' + patient.image_file)
    return render_template('admin_upload_patient_scan.html', title='Upload Patient Scan', image_file=image_file, form=form, USER='ADMIN')


def save_picture(form_image_file):
    f_name, f_ext = os.path.splitext(form_image_file.filename)
    picture_fn = f_name + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/patients_scans', picture_fn)
    form_image_file.save(picture_path)
    flash(f'{form_image_file}', 'danger')

    return picture_fn


@login_required
@app.route("/admin/veiw-patient-operations/<int:id>")
def admin_view_patient_operations(id):
    patient = Patient.query.filter_by(id=id).first()
    return render_template("admin_view_patient_operations.html", title='Veiw Patient Operations',
                           patient=patient, USER='ADMIN')


@login_required
@app.route("/admin/delete-patient/<int:id>", methods=['GET', 'POST'])
def admin_delete_patient(id):
    patient = Patient.query.filter_by(id=id).first()
    for operation in patient.operations:
        db.session.delete(operation)
        db.session.commit()

    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('admin_view_patients'))




# #admin deals with OPERATION records
@login_required
@app.route("/admin/veiw-admins")
def admin_view_admins():
    all_admins = Admin.query.all()
    return render_template("admin_view_admins.html", all_admins=all_admins, USER='ADMIN')


@login_required
@app.route("/admin/add-new-admin", methods=['GET', 'POST'])
def admin_add_new_admin():
    form = AddAdminForm()
    if form.validate_on_submit():
        admin = Admin(id=form.id.data, ssn=form.ssn.data, name=form.name.data,
                      sex=form.sex.data, address=form.address.data, age=form.age.data,
                      email=form.email.data, phone=form.phone.data,
                      )
        db.session.add(admin)
        db.session.commit()
        flash(
            f'{admin.name} record has been added to admins table in the database!', 'success')
        return redirect(url_for('admin_view_admins'))
    return render_template("admin_add_new_admin.html", form=form,
                           legend="Add New Admin", title="Add New Admin", USER='ADMIN')


@login_required
@app.route("/admin/delete-admin/<int:id>", methods=['GET', 'POST'])
def admin_delete_admin(id):
    admin = Admin.query.filter_by(id=id).first()

    db.session.delete(admin)
    db.session.commit()
    return redirect(url_for('admin_view_admins'))




# #admin deals with Operations records
@login_required
@app.route("/admin/veiw-operations")
def admin_view_operations():
    all_operations = Operation.query.all()
    return render_template("admin_view_operations.html", all_operations=all_operations, USER='ADMIN')


@login_required
@app.route("/admin/add-new-operation", methods=['GET', 'POST'])
def admin_add_new_operation():
    form = AddOperationForm()
    if form.validate_on_submit():
        patient = Patient.query.filter_by(id=form.patient_id.data).first()
        doctor = Doctor.query.filter_by(id=form.doctor_id.data).first()

        if patient and doctor:
            operation = Operation(code=form.code.data, location=form.location.data, date=form.date.data,
                                  start_time=form.start_time.data, end_time=form.end_time.data,
                                  doctor_id=form.doctor_id.data, patient_id=form.patient_id.data
                                  )
            db.session.add(operation)
            db.session.commit()
            flash(
                f'operation record has been added for patient id {operation.patient_id} and doctor id {operation.doctor_id} to operations table in the database!', 'success')
            return redirect(url_for('admin_view_operations'))
        else:
            flash(
                'Please make sure that patient and doctor IDs are registered first', 'danger')
            return redirect(url_for('admin'))
    return render_template("admin_add_new_operation.html", form=form,
                           legend="Add New Operation", title="Add New Operation", USER='ADMIN')


@login_required
@app.route("/admin/veiw-operation_details/<int:code>")
def admin_view_operation_details(code):
    operation = Operation.query.filter_by(code=code).first()
    return render_template("admin_view_operation_details.html", title='Veiw Operation Details',
                           operation=operation, USER='ADMIN')


@login_required
@app.route("/admin/delete-operation/<int:code>", methods=['GET', 'POST'])
def admin_delete_operation(code):
    operation = Operation.query.filter_by(code=code).first()

    db.session.delete(operation)
    db.session.commit()
    return redirect(url_for('admin_view_operations'))


# #admin deals with Contactus
@login_required
@app.route("/admin/veiw-contact-us-responses")
def admin_view_contact_us_responses():
    all_responses = ContactUs.query.all()
    return render_template("admin_view_contact_us_responses.html", all_responses=all_responses, USER='ADMIN')



@login_required
@app.route("/admin/delete-contact-us-response/<int:id>", methods=['GET', 'POST'])
def admin_delete_contact_us_response(id):
    response = ContactUs.query.filter_by(id=id).first()

    db.session.delete(response)
    db.session.commit()
    return redirect(url_for('admin_view_contact_us_responses'))


