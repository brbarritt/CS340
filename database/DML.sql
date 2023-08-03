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

-- Delete
DELETE FROM Locations WHERE location_id = :locationIdInput;

-- -----------------------------------------------------
-- `Doctors`
-- -----------------------------------------------------

-- Get all doctor names and specialties
SELECT doctor_id, first_name, last_name, specialty FROM Doctors;

-- Add a new doctor
INSERT INTO Doctors (first_name, last_name, specialty) VALUES (:firstNameInput, :lastNameInput, :specialtyInput);

-- Update
UPDATE Doctors SET first_name = :firstNameInput, last_name = :lastNameInput, specialty = :specialtyInput WHERE doctor_id = :doctorIdInput;

-- Delete
DELETE FROM Doctors WHERE doctor_id = :doctorIdInput;

-- -----------------------------------------------------
-- `Patients`
-- -----------------------------------------------------

-- Get all patient details
SELECT patient_id, first_name, last_name, address, phone_number FROM Patients;

-- Get appointments by patient name
SELECT appointment_id, appointment_date, reason, Invoices_invoice_id, Doctors_doctor_id, Patients_patient_id 
FROM Appointments
INNER JOIN Patients ON Appointments.Patients_patient_id = Patients.patient_id
WHERE Patients.first_name = :patientFirstNameInput OR Patients.last_name = :patientLastNameInput;

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

