BEGIN;
CREATE TEMPORARY TABLE "tmp" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(40) NOT NULL UNIQUE, "fullname" varchar(100) NOT NULL UNIQUE, "regno" varchar(20) NOT NULL UNIQUE, "type_id" integer NOT NULL, "own" bool NOT NULL );
INSERT INTO tmp SELECT id, name, fullname, regno, type_id, own FROM sro2_sro;
DROP TABLE sro2_sro;
CREATE TABLE "sro2_sro" ("id" integer NOT NULL PRIMARY KEY, "name" varchar(40) NOT NULL UNIQUE, "fullname" varchar(100) NOT NULL UNIQUE, "regno" varchar(20) NOT NULL UNIQUE, "type_id" integer NOT NULL REFERENCES "sro2_srotype" ("id"), "own" bool NOT NULL );
INSERT INTO sro2_sro SELECT id, name, fullname, regno, type_id, own FROM tmp;
DROP TABLE tmp;
COMMIT;
