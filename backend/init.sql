DROP TABLE IF EXISTS recommendations;
DROP TABLE IF EXISTS answers;
DROP TABLE IF EXISTS user_questions;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS topics;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    student_id VARCHAR(9) UNIQUE NOT NULL, -- NUS student ID
    email character varying(254) NOT NULL,
    password VARCHAR(128) NOT NULL,
    name character varying(200),

    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,

    last_login timestamp with time zone,
    date_joined timestamp with time zone NOT NULL,

    CONSTRAINT user_email_key UNIQUE (email)
);

CREATE TABLE topics (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE conversations (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE questions (
  id BIGSERIAL PRIMARY KEY,
  topic_id BIGINT,
  text TEXT NOT NULL,
  embedding DOUBLE PRECISION[],
  difficulty REAL NOT NULL,
 
  FOREIGN KEY (topic_id) REFERENCES topics(id)
);

CREATE TABLE user_questions (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT,
  question_id BIGINT,
  conversation_id BIGINT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  text TEXT NOT NULL,
  parent_question_id BIGINT,

  UNIQUE (user_id, question_id, parent_question_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (question_id) REFERENCES questions(id),
  FOREIGN KEY (parent_question_id) REFERENCES user_questions(id),
  FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);


CREATE TABLE answers (
  id BIGSERIAL PRIMARY KEY,
  user_question_id BIGINT,
  text TEXT NOT NULL,
  quality INT, -- rating from user, scale of 1-5
  relevance INT, -- rating from user, scale of 1-5
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_question_id) REFERENCES user_questions(id)
);


CREATE TABLE recommendations (
  id BIGSERIAL PRIMARY KEY,
  parent_question_id BIGINT,
  user_id BIGINT,
  hit BOOLEAN, -- whether the user actually asked our recommended qn
  quality INT, -- rating from user, scale of 1-5
  relevance INT, -- rating from user, scale of 1-5
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (parent_question_id) REFERENCES user_questions(id)
);

