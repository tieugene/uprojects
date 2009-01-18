CREATE VIEW dblist AS
	SELECT
		dbst.id			AS id,
		dbst.path		AS path,
		dbst.comments		AS comments,
		dbst.sharename		AS sharename,
		dbst.sharecomments	AS sharecomments,
		dbst.hostname		AS hostname,
		dbst.hostcomments	AS hostcomments,
		dbst.dbtypename		AS dbtypename,
		dbst.dbtypecomments	AS dbtypecomments,
		org.name		AS orgname,
		org.comments		AS orgcomments
	FROM org INNER JOIN (
		SELECT
			dbshare.id		AS id,
			dbshare.orgid		AS orgid,
			dbshare.path		AS path,
			dbshare.comments	AS comments,
			dbshare.sharename	AS sharename,
			dbshare.sharecomments	AS sharecomments,
			dbshare.hostname	AS hostname,
			dbshare.hostcomments	AS hostcomments,
			dbtype.name		AS dbtypename,
			dbtype.comments		AS dbtypecomments
		FROM dbtype INNER JOIN (
			SELECT
				db.id			AS id,
				db.dbtypeid		AS dbtypeid,
				db.orgid		AS orgid,
				db.path			AS path,
				db.comments		AS comments,
				sharehost.name		AS sharename,
				sharehost.comments	AS sharecomments,
				sharehost.hostname	AS hostname,
				sharehost.hostcomments	AS hostcomments
			FROM db INNER JOIN (
				SELECT
					share.id	AS id,
					share.name	AS name,
					share.comments	AS comments,
					host.name	AS hostname,
					host.comments	AS hostcomments
				FROM share INNER JOIN host ON host.id = share.hostid
			) AS sharehost ON sharehost.id = db.shareid
		) AS dbshare ON dbtype.id = dbshare.dbtypeid
	) AS dbst ON org.id = dbst.orgid
;
