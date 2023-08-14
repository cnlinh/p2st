CREATE EXTENSION vector; -- pgvector

DROP TABLE IF EXISTS recommendations;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS answers;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    student_id VARCHAR(9) UNIQUE NOT NULL, -- NUS student ID
    email character varying(254) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    name VARCHAR(100) NOT NULL,

    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,

    last_login timestamp with time zone,
    date_joined timestamp with time zone NOT NULL,

    CONSTRAINT user_email_key UNIQUE (email)
);

CREATE table modules (
  id BIGSERIAL PRIMARY KEY,
  code VARCHAR(6) NOT NULL,
  name VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE table enrollments (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  module_id BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  UNIQUE (user_id, module_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (module_id) REFERENCES modules(id)
);

CREATE TABLE topics (
  id BIGSERIAL PRIMARY KEY,
  module_id BIGINT NOT NULL,
  name VARCHAR(50) NOT NULL,  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (module_id) REFERENCES modules(id)
);


CREATE TABLE conversations (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  topic_id BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (topic_id) REFERENCES topics(id)
);

CREATE TYPE ROLE AS ENUM ('user', 'system');

CREATE TABLE questions (
  id BIGSERIAL PRIMARY KEY,
  topic_id BIGINT NOT NULL,
  text TEXT NOT NULL,
  embedding VECTOR(512),
  difficulty REAL NOT NULL,
  created_by ROLE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 
  FOREIGN KEY (topic_id) REFERENCES topics(id)
);

CREATE TABLE answers (
  id BIGSERIAL PRIMARY KEY,
  question_id BIGINT NOT NULL,
  text TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (question_id) REFERENCES questions(id)
);

CREATE TABLE messages (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  conversation_id BIGINT NOT NULL,
  parent_message_id BIGINT,
  question_id BIGINT,
  answer_id BIGINT,
  text TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (conversation_id) REFERENCES conversations(id),
  FOREIGN KEY (parent_message_id) REFERENCES messages(id),
  FOREIGN KEY (question_id) REFERENCES questions(id),
  FOREIGN KEY (answer_id) REFERENCES answers(id),

  CHECK (question_id IS NOT NULL OR answer_id IS NOT NULL)
);

CREATE TABLE ratings (
  id BIGSERIAL PRIMARY KEY,
  message_id BIGINT NOT NULL,
  user_id BIGINT NOT NULL,
  score INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  UNIQUE (message_id, user_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (message_id) REFERENCES messages(id)
);

CREATE TABLE exclude_from_cache (
  id BIGSERIAL PRIMARY KEY,
  text TEXT NOT NULL,
  embedding VECTOR(512),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

