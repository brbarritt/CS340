from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request

import os
import database.db_connector as db


# CS340 Portfolio Project
# Kyle Hanley and Blake Barritt

# -- Source Cited -- #
# Date: 8/12/2023
# The following code as well as the database connection and integreation are adapted from the CS340 Flask Guide provided
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app


# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("index.j2")

@app.route('/patients', methods=['GET', 'POST'])
def patients():
    if request.method == 'POST':
        # Getting User input
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        #Insert Patient into DB
        query = "INSERT INTO Patients (first_name, last_name, address, phone_number) VALUES (%s, %s, %s, %s);"
        cursor = db_connection.cursor()
        cursor.execute(query, (first_name, last_name, address, phone_number))
        db_connection.commit()
        
        return redirect('/patients')
    else:
        query = "SELECT * FROM Patients;"
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall() 

        return render_template("patients.j2", Patients=results)

@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    if request.method == 'POST':
        # Get user input
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        # Update Patient
        query = "UPDATE Patients SET first_name = %s,  last_name = %s,address = %s, phone_number = %s WHERE patient_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (first_name, last_name, address, phone_number, patient_id))
        db_connection.commit()

        return redirect('/patients')
    else:
        # Retrieving based on ID
        query = "SELECT * FROM Patients WHERE patient_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (patient_id,))
        patient = cursor.fetchone()

        return render_template("edit_patient.j2", patient=patient)

@app.route('/delete_patient/<int:patient_id>')
def delete_patient(patient_id):
    query = "DELETE FROM Patients WHERE patient_id = %s;"
    cursor = db_connection.cursor()
    cursor.execute(query, (patient_id,))
    db_connection.commit()

    return redirect('/patients')

@app.route('/invoices', methods=['GET', 'POST'])
def invoices():
    if request.method == 'POST':
        amount = request.form['amount']
        query = "INSERT INTO Invoices (amount) VALUES (%s);"
        cursor = db_connection.cursor()
        cursor.execute(query, (amount,))
        db_connection.commit()
        return redirect('/invoices')
    else:
        query = "SELECT * FROM Invoices;"
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
    
        # print(results)
        return render_template("invoices.j2", Invoices=results)
    
@app.route('/edit_invoice/<int:invoice_id>', methods=['GET', 'POST'])
def edit_invoice(invoice_id):
    if request.method == 'POST':
        amount = request.form['amount']
        query = "UPDATE Invoices SET amount = %s WHERE invoice_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (amount, invoice_id))
        db_connection.commit()

        return redirect('/invoices')
    else:
        query = "SELECT * FROM Invoices WHERE invoice_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (invoice_id,))
        invoice = cursor.fetchone()

        return render_template("edit_invoice.j2", invoice=invoice)

@app.route('/delete_invoice/<int:invoice_id>')
def delete_invoice(invoice_id):
    # Delete the doctor's record from the database
    query = "DELETE FROM Invoices WHERE invoice_id = %s;"
    cursor = db_connection.cursor()
    cursor.execute(query, (invoice_id,))
    db_connection.commit()

    return redirect('/invoices')


@app.route('/locations', methods=['GET', 'POST'])
def locations():
    if request.method == 'POST':
        location_name = request.form['location_name']
        location_type = request.form['type']

        query = "INSERT INTO Locations (location_name, type) VALUES (%s, %s);"
        cursor = db_connection.cursor()
        cursor.execute(query, (location_name, location_type))
        db_connection.commit()
        
        return redirect('/locations')
    
    else:
        query = "SELECT * FROM Locations;"
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall() 

        return render_template("locations.j2", Locations=results)

@app.route('/location_info/<int:location_id>', methods=['GET', 'POST'])
def location_info(location_id):
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        if doctor_id:
            add_query = "INSERT INTO Locations_has_Doctors (Locations_location_id, Doctors_doctor_id) VALUES (%s, %s);"
            cursor = db_connection.cursor()
            cursor.execute(add_query, (location_id, doctor_id))
            db_connection.commit()
        return redirect('/location_info/{}'.format(location_id))
    else:
        query = "SELECT D.doctor_id, D.first_name, D.last_name FROM Doctors D JOIN Locations_has_Doctors LD on D.doctor_id = LD.Doctors_doctor_id WHERE LD.Locations_location_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (location_id,))
        doctors = cursor.fetchall()

        doctors_query = "SELECT doctor_id, first_name, last_name FROM Doctors WHERE doctor_id NOT IN (SELECT Doctors_doctor_id FROM Locations_has_Doctors WHERE Locations_location_id = %s);"
        cursor.execute(doctors_query, (location_id,))
        available_doctors = cursor.fetchall()

        return render_template('location_info.j2', LocationID=location_id, Doctors=doctors, AvailableDoctors=available_doctors)



@app.route('/edit_location/<int:location_id>', methods=['GET', 'POST'])
def edit_location(location_id):
    if request.method == 'POST':
        # Get user input
        location_name = request.form['location_name']
        location_type = request.form['type']

        query = "UPDATE Locations SET location_name = %s, type = %s WHERE location_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (location_name, location_type, location_id))
        db_connection.commit()

        return redirect('/locations')
    else:
        # Retrieving based on ID
        query = "SELECT * FROM Locations WHERE location_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (location_id,))
        location = cursor.fetchone()

        return render_template("edit_location.j2", location=location)

@app.route('/delete_location/<int:location_id>')
def delete_location(location_id):
    # Delete the doctor's record from the database
    query = "DELETE FROM Locations WHERE location_id = %s;"
    cursor = db_connection.cursor()
    cursor.execute(query, (location_id,))
    db_connection.commit()

    return redirect('/locations')


