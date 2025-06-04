# Video Highlight Extractor with LLM and pgvector

## Overview

This project processes videos to extract descriptive highlights using a Large Language Model (LLM). It stores metadata and semantic embeddings in a PostgreSQL database enhanced with pgvector for similarity-based search.

---

## Features

-  Segments input videos into short clips
-  Uses OpenAI GPT-4o to describe each video segment
-  Stores results in PostgreSQL with pgvector
-  Modular, object-oriented architecture
-  Docker-based setup for reproducibility

---

## Directory Structure

```
Home_Assignment/
├── app/
│   ├── __init__.py
│   ├── processors/
│   │   ├── video_ingestor.py
│   │   ├── video_splitter.py
│   │   └── highlight_extractor.py
│   ├── utils/
│   │   ├── vision_summary.py
│   │   ├── database.py
│   │   ├── embedding.py
│   │   └── check_existence.py
├── input_data/
│   ├── video_files/         # Input videos (30–90 sec)
│   └── temp_segments/       # Auto-split segments
├── docker/
│   └── sql/
│       └── init.sql         # DB schema (creates "highlights" table)
├── docker-compose.yml
├── requirements.txt
├── main.py                  # Runs the full pipeline
├── run_demo.py              # Demo script for evaluation
└── README.md
```

---

## How It Works

1. **Segmenting Videos:**  
   Each video is split into 5-second clips using `moviepy`.

2. **Describing Segments:**  
   The middle frame of each clip is sent to OpenAI GPT-4o to generate a description.

3. **Storing to DB:**  
   Metadata and embeddings are inserted into PostgreSQL (`highlights` table).

4. **Avoiding Duplication:**  
   Before inserting, the system checks if a segment already exists in the DB.

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/VideoHighlightExtractor.git
cd VideoHighlightExtractor
```

### 2. Add Your Videos

Place at least two `.mp4` or `.mov` files (30–90 seconds long) in:

```
input_data/video_files/
```

### 3. Add Your OpenAI API Key

Create a `.env` file:

```env
OPENAI_API_KEY=your-key-here
```

### 4. Start Docker Services

```bash
docker-compose up -d
```

This starts PostgreSQL with the `highlights` table via `init.sql`.

### 5. Install Python Requirements

```bash
pip install -r requirements.txt
```

---

## Run the Demo

```bash
python run_demo.py
```

Or run the main pipeline directly:

```bash
python main.py
```

---

## Database Schema

The `highlights` table:

```sql
CREATE TABLE IF NOT EXISTS highlights (
    id SERIAL PRIMARY KEY,
    video_id TEXT,
    segment_path TEXT,
    timestamp FLOAT,
    description TEXT,
    embedding VECTOR(1536),
    llm_summary TEXT
);
```

---

## Notes

- You must upload the demo with at least **two videos**.
- All processing must run from Python using LLMs (no manual text).
- Only visual data is used (no audio).

