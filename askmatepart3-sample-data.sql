--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS fk_users_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_users_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_users_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS pk_users_id CASCADE;


DROP TABLE IF EXISTS public.question;
DROP SEQUENCE IF EXISTS public.question_id_seq;
CREATE TABLE question (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    view_number integer,
    vote_number integer,
    title text,
    message text,
    image text,
    users_id integer
);

DROP TABLE IF EXISTS public.answer;
DROP SEQUENCE IF EXISTS public.answer_id_seq;
CREATE TABLE answer (
    id serial NOT NULL,
    submission_time timestamp without time zone,
    vote_number integer,
    question_id integer,
    message text,
    image text,
    users_id integer,
    accepted boolean DEFAULT False
);

DROP TABLE IF EXISTS public.comment;
DROP SEQUENCE IF EXISTS public.comment_id_seq;
CREATE TABLE comment (
    id serial NOT NULL,
    question_id integer,
    answer_id integer,
    message text,
    submission_time timestamp without time zone,
    users_id integer
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer NOT NULL,
    tag_id integer NOT NULL
);

DROP TABLE IF EXISTS public.tag;
DROP SEQUENCE IF EXISTS public.tag_id_seq;
CREATE TABLE tag (
    id serial NOT NULL,
    name text
);

DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.users_id_seq;
CREATE TABLE users (
    id serial NOT NULL,
    user_name varchar(15) UNIQUE,
    registration_date date,
    reputation integer DEFAULT 0
);

ALTER TABLE ONLY answer
    ADD CONSTRAINT pk_answer_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT pk_comment_id PRIMARY KEY (id);

ALTER TABLE ONLY question
    ADD CONSTRAINT pk_question_id PRIMARY KEY (id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id);

ALTER TABLE ONLY tag
    ADD CONSTRAINT pk_tag_id PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_users_id PRIMARY KEY (id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_users_id FOREIGN KEY (users_id) REFERENCES users(id);

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_users_id FOREIGN KEY (users_id) REFERENCES users(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_users_id FOREIGN KEY (users_id) REFERENCES users(id);

INSERT INTO users VALUES (1, 'Kata', '2017-05-30', 0);
INSERT INTO users VALUES (2, 'Dani', '2017-05-30', 0);
INSERT INTO users VALUES (3, 'Béci', '2017-05-30', 0);
SELECT pg_catalog.setval('users_id_seq', 3, true);

INSERT INTO question VALUES (0, '2017-04-28 08:29:00', 29, 7, 'Create dictionary with list comprehension', 'I like the Python list comprehension syntax. Can it be used to create dictionaries too? For example, by iterating over pairs of keys and values', NULL, 1);
INSERT INTO question VALUES (1, '2017-04-29 09:19:00', 15, 9, 'How do I pass a variable by reference?', 'The Python documentation seems unclear about whether parameters are passed by reference or value, and the following code produces the unchanged value Original', NULL, 2);
INSERT INTO question VALUES (2, '2017-05-01 10:41:00', 1364, 57, 'What are metaclasses?', 'What are metaclasses? What do you use them for?', NULL, 3);
SELECT pg_catalog.setval('question_id_seq', 2, true);

INSERT INTO answer VALUES (1, '2017-04-28 16:49:00', 4, 1, 'Arguments are passed by assignment. The rationale behind this is twofold: the parameter passed in is actually a reference to an object (but the reference is passed by value) some data types are mutable, but others arent', NULL, 2);
INSERT INTO answer VALUES (2, '2017-04-25 14:42:00', 35, 1, 'This object (the class) is itself capable of creating objects (the instances), and this is why its a class.', NULL, 1);
SELECT pg_catalog.setval('answer_id_seq', 2, true);

INSERT INTO comment VALUES (1, 0, NULL, 'For a short explanation/clarification see the first answer to this stackoverflow question. As strings are immutable, they wont be changed and a new variable will be created, thus the outer variable still has the same value.', '2017-05-01 05:49:00', 3);
INSERT INTO comment VALUES (2, NULL, 1, 'The code shown is good, the explanation as to how is completely wrong. See the answers by DavidCournapeau or DarenThomas for correct explanations as to why', '2017-05-02 16:55:00', 2);
SELECT pg_catalog.setval('comment_id_seq', 2, true);

INSERT INTO tag VALUES (1, 'Python');
INSERT INTO tag VALUES (2, 'SQL');
INSERT INTO tag VALUES (3, 'CSS');
SELECT pg_catalog.setval('tag_id_seq', 3, true);

INSERT INTO question_tag VALUES (0, 1);
INSERT INTO question_tag VALUES (1, 3);
INSERT INTO question_tag VALUES (2, 3);
