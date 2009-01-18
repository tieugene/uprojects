INSERT INTO user (id, login, password, comments) VALUES (1, "user00", "pass00", "Eugene");
INSERT INTO org (id, name, comments) VALUES (1, "Org00", "Roga und Kopyta");
INSERT INTO dbtype (id, name, comments) VALUES (1, "Account", "1C:Accounting 7.7 Typical Pro");
INSERT INTO host (id, name) VALUES (1, "server");
INSERT INTO share (id, hostid, name) VALUES (1, 1, "1c");
INSERT INTO db (id, shareid, dbtypeid, orgid, path, comments) VALUES (1, 1, 1, 1, "A.Roga", "encaching");
INSERT INTO acl (id, userid, dbid, visible) VALUES (1, 1, 1, "T");
