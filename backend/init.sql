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
    name character varying(200) NOT NULL,

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
  user_id BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE questions (
  id BIGSERIAL PRIMARY KEY,
  topic_id BIGINT,
  text TEXT NOT NULL,
  embedding DOUBLE PRECISION[],
  difficulty REAL NOT NULL,
 
  FOREIGN KEY (topic_id) REFERENCES topics(id)
);

CREATE TABLE answers (
  id BIGSERIAL PRIMARY KEY,
  question_id BIGINT NOT NULL,
  text TEXT NOT NULL,
  quality INT, -- rating from user, scale of 1-5
  relevance INT, -- rating from user, scale of 1-5
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

CREATE TABLE recommendations (
  id BIGSERIAL PRIMARY KEY,
  message_id BIGINT NOT NULL,
  user_id BIGINT NOT NULL,
  hit BOOLEAN, -- whether the user actually asked our recommended qn
  quality INT, -- rating from user, scale of 1-5
  relevance INT, -- rating from user, scale of 1-5
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (message_id) REFERENCES messages(id)
);

