CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS highlights (
    id SERIAL PRIMARY KEY,
    video_id TEXT NOT NULL,
    segment_path TEXT NOT NULL,
    timestamp FLOAT NOT NULL,
    description TEXT,
    embedding VECTOR(1536),
    llm_summary TEXT
);
