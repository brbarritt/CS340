-- DDL Final
-- Group 78
-- Kyle Hanley and Blake Barritt


SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;


-- -----------------------------------------------------
-- Table  `Patients`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Patients`;
DROP TABLE IF EXISTS `Invoices`;
DROP TABLE IF EXISTS `Locations`;
DROP TABLE IF EXISTS `Doctors`;
DROP TABLE IF EXISTS `Locations_has_Doctors`;
DROP TABLE IF EXISTS `Appointments`;

CREATE TABLE IF NOT EXISTS `Patients` (
  `patient_id` INT UNIQUE NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(55) NOT NULL,
  `last_name` VARCHAR(55) NOT NULL,
  `address` VARCHAR(255) NOT NULL,
  `phone_number` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`patient_id`));

-- -----------------------------------------------------
-- Table `Invoices`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Invoices` (
  `invoice_id` INT UNIQUE NOT NULL AUTO_INCREMENT,
  `amount` DECIMAL(19,2) NOT NULL,
  `create_time` TIMESTAMP NOT NULL,
  PRIMARY KEY (`invoice_id`));

-- -----------------------------------------------------
-- Table `Locations`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Locations` (
  `location_id` INT UNIQUE NOT NULL AUTO_INCREMENT,
  `location_name` VARCHAR(255) NOT NULL,
  `type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`location_id`));

-- -----------------------------------------------------
-- Table `Doctors`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Doctors` (
  `doctor_id` INT UNIQUE NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(55) NOT NULL,
  `last_name` VARCHAR(55) NOT NULL,
  `specialty` VARCHAR(55) NOT NULL,
  PRIMARY KEY (`doctor_id`));  

-- -----------------------------------------------------
-- Table `Locations_has_Doctors`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Locations_has_Doctors` (
  `Locations_location_id` INT NOT NULL,
  `Doctors_doctor_id` INT NOT NULL,
  PRIMARY KEY (`Locations_location_id`, `Doctors_doctor_id`),
  INDEX `fk_Locations_has_Doctors_Doctors1_idx` (`Doctors_doctor_id` ASC),
  INDEX `fk_Locations_has_Doctors_Locations1_idx` (`Locations_location_id` ASC),
  CONSTRAINT `fk_Locations_has_Doctors_Locations1`
    FOREIGN KEY (`Locations_location_id`)
    REFERENCES `Locations` (`location_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Locations_has_Doctors_Doctors1`
    FOREIGN KEY (`Doctors_doctor_id`)
    REFERENCES `Doctors` (`doctor_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION);

-- -----------------------------------------------------
-- Table `Appointments`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `Appointments` (
  `appointment_id` INT UNIQUE NOT NULL AUTO_INCREMENT,
  `appointment_date` DATE NOT NULL,
  `reason` VARCHAR(255) NOT NULL,
  `Invoices_invoice_id` INT NOT NULL,
  `Doctors_doctor_id` INT NOT NULL,
  `Patients_patient_id` INT,    #Changed to fulfill requirement
  PRIMARY KEY (`appointment_id`),
  INDEX `fk_Appointments_Invoices2_idx` (`Invoices_invoice_id` ASC),
  INDEX `fk_Appointments_Doctors1_idx` (`Doctors_doctor_id` ASC),
  INDEX `fk_Appointments_Patients1_idx` (`Patients_patient_id` ASC),
  CONSTRAINT `fk_Appointments_Invoices2`
    FOREIGN KEY (`Invoices_invoice_id`)
    REFERENCES `Invoices` (`invoice_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Appointments_Doctors1`
    FOREIGN KEY (`Doctors_doctor_id`)
    REFERENCES `Doctors` (`doctor_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Appointments_Patients1`
    FOREIGN KEY (`Patients_patient_id`)
    REFERENCES `Patients` (`patient_id`)
    ON DELETE SET NULL
    ON UPDATE NO ACTION);


-- ---------------------------------
-- Data Insert Queries
-- ---------------------------------

-- Patients Insert
INSERT INTO `Patients` (`first_name`, `last_name`, `address`, `phone_number`)
VALUES
    ('Bob', 'Smith', '101 Oak St', '(949) 222 2222'),
    ('Bill', 'Butler', '55 Zeb Cove Rd', '(949) 212 2121'),
    ('Ashley', 'Brewer', '201 Emerald Bay', '(949) 999 2222'),
    ('Allen', 'Walsh', '200 Misty Sea Dr', '(949) 765 4545'),
    ('Jessica', 'Pavlovsky', '10 Riviera Dr', '(949) 310 7141');

-- Locations Insert
INSERT INTO `Locations` (`location_name`, `type`)
VALUES
    ('Hoag Hospital Newport Beach', 'Hospital'),
    ('Hoag Hospital Irvine', 'Hospital'),
    ('Hoag Medical Group Laguna Beach', 'Med Group'),
    ('Hoag Urgent Care Aliso Viejo', 'Urgent Care'),
    ('Hoag Urgent Care Family Medicine', 'Urgent Care');

-- Doctors Insert
INSERT INTO `Doctors` (`first_name`, `last_name`, `specialty`)
VALUES
    ('John', 'Doe', 'Internist'),
    ('Jane', 'Doe', 'Cardiology'),
    ('Tom', 'Allen', 'Orthopedics'),
    ('Jessica', 'Butler', 'Neurology'),
    ('Jane', 'Pavlovsky', 'Family Medicine');

-- Appointments Insert
INSERT INTO `Appointments` (`appointment_date`, `reason`, `Invoices_invoice_id`, `Doctors_doctor_id`, `Patients_patient_id`)
VALUES
    ('2023-07-12', 'General Checkup', 2, 1, 1),
    ('2023-07-07', 'Brain Surgery', 3, 2, 1),
    ('2023-07-11', 'Face Melted', 1, 3, 4),
    ('2023-07-22', 'Ear Infection', 4, 3, 4),
    ('2023-07-24', 'Broken ankle', 5, 4, 5);

-- Invoices Insert
INSERT INTO `Invoices` (`amount`, `create_time`)
VALUES
    (1500, '2023-07-12 10:33:00'),
    (240, '2023-07-12 10:43:00'),
    (320, '2023-07-12 10:55:00'),
    (325, '2023-07-12 10:58:00'),
    (450, '2023-07-12 10:58:10');

-- Intersection table creating relationship
INSERT INTO `Locations_has_Doctors` (`Locations_location_id`, `Doctors_doctor_id`)
VALUES
    (2, 3),
    (1, 3),
    (3, 1);


SET FOREIGN_KEY_CHECKS=1;
COMMIT;