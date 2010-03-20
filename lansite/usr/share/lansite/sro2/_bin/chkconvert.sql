BEGIN;
SELECT 'SRC:';
SELECT 'Src.Org', COUNT() FROM sro_org;
SELECT 'Src.Bld.StageLists', COUNT() FROM sro_permit;
SELECT 'Src.Bld.StageLists.MaxID', MAX(id) FROM sro_permit;
SELECT 'Src.Bld.StageLists.Stages', COUNT() FROM sro_permitstage;
SELECT 'Src.Bld.StageLists.Stages.MaxID', MAX(permit_id) FROM sro_permitstage;
SELECT 'Src.Bld.Proto', COUNT() FROM sro_meeting;
SELECT 'Src.Prj.Orgs', COUNT() FROM sro_prjorg;
SELECT 'Src.Prj.StageLists', COUNT() FROM (SELECT DISTINCT org_id FROM sro_prjorgstage);
SELECT 'Src.Prj.StageLists.MaxID', MAX(org_id) FROM sro_prjorgstage;
SELECT 'Src.Prj.StageLists.Stages', COUNT() FROM sro_prjorgstage;
SELECT 'Src.Prj.StageLists.Stages.MaxID', MAX(org_id) FROM sro_prjorgstage;
SELECT 'Src.Prj.Proto', COUNT() FROM sro_prjproto;
SELECT 'DST:';
SELECT 'Dst.Orgs', COUNT() FROM sro2_org;
SELECT 'Dst.StageLists', COUNT() FROM sro2_stagelist;
SELECT 'Dst.StageLists.MaxID', MAX(id) FROM sro2_stagelist;
SELECT 'Dst.StageLists.Stages', COUNT() FROM sro2_permitstage;
SELECT 'Dst.StageLists.Stages.MaxID', MAX(stagelist_id) FROM sro2_permitstage;
SELECT 'Dst.Bld.Orgs', COUNT() FROM sro2_orgsro WHERE (sro_id=1);
SELECT 'Dst.Bld.Proto', COUNT() FROM sro2_protocol WHERE (sro_id=1);
SELECT 'Dst.Bld.StageLists', COUNT() FROM (SELECT *, sro2_orgsro.sro_id AS sro_id FROM sro2_stagelist JOIN sro2_orgsro ON sro2_stagelist.orgsro_id = sro2_orgsro.id WHERE sro_id = 1);
SELECT 'Dst.Bld.StageLists.MaxID', MAX(id) FROM (SELECT *, sro2_orgsro.sro_id AS sro_id FROM sro2_stagelist JOIN sro2_orgsro ON sro2_stagelist.orgsro_id = sro2_orgsro.id WHERE sro_id = 1);
SELECT 'Dst.Bld.StageLists.Stages', COUNT() FROM (SELECT *, sro2_orgsro.sro_id AS sro_id FROM sro2_permitstage JOIN sro2_stagelist ON sro2_permitstage.stagelist_id = sro2_stagelist.id JOIN sro2_orgsro ON sro2_stagelist.orgsro_id = sro2_orgsro.id WHERE sro_id = 1);
SELECT 'Dst.Bld.StageLists.Stages.MaxID', MAX(stagelist_id) FROM (SELECT *, sro2_orgsro.sro_id AS sro_id FROM sro2_permitstage JOIN sro2_stagelist ON sro2_permitstage.stagelist_id = sro2_stagelist.id JOIN sro2_orgsro ON sro2_stagelist.orgsro_id = sro2_orgsro.id WHERE sro_id = 1);
SELECT 'Dst.Prj.Orgs', COUNT() FROM sro2_orgsro WHERE (sro_id=2);
SELECT 'Dst.Prj.Proto', COUNT() FROM sro2_protocol WHERE (sro_id=2);
SELECT 'Dst.Prj.StageLists', COUNT() FROM (SELECT *, sro2_orgsro.sro_id AS sro_id FROM sro2_stagelist JOIN sro2_orgsro ON sro2_stagelist.orgsro_id = sro2_orgsro.id WHERE sro_id = 2);
SELECT 'Dst.Prj.StageLists.MinID', MIN(id) FROM (SELECT *, sro2_orgsro.sro_id AS sro_id FROM sro2_stagelist JOIN sro2_orgsro ON sro2_stagelist.orgsro_id = sro2_orgsro.id WHERE sro_id = 2);
SELECT 'Dst.Prj.StageLists.MaxID', MAX(id) FROM (SELECT *, sro2_orgsro.sro_id AS sro_id FROM sro2_stagelist JOIN sro2_orgsro ON sro2_stagelist.orgsro_id = sro2_orgsro.id WHERE sro_id = 2);
SELECT 'Dst.Prj.StageLists.Stages', COUNT() FROM (SELECT *, sro2_orgsro.sro_id AS sro_id FROM sro2_permitstage JOIN sro2_stagelist ON sro2_permitstage.stagelist_id = sro2_stagelist.id JOIN sro2_orgsro ON sro2_stagelist.orgsro_id = sro2_orgsro.id WHERE sro_id = 2);
SELECT 'Dst.Prj.StageLists.Stages.MinID', MIN(stagelist_id) FROM (SELECT *, sro2_orgsro.sro_id AS sro_id FROM sro2_permitstage JOIN sro2_stagelist ON sro2_permitstage.stagelist_id = sro2_stagelist.id JOIN sro2_orgsro ON sro2_stagelist.orgsro_id = sro2_orgsro.id WHERE sro_id = 2);
SELECT 'Dst.Prj.StageLists.Stages.MaxID', MAX(stagelist_id) FROM (SELECT *, sro2_orgsro.sro_id AS sro_id FROM sro2_permitstage JOIN sro2_stagelist ON sro2_permitstage.stagelist_id = sro2_stagelist.id JOIN sro2_orgsro ON sro2_stagelist.orgsro_id = sro2_orgsro.id WHERE sro_id = 2);
COMMIT;