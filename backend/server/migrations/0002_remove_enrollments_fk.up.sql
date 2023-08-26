
ALTER TABLE enrollments
DROP COLUMN user_id;

ALTER TABLE enrollments
ADD COLUMN student_id VARCHAR(9) NOT NULL;

ALTER TABLE enrollments
ADD UNIQUE (student_id, module_id);

ALTER TABLE modules
ADD UNIQUE (code);