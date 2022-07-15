# graphqlapi

Create these tables in Postgresql

CREATE TABLE IF NOT EXISTS warp_user_profile
(
user_id VARCHAR(10) NOT NULL PRIMARY KEY,
personaldata_jsonb jsonb NOT NULL,
capacity numeric NOT NULL,
skills text NOT NULL,
interests text NOT NULL,
about_me text NOT NULL,
prof_aspirations text NOT NULL,
target_job_func text NOT NULL,
travel_ready boolean DEFAULT false,
relocation_outside boolean DEFAULT false,
relocation_inside boolean DEFAULT false,
profile_headline text NOT NULL,
education_jsonb jsonb NOT NULL,
experience_jsonb jsonb NOT NULL,
language_jsonb jsonb NOT NULL,
certificates boolean DEFAULT false,
cert_jsonb jsonb,
status_visible boolean DEFAULT false,
email_newmsg boolean DEFAULT false,
email_rolerec boolean DEFAULT false,
email_reminders boolean DEFAULT false,
email_vis boolean DEFAULT false,
phone_vis boolean DEFAULT false,
mobile_vis boolean DEFAULT false,
updated_on timestamp with time zone DEFAULT now(),
created_on timestamp with time zone DEFAULT now(),
profile_pic character varying(256)
);

CREATE TABLE warp_user_role
(user_id Varchar(10) NOT NULL,
project_id Integer NOT NULL,
role_name Varchar(50) NOT NULL,
category VARCHAR (20) NOT NULL,
status BOOLEAN NOT NULL DEFAULT true,
updated_on Timestamptz DEFAULT NOW(),
created_on Timestamptz DEFAULT NOW(),PRIMARY KEY (user_id, project_id, role_name));

CREATE SCHEMA IF NOT EXISTS public;

-- Create a sequence project_id_seq , which start from 10001
CREATE SEQUENCE IF NOT EXISTS project_id_seq START 10001 INCREMENT BY 1;

-- Create a sequence msg_id_seq , which start from 100001
CREATE SEQUENCE msg_id_seq START 100001 INCREMENT BY 1;

