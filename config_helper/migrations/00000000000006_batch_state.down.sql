CREATE TYPE COLLECTION_JOB_STATE_NEW AS ENUM(
    'START',
    'FINISHED',
    'ABANDONED',
    'DELETED'
);
ALTER TABLE collection_jobs ALTER COLUMN state TYPE COLLECTION_JOB_STATE_NEW
    USING (state::text::COLLECTION_JOB_STATE_NEW);
DROP TYPE COLLECTION_JOB_STATE;
ALTER TYPE COLLECTION_JOB_STATE_NEW RENAME TO COLLECTION_JOB_STATE;

DROP TABLE batches;
DROP TYPE BATCH_STATE CASCADE;