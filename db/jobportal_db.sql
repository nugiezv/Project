-- This script was generated by a beta version of the ERD tool in pgAdmin 4.
-- Please log an issue at https://redmine.postgresql.org/projects/pgadmin4/issues/new if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.application
(
    application_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    j_user_id integer NOT NULL,
    jobs_id integer NOT NULL,
    is_accepted boolean NOT NULL DEFAULT false,
    CONSTRAINT application_pkey PRIMARY KEY (application_id)
);

CREATE TABLE IF NOT EXISTS public.company_profile
(
    c_profile_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    c_user_id integer NOT NULL,
    c_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    c_address character varying(255) COLLATE pg_catalog."default" NOT NULL,
    c_description character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT company_profile_pkey PRIMARY KEY (c_profile_id)
);

CREATE TABLE IF NOT EXISTS public.jobs
(
    jobs_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    jobs_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    c_user_id integer NOT NULL,
    jobs_description character varying(255) COLLATE pg_catalog."default" NOT NULL,
    jobs_location character varying(255) COLLATE pg_catalog."default" NOT NULL,
    jobs_type character varying(255) COLLATE pg_catalog."default" NOT NULL,
    jobs_gender character varying(255) COLLATE pg_catalog."default" NOT NULL,
    jobs_status character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT jobs_pkey PRIMARY KEY (jobs_id)
);

CREATE TABLE IF NOT EXISTS public.jobseeker_profile
(
    j_profile_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    j_user_id integer NOT NULL,
    j_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    j_address character varying(255) COLLATE pg_catalog."default" NOT NULL,
    j_contact bigint NOT NULL,
    j_education character varying(255) COLLATE pg_catalog."default" NOT NULL,
    j_experience character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT profile_pkey PRIMARY KEY (j_profile_id)
);

CREATE TABLE IF NOT EXISTS public.users
(
    user_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    username character varying(255) COLLATE pg_catalog."default" NOT NULL,
    email character varying(255) COLLATE pg_catalog."default" NOT NULL,
    password character varying(255) COLLATE pg_catalog."default" NOT NULL,
    type character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_pkey PRIMARY KEY (user_id)
);

ALTER TABLE IF EXISTS public.application
    ADD CONSTRAINT application_j_user_id_fkey FOREIGN KEY (j_user_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.company_profile
    ADD CONSTRAINT company_profile_c_user_id_fkey FOREIGN KEY (c_user_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.jobs
    ADD CONSTRAINT jobs_c_user_id_fkey FOREIGN KEY (c_user_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.jobseeker_profile
    ADD CONSTRAINT profile_user_id_fkey FOREIGN KEY (j_user_id)
    REFERENCES public.users (user_id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;