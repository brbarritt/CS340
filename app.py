from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


# Configuration

app = Flask(__name__)

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
    return render_template('appointments.j2')

@app.route('/locations_has_doctors')
def locations_has_doctors():
    return render_template('locations_has_doctors.j2')


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 68194)) 

    #Start the app on port 3000, it will be different once hosted
    app.run(port=port, debug=True)