CREATE TABLE var (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE, value TEXT
);
CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	login TEXT UNIQUE,
	password TEXT,
	comments TEXT
);
CREATE TABLE org (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	comments TEXT
);
CREATE TABLE dbtype (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	comments TEXT
);
CREATE TABLE host (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT UNIQUE,
	comments TEXT
);
CREATE TABLE share (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	hostid INTEGER,
	name TEXT UNIQUE,
	comments TEXT
);
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
CREATE VIEW "sharelist" AS
	SELECT
		share.id AS id,
		share.name AS name,
		host.name AS hostname
	FROM share INNER JOIN host ON host.id = share.hostid;
CREATE VIEW "dblist" AS
	SELECT
		dbst.id AS id,
		dbst.shareid AS shareid,
		dbst.hostid AS hostid,
		dbst.hostid AS hostid,
		dbst.dbtypeid AS dbtypeid,
		dbst.orgid AS orgid,
		dbst.path AS path,
		dbst.comments AS comments,
		dbst.sharename AS sharename,
		dbst.sharecomments AS sharecomments,
		dbst.hostname AS hostname,
		dbst.hostcomments AS hostcomments,
		dbst.dbtypename AS dbtypename,
		dbst.dbtypecomments AS dbtypecomments,
		org.name AS orgname,
		org.comments AS orgcomments
	FROM org INNER JOIN (
		SELECT
			dbshare.id AS id,
			dbshare.shareid AS shareid,
			dbshare.hostid AS hostid,
			dbshare.dbtypeid AS dbtypeid,
			dbshare.orgid AS orgid,
			dbshare.path AS path,
			dbshare.comments AS comments,
			dbshare.sharename AS sharename,
			dbshare.sharecomments AS sharecomments,
			dbshare.hostname AS hostname,
			dbshare.hostcomments AS hostcomments,
			dbtype.name AS dbtypename,
			dbtype.comments AS dbtypecomments
		FROM dbtype INNER JOIN (
			SELECT
				db.id AS id,
				db.shareid AS shareid,
				db.dbtypeid AS dbtypeid,
				db.orgid AS orgid,
				db.path AS path,
				db.comments AS comments,
				sharehost.hostid AS hostid,
				sharehost.name AS sharename,
				sharehost.comments AS sharecomments,
				sharehost.hostname AS hostname,
				sharehost.hostcomments AS hostcomments
			FROM db INNER JOIN (
				SELECT
					share.id AS id,
					share.hostid AS hostid,
					share.name AS name,
					share.comments AS comments,
					host.name AS hostname,
					host.comments AS hostcomments
				FROM share INNER JOIN host ON host.id = share.hostid
			) AS sharehost ON sharehost.id = db.shareid
		) AS dbshare ON dbtype.id = dbshare.dbtypeid
	) AS dbst ON org.id = dbst.orgid;
CREATE VIEW "baselist" AS
	SELECT
		acl.userid AS userid,
		acl.dbid AS dbid,
		acl.visible AS visible,
		blst.id AS id,
		blst.path AS path,
		blst.comments AS comments,
		blst.sharename AS sharename,
		blst.sharecomments AS sharecomments,
		blst.hostname AS hostname,
		blst.hostcomments AS hostcomments,
		blst.dbtypename AS dbtypename,
		blst.dbtypecomments AS dbtypecomments,
		blst.orgname AS orgname,
		blst.orgcomments AS orgcomments
	FROM acl INNER JOIN (
		SELECT
			dbst.id AS id,
			dbst.orgid AS orgid,
			dbst.path AS path,
			dbst.comments AS comments,
			dbst.sharename AS sharename,
			dbst.sharecomments AS sharecomments,
			dbst.hostname AS hostname,
			dbst.hostcomments AS hostcomments,
			dbst.dbtypename AS dbtypename,
			dbst.dbtypecomments AS dbtypecomments,
			org.name AS orgname,
			org.comments AS orgcomments
		FROM org INNER JOIN (
			SELECT
				dbshare.id AS id,
				dbshare.dbtypeid AS dbtypeid,
				dbshare.orgid AS orgid,
				dbshare.path AS path,
				dbshare.comments AS comments,
				dbshare.sharename AS sharename,
				dbshare.sharecomments AS sharecomments,
				dbshare.hostname AS hostname,
				dbshare.hostcomments AS hostcomments,
				dbtype.name AS dbtypename,
				dbtype.comments AS dbtypecomments
			FROM dbtype INNER JOIN (
				SELECT
					db.id AS id,
					db.shareid AS shareid,
					db.dbtypeid AS dbtypeid,
					db.orgid AS orgid,
					db.path AS path,
					db.comments AS comments,
					sharehost.hostid AS hostid,
					sharehost.name AS sharename,
					sharehost.comments AS sharecomments,
					sharehost.hostname AS hostname,
					sharehost.hostcomments AS hostcomments
				FROM db INNER JOIN (
					SELECT share.id AS id,
					share.hostid AS hostid,
					share.name AS name,
					share.comments AS comments,
					host.name AS hostname,
					host.comments AS hostcomments
				FROM share INNER JOIN host ON host.id = share.hostid
			) AS sharehost ON sharehost.id = db.shareid
		) AS dbshare ON dbtype.id = dbshare.dbtypeid
	) AS dbst ON org.id = dbst.orgid
) AS blst ON acl.dbid = blst.id ORDER BY hostname, sharename;
CREATE TRIGGER "delorg" BEFORE DELETE ON org
	BEGIN
		DELETE FROM db WHERE db.orgid = OLD.id;
	END;
CREATE TRIGGER "deldbtype" BEFORE DELETE ON dbtype
	BEGIN
		DELETE FROM db WHERE db.dbtypeid = OLD.id;
	END;
CREATE TRIGGER "delhost" BEFORE DELETE ON host
	BEGIN
		DELETE FROM share WHERE share.hostid = OLD.id;
	END;
CREATE TRIGGER "delshare" BEFORE DELETE ON share
	BEGIN
		DELETE FROM db WHERE db.shareid = OLD.id;
	END;
CREATE TRIGGER "deldb" BEFORE DELETE ON db
	BEGIN
		DELETE FROM acl WHERE acl.dbid = OLD.id;
	END;
CREATE TRIGGER "deluser" BEFORE DELETE ON user
	BEGIN
		DELETE FROM acl WHERE acl.userid = OLD.id;
	END;
INSERT INTO "var" VALUES(1,'serial','1');
