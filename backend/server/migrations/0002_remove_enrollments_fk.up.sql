
ALTER TABLE enrollments
DROP COLUMN user_id;

ALTER TABLE enrollments
ADD COLUMN student_id VARCHAR(9) NOT NULL;

ALTER TABLE modules
ADD UNIQUE (code);