-- Adminer 4.6.3-dev PostgreSQL dump

\connect "dtcfharr0ij91";

DROP TABLE IF EXISTS "city";
DROP SEQUENCE IF EXISTS city_id_seq;
CREATE SEQUENCE city_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."city" (
    "id" integer DEFAULT nextval('city_id_seq') NOT NULL,
    "zipcode" character varying NOT NULL,
    "city" character varying NOT NULL,
    "state" character varying NOT NULL,
    "latitude" numeric NOT NULL,
    "longitude" numeric NOT NULL,
    "population" integer NOT NULL,
    CONSTRAINT "city_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "comments";
DROP SEQUENCE IF EXISTS comments_id_seq;
CREATE SEQUENCE comments_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."comments" (
    "id" integer DEFAULT nextval('comments_id_seq') NOT NULL,
    "user_id" character varying NOT NULL,
    "city_id" integer NOT NULL,
    "comment" character varying NOT NULL,
    "checkin" integer DEFAULT '0',
    CONSTRAINT "comments_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "flights";
DROP SEQUENCE IF EXISTS flights_id_seq;
CREATE SEQUENCE flights_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."flights" (
    "id" integer DEFAULT nextval('flights_id_seq') NOT NULL,
    "origin" character varying NOT NULL,
    "destination" character varying NOT NULL,
    "duration" integer NOT NULL,
    CONSTRAINT "flights_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "passengers";
DROP SEQUENCE IF EXISTS passengers_id_seq;
CREATE SEQUENCE passengers_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."passengers" (
    "id" integer DEFAULT nextval('passengers_id_seq') NOT NULL,
    "name" character varying NOT NULL,
    "flight_id" integer,
    CONSTRAINT "passengers_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "passengers_flight_id_fkey" FOREIGN KEY (flight_id) REFERENCES flights(id) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "username" character varying NOT NULL,
    "password" character varying NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "usr";
DROP SEQUENCE IF EXISTS usr_id_seq;
CREATE SEQUENCE usr_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."usr" (
    "id" integer DEFAULT nextval('usr_id_seq') NOT NULL,
    "name" character varying NOT NULL,
    "flight_id" integer NOT NULL,
    CONSTRAINT "usr_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


-- 2018-07-12 21:32:46.730262+00
