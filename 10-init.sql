CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot');

CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    имя VARCHAR(50),
    фамилия VARCHAR(50),
    группа VARCHAR(10)
);

INSERT INTO students (имя, фамилия, группа) VALUES
    ('Иван', 'Иванов', 'А-101'),
    ('Мария', 'Петрова', 'Б-202'),
    ('Алексей', 'Сидоров', 'В-303');