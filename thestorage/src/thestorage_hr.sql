SELECT
	soft_file.id AS id,
	soft_file.name AS name,
	soft_file.ver AS ver,
	soft_file.platform_id AS platform_id,
	soft_file.platform_name AS platform_name,
	soft_file.platform_comments AS platform_comments,
	soft_file.vendor_id AS vendor_id,
	soft_file.vendor_name AS vendor_name,
	soft_file.vendor_comments AS vendor_comments,
	soft_file.distrib_id AS distrib_id,
	soft_file.distrib_name AS distrib_name,
	soft_file.distrib_comments AS distrib_comments,
	soft_file.file_size AS file_size,
	soft_file.datetime AS datetime,
	soft_file.md5 AS md5,
	soft_file.mimetype AS mimetype,
	soft_file.origfn AS origfn,
	soft_file.ext AS ext,
	object.comments AS comments
FROM object LEFT JOIN (
	SELECT
		soft_distrib.id AS id,
		soft_distrib.name AS name,
		soft_distrib.ver AS ver,
		soft_distrib.platform_id AS platform_id,
		soft_distrib.platform_name AS platform_name,
		soft_distrib.platform_comments AS platform_comments,
		soft_distrib.vendor_id AS vendor_id,
		soft_distrib.vendor_name AS vendor_name,
		soft_distrib.vendor_comments AS vendor_comments,
		soft_distrib.distrib_id AS distrib_id,
		soft_distrib.distrib_name AS distrib_name,
		soft_distrib.distrib_comments AS distrib_comments,
		file.size AS file_size,
		file.datetime AS datetime,
		file.md5 AS md5,
		file.mimetype AS mimetype,
		file.origfn AS origfn,
		file.ext AS ext
	FROM file LEFT JOIN (
		SELECT
			soft_vendor.id AS id,
			soft_vendor.name AS name,
			soft_vendor.ver AS ver,
			soft_vendor.platform_id AS platform_id,
			soft_vendor.platform_name AS platform_name,
			soft_vendor.platform_comments AS platform_comments,
			soft_vendor.vendor_id AS vendor_id,
			soft_vendor.vendor_name AS vendor_name,
			soft_vendor.vendor_comments AS vendor_comments,
			distrib.id AS distrib_id,
			distrib.name AS distrib_name,
			distrib.comments AS distrib_comments
		FROM distrib LEFT JOIN (
			SELECT
				soft_platform.id AS id,
				soft_platform.distrib_id AS distrib_id,
				soft_platform.name AS name,
				soft_platform.ver AS ver,
				soft_platform.platform_id AS platform_id,
				soft_platform.platform_name AS platform_name,
				soft_platform.platform_comments AS platform_comments,
				vendor.id AS vendor_id,
				vendor.name AS vendor_name,
				vendor.comments AS vendor_comments
			FROM vendor LEFT JOIN (
				SELECT
					programm.id AS id,
					programm.vendor AS vendor_id,
					programm.distrib AS distrib_id,
					programm.name AS name,
					programm.ver AS ver,
					platform.id AS platform_id,
					platform.name AS platform_name,
					platform.comments AS platform_comments
				FROM programm LEFT JOIN platform ON programm.platform = platform.id
			) AS soft_platform ON vendor.id = soft_platform.vendor_id
		) AS soft_vendor ON distrib.id = soft_vendor.distrib_id
	) AS soft_distrib ON file.id = soft_distrib.id
) AS soft_file ON object.id = soft_file.id
