# =========================================================
# DATABASES & SQL WITH PYTHON 
# =========================================================

import sqlite3
import csv

# ---------------------------------------------------------
# 1. CONNECT TO DATABASE
# ---------------------------------------------------------

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

print("Connected to students.db")


# ---------------------------------------------------------
# 2. CREATE STUDENTS TABLE
# ---------------------------------------------------------

create_table_query = """
CREATE TABLE IF NOT EXISTS students (
id INTEGER PRIMARY KEY AUTOINCREMENT,
full_name TEXT NOT NULL,
course TEXT NOT NULL,
year_level INTEGER NOT NULL
)
"""

cursor.execute(create_table_query)
conn.commit()

print("Table 'students' created successfully.")


# ---------------------------------------------------------
# 3. VERIFY TABLE
# ---------------------------------------------------------

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tables in database:", cursor.fetchall())


# ---------------------------------------------------------
# 4. INSERT SAMPLE DATA
# ---------------------------------------------------------

students = [
("Anna Reyes", "BS ECE", 3),
("Carlos Dela Cruz", "BS EE", 2),
("Mika Santos", "BS CE", 1)
]

insert_query = """
INSERT INTO students (full_name, course, year_level)
VALUES (?, ?, ?)
"""

cursor.executemany(insert_query, students)

conn.commit()

print("Sample data inserted into 'students' table.")


# ---------------------------------------------------------
# 5. DISPLAY INSERTED DATA
# ---------------------------------------------------------

cursor.execute("SELECT * FROM students")

rows = cursor.fetchall()

for row in rows:
    print(row)


# ---------------------------------------------------------
# 6. QUERY DATA
# ---------------------------------------------------------

cursor.execute("SELECT * FROM students")
print("All Students:")

for row in cursor.fetchall():
    print(row)


cursor.execute("SELECT * FROM students WHERE course = 'BS ECE'")
print("\nBS ECE Students:")
print(cursor.fetchall())


cursor.execute("SELECT * FROM students ORDER BY year_level DESC")
print("\nSorted by Year Level:")
print(cursor.fetchall())


cursor.execute("SELECT * FROM students LIMIT 2")
print("\nTop 2 Students:")
print(cursor.fetchall())


# ---------------------------------------------------------
# TRY IT QUERY
# ---------------------------------------------------------

cursor.execute("SELECT * FROM students WHERE course = 'BS CE' AND year_level >= 1")

print("Filtered list of BS CE students:")
print(cursor.fetchall())


# ---------------------------------------------------------
# 7. UPDATE AND DELETE RECORDS
# ---------------------------------------------------------

cursor.execute("""
UPDATE students
SET year_level = 4
WHERE full_name = 'Anna Reyes'
""")

conn.commit()

print("Updated Anna Reyes to 4th year.")


cursor.execute("""
DELETE FROM students
WHERE full_name = 'Carlos Dela Cruz'
""")

conn.commit()

print("Deleted Carlos Dela Cruz from the database.")


# ---------------------------------------------------------
# TRY IT UPDATE
# ---------------------------------------------------------

cursor.execute("""
UPDATE students
SET year_level = 2
WHERE full_name = 'Mika Santos'
""")

conn.commit()

print("Mika Santos has been updated to 2nd year.")


# ---------------------------------------------------------
# 8. AGGREGATE FUNCTIONS
# ---------------------------------------------------------

cursor.execute("SELECT COUNT(*) FROM students")

print("Total Students:", cursor.fetchone()[0])


cursor.execute("SELECT AVG(year_level) FROM students")

print("Average Year Level:", cursor.fetchone()[0])


cursor.execute("SELECT course, COUNT(*) FROM students GROUP BY course")

print("Students per Course:", cursor.fetchall())


cursor.execute("SELECT course, COUNT(*) FROM students GROUP BY course")

print("Total number of students per course:")
print(cursor.fetchall())


# ---------------------------------------------------------
# 9. INSERT DATA VIA USER INPUT
# (Using your information)
# ---------------------------------------------------------

full_name = "INTES, PETER JOHN B."
course = "BS ECE"
year_level = 1

cursor.execute("""
INSERT INTO students (full_name, course, year_level)
VALUES (?, ?, ?)
""", (full_name, course, year_level))

conn.commit()

print("Student record successfully added.")


# ---------------------------------------------------------
# 10. RESET TABLE RECORDS
# ---------------------------------------------------------

cursor.execute("DELETE FROM students")
conn.commit()

cursor.execute("DELETE FROM sqlite_sequence WHERE name='students'")
conn.commit()

print("All records deleted. ID counter reset.")


# ---------------------------------------------------------
# 11. EXPORT DATA TO CSV
# ---------------------------------------------------------

cursor.execute("SELECT * FROM students")

rows = cursor.fetchall()

with open("students_export.csv", "w", newline='') as file:
    writer = csv.writer(file)

    writer.writerow(["ID", "Full Name", "Course", "Year Level"])

    writer.writerows(rows)

print("Data exported to 'students_export.csv'.")


# ---------------------------------------------------------
# 12. CREATE COURSES TABLE
# ---------------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS courses (
course_code TEXT PRIMARY KEY,
description TEXT NOT NULL
)
""")

conn.commit()


course_data = [
("BS ECE", "Electronics and Communications Engineering"),
("BS EE", "Electrical Engineering"),
("BS COE", "Computer Engineering"),
("BS CE", "Civil Engineering")
]

cursor.executemany("""
INSERT OR IGNORE INTO courses (course_code, description)
VALUES (?, ?)
""", course_data)

conn.commit()


cursor.execute("""
SELECT s.full_name, s.course, c.description
FROM students s
JOIN courses c ON s.course = c.course_code
""")


for row in cursor.fetchall():
    print(row)


# ---------------------------------------------------------
# 13. JOIN WITH FILTERING
# ---------------------------------------------------------

cursor.execute("""
SELECT s.full_name, s.course, c.description
FROM students s
JOIN courses c ON s.course = c.course_code
WHERE s.course = 'BS CE'
ORDER BY s.full_name ASC
""")


for row in cursor.fetchall():
    print(row)


# ---------------------------------------------------------
# 14. SEARCH USING LIKE
# ---------------------------------------------------------

cursor.execute("""
SELECT * FROM students
WHERE full_name LIKE '%Reyes%'
""")

print("Static search result:")

for row in cursor.fetchall():
    print(row)


keyword = input("Enter a name keyword to search: ")

cursor.execute("""
SELECT * FROM students
WHERE full_name LIKE ?
""", ('%' + keyword + '%',))


print("Search results:")

for row in cursor.fetchall():
    print(row)


# ---------------------------------------------------------
# CLOSE DATABASE
# ---------------------------------------------------------

cursor.close()
conn.close()

print("Database connection closed.")