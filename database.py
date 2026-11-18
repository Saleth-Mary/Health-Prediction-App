
import sqlite3
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent / "health_records.db"


# 1. Establish database connection
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# 2. Create patients and failed_records tables
def create_table():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT NOT NULL,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS failed_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_number INTEGER,
            full_name TEXT,
            dob TEXT,
            email TEXT,
            glucose TEXT,
            haemoglobin TEXT,
            cholesterol TEXT,
            error_reason TEXT
        )
    """)

    conn.commit()
    conn.close()


# 3. CREATE - Insert a valid patient and return patient ID
def add_patient(full_name, dob, email, glucose,
                haemoglobin, cholesterol, remarks):

    conn = get_connection()

    cursor = conn.execute("""
        INSERT INTO patients
        (full_name, dob, email, glucose,
         haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (full_name, dob, email, glucose,
          haemoglobin, cholesterol, remarks))

    patient_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return patient_id


# 4. READ - Retrieve all valid patients
def get_all_patients():
    conn = get_connection()

    patients = conn.execute(
        "SELECT * FROM patients ORDER BY id"
    ).fetchall()

    conn.close()

    return [dict(patient) for patient in patients]


# 5. UPDATE - Update patient email
def update_patient_email(patient_id, new_email):
    conn = get_connection()

    conn.execute("""
        UPDATE patients
        SET email = ?
        WHERE id = ?
    """, (new_email, patient_id))

    conn.commit()
    conn.close()


# 6. DELETE - Delete a patient
def delete_patient(patient_id):
    conn = get_connection()

    conn.execute("""
        DELETE FROM patients
        WHERE id = ?
    """, (patient_id,))

    conn.commit()
    conn.close()


# 7. READ - Retrieve one patient by ID
def get_patient_by_id(patient_id):
    conn = get_connection()

    patient = conn.execute(
        "SELECT * FROM patients WHERE id = ?",
        (patient_id,)
    ).fetchone()

    conn.close()

    return dict(patient) if patient else None


# 8. UPDATE - Update AI-generated remarks
def update_patient_remarks(patient_id, remarks):
    conn = get_connection()

    conn.execute("""
        UPDATE patients
        SET remarks = ?
        WHERE id = ?
    """, (remarks, patient_id))

    conn.commit()
    conn.close()


# 9. CREATE - Save a rejected patient record
def add_failed_record(test_number, full_name, dob, email,
                      glucose, haemoglobin, cholesterol, error_reason):

    conn = get_connection()

    conn.execute("""
        INSERT INTO failed_records
        (test_number, full_name, dob, email,
         glucose, haemoglobin, cholesterol, error_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (test_number, full_name, dob, email,
          str(glucose), str(haemoglobin), str(cholesterol),
          error_reason))

    conn.commit()
    conn.close()


# 10. READ - Retrieve all rejected patient records
def get_failed_records():
    conn = get_connection()

    records = conn.execute(
        "SELECT * FROM failed_records ORDER BY id"
    ).fetchall()

    conn.close()

    return [dict(record) for record in records]
