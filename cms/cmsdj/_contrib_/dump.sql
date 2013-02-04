INSERT INTO core_person (id, lastname, firstname, midname, gender_id, birthdate, birthplace) VALUES (1,'Иванов','Иван','Иванович',1,'1970-02-06','под забором');
INSERT INTO core_personaddress (id, person_id, addrtype_id, no, housing, building, app) VALUES(1,1,1,'1','2','3','4');
INSERT INTO core_personphone (id, person_id, phonetype_id, ccode, tcode, cno, hno) VALUES (1,1,2,'7','921','1234657','123-45-67');
INSERT INTO core_personemail (id, person_id, email) VALUES (1,1,'ivanoff@mail.ru');
INSERT INTO core_persondocument (id, person_id, doctype_id, series, no, date, place, addon) VALUES (1,1,1,'4005','123456','2003-02-01','15 ОМ Невского р-на СПБ','');
INSERT INTO core_personcode (id, person_id, codetype_id, value) VALUES (1,1,1,'78654123');
