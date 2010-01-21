BEGIN;
ALTER TABLE "sro_personskill" ADD COLUMN "courseno" varchar(50);
ALTER TABLE "sro_personskill" ADD COLUMN "coursedate" date;
ALTER TABLE "sro_personskill" ADD COLUMN "coursename" varchar(50);
ALTER TABLE "sro_personskill" ADD COLUMN "courseschool" varchar(100);
COMMIT;