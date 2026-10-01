"""Practical 1: Implementation of Database Connection and DDL/DML Operations.

Course: Database Management Systems Lab
Subject Code: DBMS-LAB-01
Name: [Your Name]
Roll Number: [Your Roll Number]
Date: [DD/MM/YYYY]

Problem Statement:
Create a student database using SQLite3 in Python to demonstrate:
1. DDL: Create a 'students' table with constraints (ID, Name, Branch, CGPA).
2. DML: Insert student records, query with filtering, update records, and delete records.
"""

import sqlite3
from typing import List, Tuple


def get_connection(db_name: str = ":memory:") -> sqlite3.Connection:
    """Establish and return a connection to the SQLite database."""
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """Execute DDL statements to create the students table."""
    query = """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roll_no TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        branch TEXT NOT NULL,
        cgpa REAL CHECK(cgpa >= 0.0 AND cgpa <= 10.0)
    );
    """
    with conn:
        conn.execute(query)
    print("[DDL] Table 'students' created successfully.")


def insert_students(conn: sqlite3.Connection, student_records: List[Tuple[str, str, str, float]]) -> None:
    """Execute DML statement to insert multiple student records."""
    query = """
    INSERT INTO students (roll_no, name, branch, cgpa)
    VALUES (?, ?, ?, ?);
    """
    with conn:
        conn.executemany(query, student_records)
    print(f"[DML] Inserted {len(student_records)} student record(s).")


def fetch_all_students(conn: sqlite3.Connection) -> List[Tuple]:
    """Retrieve all student records ordered by CGPA descending."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, roll_no, name, branch, cgpa FROM students ORDER BY cgpa DESC;")
    return cursor.fetchall()


def update_student_cgpa(conn: sqlite3.Connection, roll_no: str, new_cgpa: float) -> None:
    """Update CGPA for a student identified by roll number."""
    query = "UPDATE students SET cgpa = ? WHERE roll_no = ?;"
    with conn:
        cursor = conn.execute(query, (new_cgpa, roll_no))
        if cursor.rowcount == 0:
            print(f"[WARN] No student found with Roll No: {roll_no}")
        else:
            print(f"[DML] Updated CGPA for Roll No '{roll_no}' to {new_cgpa}.")


def delete_student(conn: sqlite3.Connection, roll_no: str) -> None:
    """Delete a student record identified by roll number."""
    query = "DELETE FROM students WHERE roll_no = ?;"
    with conn:
        cursor = conn.execute(query, (roll_no,))
        if cursor.rowcount == 0:
            print(f"[WARN] No student found with Roll No: {roll_no}")
        else:
            print(f"[DML] Deleted student with Roll No '{roll_no}'.")


def main() -> None:
    """Driver function demonstrating DDL and DML operations."""
    print("=" * 50)
    print("Practical 1: SQLite3 DDL and DML Operations")
    print("=" * 50)

    # Use in-memory database for demonstration
    conn = get_connection(":memory:")

    # 1. Create table
    create_schema(conn)

    # 2. Insert records
    sample_data = [
        ("CS101", "Alice Smith", "CSE", 9.4),
        ("CS102", "Bob Johnson", "IT", 8.7),
        ("CS103", "Charlie Davis", "CSE", 7.9),
        ("CS104", "Diana Prince", "ECE", 9.1),
    ]
    insert_students(conn, sample_data)

    # 3. Query records
    print("\nInitial Records:")
    for row in fetch_all_students(conn):
        print(f"  ID: {row[0]} | Roll: {row[1]} | Name: {row[2]:<14} | Branch: {row[3]:<4} | CGPA: {row[4]}")

    # 4. Update a record
    print("\nUpdating Charlie's CGPA...")
    update_student_cgpa(conn, "CS103", 8.5)

    # 5. Delete a record
    print("\nDeleting Bob's record...")
    delete_student(conn, "CS102")

    # 6. Final state
    print("\nFinal Records:")
    for row in fetch_all_students(conn):
        print(f"  ID: {row[0]} | Roll: {row[1]} | Name: {row[2]:<14} | Branch: {row[3]:<4} | CGPA: {row[4]}")

    conn.close()
    print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
