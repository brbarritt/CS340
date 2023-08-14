-- Project Step 3 Draft Data Manipulation
-- Group 78
-- Kyle Hanley and Blake Barritt



-- -----------------------------------------------------
-- `Locations`
-- -----------------------------------------------------

-- Get all location names and types
SELECT location_id, location_name, type FROM Locations;

-- Add a new location
INSERT INTO Locations (location_name, type) VALUES (:locationNameInput, :typeInput);

-- Update
UPDATE Locations SET location_name = :locationNameInput, type = :typeInput WHERE location_id = :locationIdInput;

-- Insert Doctor into Location (via the Locations_has_Doctors table on the Location Info subpage)
INSERT INTO Locations_has_Doctors (Locations_location_id, Doctors_doctor_id) VALUES (:locationNameInput, :doctorInput);

-- Filter and display all doctor's assigned to a location
SELECT D.doctor_id, D.first_name, D.last_name FROM Doctors D JOIN Locations_has_Doctors LD on D.doctor_id = LD.Doctors_doctor_id WHERE Locations_location_id = :Locations_location_id

-- Filter and display all doctor's not assigned to a location
SELECT doctor_id, first_name, last_name FROM Doctors WHERE doctor_id NOT IN (SELECT Doctors_doctor_id FROM Locations_has_Doctors WHERE Locations_location_id = :Locations_location_id


-- Remove Doctor from a Location
DELETE FROM Locations_has_Doctors WHERE Locations_location_id = : Locations_location_id AND Doctors_doctor_id = :Doctors_doctor_id 

-- Delete
DELETE FROM Locations WHERE location_id = :locationIdInput;

-- -----------------------------------------------------
-- `Doctors`
-- -----------------------------------------------------

-- Get all doctor names and specialties
SELECT doctor_id, first_name, last_name, specialty FROM Doctors;

-- Get all appointments by Doctor id
SELECT appointment_id, appointment_date, reason, Invoices_invoice_id, Doctors_doctor_id, Patients_patient_id 
FROM Appointments
WHERE Doctors_doctor_id = :doctorIdInput;

-- Add a new doctor
INSERT INTO Doctors (first_name, last_name, specialty) VALUES (:firstNameInput, :lastNameInput, :specialtyInput);

-- Get all appointments for individual doctor
SELECT appointment_id, appointment_date, reason, Invoices_invoice_id, Doctors_doctor_id, Patients_patient_id FROM Appointments WHERE Doctors_doctor_id = :Doctors_doctor_id

-- Update
UPDATE Doctors SET first_name = :firstNameInput, last_name = :lastNameInput, specialty = :specialtyInput WHERE doctor_id = :doctorIdInput;

-- Delete
DELETE FROM Doctors WHERE doctor_id = :doctorIdInput;

-- -----------------------------------------------------
-- `Patients`
-- -----------------------------------------------------

-- Get all patient details
SELECT patient_id, first_name, last_name, address, phone_number FROM Patients;

-- Add a new patient
INSERT INTO Patients (first_name, last_name, address, phone_number) VALUES 
(:firstNameInput, :lastNameInput, :addressInput, :phoneNumberInput);

-- Update
UPDATE Patients SET first_name = :firstNameInput, last_name = :lastNameInput, address = :addressInput, phone_number = :phoneNumberInput 
WHERE patient_id = :patientIdInput;

-- Delete
DELETE FROM Patients WHERE patient_id = :patientIdInput;

-- -----------------------------------------------------
-- `Appointments`
-- -----------------------------------------------------

-- Get all appointment details
SELECT appointment_id, appointment_date, reason, Invoices_invoice_id, Doctors_doctor_id, Patients_patient_id FROM Appointments;

-- Add a new appointment
INSERT INTO Appointments (appointment_date, reason, Invoices_invoice_id, Doctors_doctor_id, Patients_patient_id) 
VALUES (:appointmentDateInput, :reasonInput, :invoiceIdInput, :doctorIdInput, :patientIdInput);

-- Update
UPDATE Appointments SET appointment_date = :appointmentDateInput, reason = :reasonInput, Invoices_invoice_id = :invoiceIdInput, 
Doctors_doctor_id = :doctorIdInput, Patients_patient_id = :patientIdInput WHERE appointment_id = :appointmentIdInput;

-- Delete
DELETE FROM Appointments WHERE appointment_id = :appointmentIdInput;

-- For clarity, we are adding the dropdown menus to the Appointments section
-- Dropdowns for doctors, patients, and invoices
SELECT doctor_id, first_name, last_name FROM Doctors;
SELECT patient_id, first_name, last_name FROM Patients
SELECT invoice_id FROM Invoices;

-- -----------------------------------------------------
-- `Invoices`
-- -----------------------------------------------------

-- Get all invoice details
SELECT invoice_id, amount, create_time FROM Invoices;

-- Add a new invoice
INSERT INTO Invoices (amount, create_time) VALUES (:amountInput, :createTimeInput);

-- Update
UPDATE Invoices SET amount = :amountInput, create_time = :createTimeInput WHERE invoice_id = :invoiceIdInput;

-- Delete
DELETE FROM Invoices WHERE invoice_id = :invoiceIdInput;

