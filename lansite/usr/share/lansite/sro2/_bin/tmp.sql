BEGIN;
ALTER TABLE sro2_sroown ADD COLUMN subtitle varchar(1000);
ALTER TABLE sro2_orgsro ADD COLUMN agent_id INTEGER REFERENCES sro2_agent (id);
CREATE INDEX sro2_orgsro_agent_id ON sro2_orgsro (agent_id);
COMMIT;