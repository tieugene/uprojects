SELECT
	object.id AS id,
	object.comments AS comments,
	file.size AS size,
	file.datetime AS datetime,
	file.md5 AS md5,
	file.mimetype AS mimetype,
	file.origfn AS origfn,
	file.ext AS ext,
	programm.platform AS platform,
	programm.vendor AS vendor,
	programm.distrib AS distrib,
	programm.name AS name,
	programm.ver AS ver,
	platform.name AS platform_name,
	platform.comments AS platform_comments,
	vendor.name AS vendor_name,
	vendor.comments AS vendor_comments,
	distrib.name AS distrib_name,
	distrib.comments AS distrib_comments
FROM object
	JOIN file ON object.id = file.id
	JOIN programm ON object.id = programm.id
	LEFT JOIN platform ON programm.platform = platform.id
	LEFT JOIN vendor ON programm.vendor = vendor.id
	LEFT JOIN distrib ON programm.distrib = distrib.id
