import csv
import sqlite3

def insert_data_from_csv(csv_file, table_name, conn):
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        data = [tuple(row) for row in reader]

    if not data:
        print(f"No data found in {csv_file}. Skipping insertion.")
        return

    # Use INSERT OR IGNORE to avoid duplicate key errors
    query = f"INSERT OR IGNORE INTO {table_name} VALUES ({', '.join(['?' for _ in data[0]])})"
    
    try:
        conn.executemany(query, data)
        conn.commit()
        print(f"Inserted {conn.total_changes} new rows into {table_name}.")
    except sqlite3.IntegrityError as e:
        print(f"Error inserting into {table_name}: {e}")
# Connect to SQLite database
conn = sqlite3.connect("hospital.db")

# Ensure foreign keys are enabled
conn.execute("PRAGMA foreign_keys = ON;")

# Create tables with consistent naming
conn.executescript("""
                   
CREATE TABLE IF NOT EXISTS USER_DATA(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    user_type TEXT NOT NULL);
                   

CREATE TABLE IF NOT EXISTS DEPARTMENT (
    DEPT_ID INTEGER PRIMARY KEY,
    DEPT_NAME TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS STAFF (
    STAFF_ID INTEGER NOT NULL,
    NAME TEXT NOT NULL,
    DESIGNATION TEXT NOT NULL,
    DEPT_ID INTEGER NOT NULL,
    FOREIGN KEY (DEPT_ID) REFERENCES DEPARTMENT(DEPT_ID) ON DELETE CASCADE
    UNIQUE(NAME, DESIGNATION, DEPT_ID)
);

CREATE TABLE IF NOT EXISTS CASHIER (
    CASHIER_ID INTEGER PRIMARY KEY,
    NAME TEXT NOT NULL,
    DESIGNATION TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS DOCTOR (
    DOC_ID INTEGER PRIMARY KEY,
    DOC_NAME TEXT NOT NULL,
    SPECIALIZATION TEXT NOT NULL,
    EMAIL TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS NURSE (
    NURSE_ID INTEGER PRIMARY KEY,
    FNAME TEXT NOT NULL,
    LNAME TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ADMIN (
    ADMIN_ID INTEGER PRIMARY KEY,
    NAME TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS PATIENT (
    PAT_ID INTEGER PRIMARY KEY,
    FNAME TEXT NOT NULL,
    LNAME TEXT NOT NULL,
    EMAIL TEXT NOT NULL,
    PATIENT_TYPE TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS APPOINTMENT ( 
    APPT_ID INTEGER PRIMARY KEY, 
    DOC_ID INTEGER NOT NULL, 
    DATE TEXT NOT NULL, 
    TIME TEXT NOT NULL, 
    PAT_ID INTEGER NOT NULL,
    FOREIGN KEY (DOC_ID) REFERENCES DOCTOR(DOC_ID) ON DELETE CASCADE,
    FOREIGN KEY (PAT_ID) REFERENCES PATIENT(PAT_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Billing ( 
invoice_id TEXT NOT NULL PRIMARY KEY,
pat_id INTEGER NOT NULL, 
items TEXT NOT NULL, 
amount REAL NOT NULL, 
FOREIGN KEY (pat_id) REFERENCES Patient(pat_id) ON DELETE CASCADE);




PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS Medical_History (  
    proc_id INTEGER NOT NULL,  
    name TEXT NOT NULL,  
    appt_id INTEGER NOT NULL,  
    PRIMARY KEY(proc_id, appt_id),
    FOREIGN KEY (appt_id) REFERENCES Appointment(appt_id) ON DELETE CASCADE
    
);
""")

# Insert data from CSV files
insert_data_from_csv('Department.csv', 'DEPARTMENT', conn)
insert_data_from_csv('Staff_table_filled.csv', 'STAFF', conn)
insert_data_from_csv('Cashiers.csv', 'CASHIER', conn)
insert_data_from_csv('Doctor.csv', 'DOCTOR', conn)
insert_data_from_csv('Nurse.csv', 'NURSE', conn)
insert_data_from_csv('Admin.csv', 'ADMIN', conn)
insert_data_from_csv('Patient.csv', 'PATIENT', conn)
insert_data_from_csv('Appointment.csv', 'APPOINTMENT', conn)
insert_data_from_csv('med_history.csv', 'MEDICAL_HISTORY', conn)
insert_data_from_csv('Billing.csv', 'BILLING', conn)
insert_data_from_csv('User_data.csv', 'USER_DATA', conn)


# Close the database connection
conn.close()
