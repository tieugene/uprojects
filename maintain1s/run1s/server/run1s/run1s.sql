CREATE TABLE var (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	value TEXT
);
;
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	login TEXT UNIQUE,
	password TEXT,
	comments TEXT
);
;
CREATE TABLE org (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	comments TEXT
);
;
CREATE TABLE dbtype (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	comments TEXT
);
;
CREATE TABLE host (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	comments TEXT
);
;
CREATE TABLE share (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	hostid INTEGER,
	name TEXT UNIQUE,
	comments TEXT
);
;
CREATE TABLE db (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	shareid INTEGER,
	dbtypeid INTEGER,
	orgid INTEGER,
	path TEXT,
	comments TEXT
);
CREATE TABLE acl (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	userid INTEGER,
	dbid INTEGER,
	visible BOOL DEFAULT 'F'
);
CREATE VIEW "dblist" AS
SELECT
	db.id		AS id,
	db.shareid	AS shareid,
	db.dbtypeid	AS dbtypeid,
	db.orgid	AS orgid,
	db.path		AS path,
	db.comments	AS comments,
	share.name	AS sharename,
	share.comments	AS sharecomments,
	host.name	AS hostname,
	host.comments	AS hostcomments,
	dbtype.name	AS dbtypename,
	dbtype.comments	AS dbtypecomments,
	org.name	AS orgname,
	org.comments	AS orgcomments
FROM db
	JOIN share ON share.id = db.shareid
	JOIN host ON host.id = share.hostid
	JOIN dbtype ON dbtype.id = db.dbtypeid
	JOIN org ON org.id = db.orgid;
CREATE VIEW "baselist" AS
SELECT
	acl.userid		AS userid,
	acl.dbid		AS dbid,
	acl.visible		AS visible,
	db.shareid	AS shareid,
	db.dbtypeid	AS dbtypeid,
	db.orgid	AS orgid,
	db.path		AS path,
	db.comments	AS comments,
	share.name	AS sharename,
	share.comments	AS sharecomments,
	host.name	AS hostname,
	host.comments	AS hostcomments,
	dbtype.name	AS dbtypename,
	dbtype.comments	AS dbtypecomments,
	org.name	AS orgname,
	org.comments	AS orgcomments
FROM acl
	JOIN db ON db.id = acl.dbid
	JOIN share ON share.id = db.shareid
	JOIN host ON host.id = share.hostid
	JOIN dbtype ON dbtype.id = db.dbtypeid
	JOIN org ON org.id = db.orgid;
CREATE TRIGGER "deluser"
	BEFORE
	DELETE
	ON user
BEGIN
	DELETE FROM acl WHERE acl.userid = OLD.id;
END;
CREATE TRIGGER "delhost"
	BEFORE
	DELETE
	ON host
BEGIN
	DELETE FROM share WHERE share.hostid = OLD.id;
END;
CREATE TRIGGER "delshare"
	BEFORE
	DELETE
	ON share
BEGIN
	DELETE FROM db WHERE db.shareid = OLD.id;
END;
CREATE TRIGGER "delorg"
	BEFORE
	DELETE
	ON org
BEGIN
	DELETE FROM db WHERE db.orgid = OLD.id;
END;
CREATE TRIGGER "deldbtype"
	BEFORE
	DELETE
	ON dbtype
BEGIN
	DELETE FROM db WHERE db.dbtypeid = OLD.id;
END;
CREATE TRIGGER "deldb"
	BEFORE
	DELETE
	ON db
BEGIN
	DELETE FROM acl WHERE acl.dbid = OLD.id;
END;
CREATE VIEW "sharelist" AS
SELECT
		share.id	AS id,
		share.name	AS sharename,
		host.name	AS hostname
FROM share INNER JOIN host ON host.id = share.hostid
ORDER BY hostname, sharename;
