INSERT INTO schools (id, name) VALUES (1, 'Greenfield High School');

INSERT INTO teachers (id, school_id, name, email) VALUES
  (1, 1, 'Anita Rao',   'anita.rao@greenfield.edu'),
  (2, 1, 'Vikram Shah', 'vikram.shah@greenfield.edu');

INSERT INTO classes (id, school_id, name) VALUES
  (1, 1, '10-A'),
  (2, 1, '10-B');

INSERT INTO subjects (id, school_id, name) VALUES
  (1, 1, 'Maths'),
  (2, 1, 'English');

INSERT INTO teaching_assignments (school_id, teacher_id, class_id, subject_id) VALUES
  (1, 1, 1, 1),
  (1, 1, 2, 1),
  (1, 2, 1, 2),
  (1, 2, 2, 2);

INSERT INTO students (id, school_id, class_id, name, roll_number) VALUES
  (1, 1, 1, 'Aarav Mehta', 1),
  (2, 1, 1, 'Diya Nair',   2),
  (3, 1, 2, 'Rohan Iyer',  1),
  (4, 1, 2, 'Sara Khan',   2);

INSERT INTO parents (id, school_id, name, phone) VALUES
  (1, 1, 'Sunita Mehta', '+91-90000-00001'),
  (2, 1, 'Rajesh Nair',  '+91-90000-00002');

INSERT INTO student_guardians (school_id, student_id, parent_id, relationship) VALUES
  (1, 1, 1, 'mother'),
  (1, 2, 2, 'father');

INSERT INTO marks (school_id, student_id, subject_id, exam_name, score) VALUES
  (1, 1, 1, 'Midterm', 88.50),
  (1, 2, 1, 'Midterm', 92.00),
  (1, 3, 1, 'Midterm', 75.25),
  (1, 4, 1, 'Midterm', 81.00),
  (1, 1, 2, 'Midterm', 79.00),
  (1, 2, 2, 'Midterm', 85.50);

-- identity columns start at 1; move them past the ids we inserted by hand
SELECT setval(pg_get_serial_sequence('schools',  'id'), (SELECT max(id) FROM schools));
SELECT setval(pg_get_serial_sequence('teachers', 'id'), (SELECT max(id) FROM teachers));
SELECT setval(pg_get_serial_sequence('classes',  'id'), (SELECT max(id) FROM classes));
SELECT setval(pg_get_serial_sequence('subjects', 'id'), (SELECT max(id) FROM subjects));
SELECT setval(pg_get_serial_sequence('students', 'id'), (SELECT max(id) FROM students));
SELECT setval(pg_get_serial_sequence('parents',  'id'), (SELECT max(id) FROM parents));
