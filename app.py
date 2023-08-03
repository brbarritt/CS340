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

@app.route('/invoices')
def invoices():
    return render_template('invoices.j2')

@app.route('/locations')
def locations():
    return render_template('locations.j2')

@app.route('/doctors')
def doctors():
    return render_template('doctors.j2')

@app.route('/appointments')
def appointments():
        # Write the query and save it to a variable
    query = "SELECT * FROM Appointments;"

    # The way the interface between MySQL and Flask works is by using an
    # object called a cursor. Think of it as the object that acts as the
    # person typing commands directly into the MySQL command line and
    # reading them back to you when it gets results
    cursor = db.execute_query(db_connection=db_connection, query=query)

    # The cursor.fetchall() function tells the cursor object to return all
    # the results from the previously executed
    #
    # The json.dumps() function simply converts the dictionary that was
    # returned by the fetchall() call to JSON so we can display it on the
    # page.
    results = cursor.fetchall()
    return render_template("appointments.j2", Appointments=results)


@app.route('/locations_has_doctors')
def locations_has_doctors():
    return render_template('locations_has_doctors.j2')


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 68194)) 

    #Start the app on port 3000, it will be different once hosted
    app.run(port=port, debug=True)