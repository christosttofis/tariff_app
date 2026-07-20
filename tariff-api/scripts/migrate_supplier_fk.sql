-- One-time migration: add supplier_id FK columns to users and message_reads,
-- backfilled from the existing supplier_name string columns.
--
-- Run manually via psql (no Alembic in this project — schema changes to
-- existing tables are applied by hand; Base.metadata.create_all only creates
-- missing tables, it does not add columns to existing ones).
--
-- BACK UP THE DATABASE BEFORE RUNNING THIS (tariff-api\scripts\backup_db.ps1).
--
-- The old supplier_name columns are intentionally left in place after this
-- script — they are dropped in a later, separate migration once the
-- supplier_id-based code path has been verified in production.

ALTER TABLE users ADD COLUMN IF NOT EXISTS supplier_id INTEGER REFERENCES suppliers(id);
ALTER TABLE message_reads ADD COLUMN IF NOT EXISTS supplier_id INTEGER REFERENCES suppliers(id);

UPDATE users u SET supplier_id = s.id
FROM suppliers s
WHERE u.supplier_name = s.name AND u.supplier_id IS NULL;

UPDATE message_reads mr SET supplier_id = s.id
FROM suppliers s
WHERE mr.supplier_name = s.name AND mr.supplier_id IS NULL;

-- Verification — both of these must return 0 rows before the code that
-- relies on supplier_id is deployed.
SELECT id, email, supplier_name FROM users WHERE role = 'supplier' AND supplier_id IS NULL;
SELECT id, message_id, supplier_name FROM message_reads WHERE supplier_id IS NULL;
