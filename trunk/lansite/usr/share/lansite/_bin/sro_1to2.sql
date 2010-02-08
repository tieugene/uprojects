BEGIN;
DELETE FROM sro2_insurer;
DELETE FROM sro2_okato;
DELETE FROM sro2_okopf;
DELETE FROM sro2_okved;
DELETE FROM sro2_srotype;
DELETE FROM sro2_sro;
DELETE FROM sro2_stage;
DELETE FROM sro2_job;
DELETE FROM sro2_speciality;
DELETE FROM sro2_specialitystage;
DELETE FROM sro2_skill;
DELETE FROM sro2_eventtype;
DELETE FROM sro2_role;
DELETE FROM sro2_person;
DELETE FROM sro2_personskill;
DELETE FROM sro2_org;
DELETE FROM sro2_orgokved;
DELETE FROM sro2_orgphone;
DELETE FROM sro2_orgemail;
DELETE FROM sro2_orgwww;
DELETE FROM sro2_orgstuff;
DELETE FROM sro2_orgsro;
DELETE FROM sro2_orgevent;
DELETE FROM sro2_orglicense;
DELETE FROM sro2_orginsurance;
DELETE FROM sro2_protocol;
DELETE FROM sro2_stagelisttype;
DELETE FROM sro2_stagelist;
DELETE FROM sro2_permitstage;
DELETE FROM sro2_permitstagejob;
INSERT INTO sro2_insurer (id, name, fullname) SELECT id, name, fullname FROM sro_insurer;
INSERT INTO sro2_okato (id, name) SELECT id, name FROM sro_okato;
INSERT INTO sro2_okopf (id, name, shortname, namedp, disabled, parent_id) SELECT id, name, shortname, namedp, disabled, parent_id FROM sro_okopf;
INSERT INTO sro2_okved (id, name, parent_id) SELECT id, name, parent_id FROM sro_okved;
INSERT INTO sro2_srotype (id, name) VALUES (1, 'Строительство');
INSERT INTO sro2_srotype (id, name) VALUES (2, 'Проектирование');
INSERT INTO sro2_sro (id, name, fullname, regno, type_id, own) VALUES (1, 'МООЖС', 'НП СРО "Межрегиональное объединение организаций железнодорожного строительства"', 'СРО-С-043-28092009', 1, 1);
INSERT INTO sro2_sro (id, name, fullname, regno, type_id, own) VALUES (2, 'МООАСП', 'НП СРО "Межрегиональное объединение организаций архитектурно-строительного проектирования"', 'СРО-П-115-18012010', 2, 1);
INSERT INTO sro2_sro (id, name, fullname, regno, type_id, own) SELECT id+2, name, fullname, regno, 1, 0 FROM sro_sro;
INSERT INTO sro2_stage (id, srotype_id, no, name, hq, hs, mq, ms) SELECT id, 1, id, name, hq, hs, mq, ms FROM sro_stage;
INSERT INTO sro2_stage (id, srotype_id, no, name, hq, hs, mq, ms) SELECT 100+id, 2, id, name, hq, hs, mq, ms FROM sro_prjstage;
INSERT INTO sro2_job (id, stage_id, okdp, name) SELECT id, stage_id, okdp, name FROM sro_job;
INSERT INTO sro2_speciality (id, name) SELECT id, name FROM sro_speciality;
INSERT INTO sro2_specialitystage (id, speciality_id, stage_id) SELECT id, speciality_id, stage_id FROM sro_specialitystage;
INSERT INTO sro2_skill (id, name, high) SELECT id, name, high FROM sro_skill;
INSERT INTO sro2_eventtype (id, name, comments) SELECT id, name, comments FROM sro_eventtype;
INSERT INTO sro2_role (id, name, comments) SELECT id, name, comments FROM sro_role;
INSERT INTO sro2_person (id, firstname, midname, lastname, phone) SELECT id, firstname, midname, lastname, phone FROM sro_person;
INSERT INTO sro2_personskill (id, person_id, speciality_id, skill_id, year, skilldate, school, seniority, seniodate, tested, courseno, coursedate, coursename, courseschool) SELECT id, person_id, speciality_id, skill_id, year, skilldate, school, seniority, seniodate, tested, courseno, coursedate, coursename, courseschool FROM sro_personskill;
INSERT INTO sro2_org (id, name, fullname, okopf_id, egruldate, inn, kpp, ogrn, okato_id, laddress, raddress, comments) SELECT id, name, fullname, okopf_id, egruldate, inn, kpp, ogrn, okato_id, laddress, raddress, comments FROM sro_org;
INSERT INTO sro2_orgokved (id, org_id, okved_id) SELECT id, org_id, okved_id FROM sro_orgokved;
INSERT INTO sro2_orgphone (id, org_id, phone) SELECT id, org_id, phone FROM sro_orgphone;
INSERT INTO sro2_orgemail (id, org_id, URL) SELECT id, org_id, URL FROM sro_orgemail;
INSERT INTO sro2_orgwww (id, org_id, URL) SELECT id, org_id, URL FROM sro_orgwww;
INSERT INTO sro2_orgstuff (id, org_id, role_id, person_id, leader, permanent) SELECT id, org_id, role_id, person_id, leader, permanent FROM sro_orgstuff;
INSERT INTO sro2_stagelisttype (id, name)  VALUES (1, 'Заявление');
INSERT INTO sro2_stagelisttype (id, name)  VALUES (2, 'Свидетельство');
-- 1. Building
INSERT INTO sro2_orgsro (id, org_id, sro_id, regno, regdate, paydate, paysum, paydatevv, comments, publish) SELECT id, id, 1, sroregno, sroregdate, paydate, paysum, paydatevv, comments, public FROM sro_org;
INSERT INTO sro2_orgevent (id, orgsro_id, type_id, date, comments) SELECT id, org_id, type_id, date, comments FROM sro_orgevent;
INSERT INTO sro2_orglicense (id, orgsro_id, no, datefrom, datedue) SELECT id, org_id, no, datefrom, datedue FROM sro_orglicense;
INSERT INTO sro2_orginsurance (id, orgsro_id, insurer_id, no, date, sum, datefrom, datedue) SELECT id, org_id, insurer_id, insno, insdate, insum, datefrom, datetill FROM sro_orginsurance;
INSERT INTO sro2_stagelist (id, orgsro_id, type_id) SELECT id, org_id, 3 - permittype_id FROM sro_permit WHERE permittype_id < 3;	/* statement & permit*/
INSERT INTO sro2_permitstage (id, stagelist_id, stage_id) SELECT id, permit_id, stage_id FROM sro_permitstage;
INSERT INTO sro2_permitstagejob (id, permitstage_id, job_id) SELECT id, permitstage_id, job_id FROM sro_permitstagejob;
INSERT INTO sro2_statement (id, stagelist_id, date) SELECT id, permit_id, date FROM sro_permitstatement;
INSERT INTO sro2_permit (id, stagelist_id, no, date, datedue, protocol_id) SELECT id, permit_id, regno, date, datedue, meeting_id FROM sro_permitown;
/*INSERT INTO sro2_protocol (id, sro_id, no, date) SELECT id, 1, regno, date FROM sro_meeting;*/
-- 2. Projecting
COMMIT;
