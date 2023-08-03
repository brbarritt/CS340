from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request

import os
import database.db_connector as db


# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("index.j2")

@app.route('/patients')
def patients():
    return render_template('patients.j2')

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
    
        print(results)
        return render_template("invoices.j2", Invoices=results)


    

@app.route('/locations')
def locations():
    return render_template('locations.j2')

@app.route('/doctors')
def doctors():
    if request.method == 'POST':
        # Will add just to be consistent and get to the Edit/Delete
        return redirect('/doctors')
    else:
        query = "SELECT * FROM Doctors;"
        cursor = db_connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall() 

        return render_template("doctors.j2", Doctors=results)
    
@app.route('/edit_doctor/<int:doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    if request.method == 'POST':
        # Get user input
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        specialty = request.form['specialty'] 

        # Updating doctor info
        query = "UPDATE Doctors SET first_name = %s, last_name = %s, specialty = %s WHERE doctor_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (first_name, last_name, specialty, doctor_id))
        db_connection.commit()

        return redirect('/doctors')
    else:
        # Retrieving based on ID
        query = "SELECT * FROM Doctors WHERE doctor_id = %s;"
        cursor = db_connection.cursor()
        cursor.execute(query, (doctor_id,))
        doctor = cursor.fetchone()

        return render_template("edit_doctor.j2", doctor=doctor)

@app.route('/delete_doctor/<int:doctor_id>')
def delete_doctor(doctor_id):
    # Delete the doctor's record from the database
    query = "DELETE FROM Doctors WHERE doctor_id = %s;"
    cursor = db_connection.cursor()
    cursor.execute(query, (doctor_id,))
    db_connection.commit()

    return redirect('/doctors')

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        # if request.form.get("Add_Appointment"):
        #     appointment_date = request.form['appointment_date']
        #     reason = request.form['reason']
        #     doctor_id = request.form['doctor_id']
        #     patient_id = request.form['patient_id']
        #     invoice_id = request.form['invoice_id']
            
        #     query = "INSERT INTO Appointments (appointment_date, reason, Doctors_doctor_id, Patients_patient_id, Invoices_invoice_id) VALUES (%s, %s, %s, %s, %s);"
        #     cursor = db_connection.cursor()
        #     cursor.execute(query, (appointment_date, reason, doctor_id, patient_id, invoice_id))
        #     db_connection.commit()
        # The way the interface between MySQL and Flask works is by using an
        # object called a cursor. Think of it as the object that acts as the
        # person typing commands directly into the MySQL command line and
        # reading them back to you when it gets results
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


@app.route('/locations_has_doctors')
def locations_has_doctors():
    return render_template('locations_has_doctors.j2')


# Listener

if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 68194)) 

    #Start the app on port 3000, it will be different once hosted
    app.run()