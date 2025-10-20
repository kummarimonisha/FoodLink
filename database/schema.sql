-- basic example schema (Postgres/MySQL)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) DEFAULT 'donor' -- donor/recipient/admin
);

CREATE TABLE donations (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title VARCHAR(255),
  description TEXT,
  quantity INTEGER,
  expires_at TIMESTAMP,
  status VARCHAR(20) DEFAULT 'pending' -- pending/approved/claimed/rejected
);