@app.route('/doctors')
def doctors():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        speciality = request.forn['specialty']

        query = "INSERT INTO Doctors (first_name, last_name, specialty) VALUES (%s, %s, %s);"
        cursor = db_connection.cursor()
        cursor.execute(query, (first_name, last_name, specialty))
        db_connection.commit()
        
        return redirect('/doctors')
    else:
        query = "SELECT * FROM Doctors;"
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall() 

        return render_template("doctors.j2", Doctors=results)
    
@app.route('/doctor_info/<int:doctor_id>')  
def doctor_info(doctor_id):
    doctor_query = "SELECT first_name, last_name FROM Doctors WHERE doctor_id = %s;"
    cursor = db_connection.cursor()
    cursor.execute(doctor_query, (doctor_id,))
    doctor_name = cursor.fetchone()
    
    appointments_query = "SELECT appointment_id, appointment_date, reason, Invoices_invoice_id, Doctors_doctor_id, Patients_patient_id FROM Appointments WHERE Doctors_doctor_id = %s;"
    cursor.execute(appointments_query, (doctor_id,))
    appointments = cursor.fetchall()
    
    return render_template('doctor_info.j2', Doctor=doctor_name, Appointments=appointments)

@app.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        specialty = request.form['specialty'] 

        query = "UPDATE Doctors SET first_name = %s, last_name = %s, specialty = %s WHERE doctor_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (first_name, last_name, specialty, doctor_id))
        db_connection.commit()

        return redirect('/doctors')
    else:
        query = "SELECT * FROM Doctors WHERE doctor_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (doctor_id,))
        doctor = cursor.fetchone()

        return render_template("edit_doctor.j2", doctor=doctor)

@app.route('/delete_doctor/<int:doctor_id>')
def delete_doctor(doctor_id):
    query = "DELETE FROM Doctors WHERE doctor_id = %s;"
    cursor = db_connection.cursor()
    cursor.execute(query, (doctor_id,))
    db_connection.commit()

    return redirect('/doctors')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        appointment_date = request.form['appointment_date']
        reason = request.form['reason']
        invoice_id = request.form['invoice_id']
        doctor_id = request.form['doctor_id']
        patient_id = request.form['patient_id']
        
        query = "INSERT INTO Appointments (appointment_date, reason, Invoices_invoice_id, Doctors_doctor_id, Patients_patient_id) VALUES (%s, %s, %s, %s, %s);"
        cursor = db_connection.cursor()
        cursor.execute(query, (appointment_date, reason, invoice_id, doctor_id, patient_id))
        db_connection.commit()

        return redirect('/appointments')
    else:
        query = "SELECT * FROM Appointments;"
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

        # Dropdowns for doctors, patients, and invoices
        doctors_query = "SELECT doctor_id, first_name, last_name FROM Doctors;"
        patients_query = "SELECT patient_id, first_name, last_name FROM Patients;"
        invoices_query = "SELECT invoice_id FROM Invoices;"
        
        cursor.execute(doctors_query)
        doctors = cursor.fetchall()
        
        cursor.execute(patients_query)
        patients = cursor.fetchall()
        
        cursor.execute(invoices_query)
        invoices = cursor.fetchall()
        
        # print(results)
        return render_template("appointments.j2", Appointments=results, Doctors=doctors, Patients=patients, Invoices=invoices)

@app.route('/edit_appointment/<int:appointment_id>', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    if request.method == 'POST':
        appointment_date = request.form['appointment_date']
        reason = request.form['reason']
        invoice_id = request.form['invoice_id']
        doctor_id = request.form['doctor_id']
        patient_id = request.form['patient_id']
        
        # Nullable relationship on Update
        if patient_id == '':
            patient_id = None
            
        query = "UPDATE Appointments SET appointment_date = %s, reason = %s, Invoices_invoice_id = %s, Doctors_doctor_id = %s, Patients_patient_id = %s WHERE appointment_id = %s"
        cursor = db_connection.cursor()
        cursor.execute(query, (appointment_date, reason, invoice_id, doctor_id, patient_id, appointment_id))
        db_connection.commit()
        
        return redirect('/appointments')
    
    else:
        appointment_query = "SELECT * FROM Appointments WHERE appointment_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(appointment_query, (appointment_id,))
        appointment = cursor.fetchone()
        
        invoices_query = "SELECT invoice_id FROM Invoices;"
        cursor.execute(invoices_query)
        invoices = cursor.fetchall()
    
        doctors_query = "SELECT doctor_id, first_name, last_name FROM Doctors;"
        cursor.execute(doctors_query)
        doctors = cursor.fetchall()
        
        patients_query = "SELECT patient_id, first_name, last_name FROM Patients;"
        cursor.execute(patients_query)
        patients = cursor.fetchall()
        
        return render_template("edit_appointment.j2", appointment=appointment, Invoices=invoices, Doctors=doctors, Patients=patients)
        
    
@app.route('/delete_appointment/<int:appointment_id>')
def delete_appointment(appointment_id):
    query = "DELETE FROM Appointments WHERE appointment_id = %s;"
    cursor = db_connection.cursor()
    cursor.execute(query, (appointment_id,))
    db_connection.commit()

    return redirect('/appointments')


@app.route('/locations_has_doctors')
def locations_has_doctors():
    query = "SELECT * FROM Locations_has_Doctors;"
    cursor = db_connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall() 

    return render_template('locations_has_doctors.j2', LocationsDoctors = results)


# Listener

if __name__ == "__main__":
    app.run()