
# Video Highlight Extractor with LLM and pgvector

## Overview
This project extracts descriptive highlights from videos using a Large Language Model (LLM) and enables interactive querying over the extracted content. Each video is segmented, analyzed visually using OpenAI GPT-4o, and stored with semantic embeddings in PostgreSQL using `pgvector`. The project also includes a web-based chat interface to ask questions about the highlights.

---

## Workflow

```mermaid
Video File
   ↓
Split into 5-sec Segments
   ↓
Extract Middle Frame (Image)
   ↓
Send to GPT-4o → Get Description
   ↓
Embed Description (text-embedding-3-small)
   ↓
Save to PostgreSQL (with pgvector)
   ↓
User asks question → Embed it → Search similar vectors → Return matching segments
```

## Features

- LLM-based description for visual content (no audio).
- Video segmentation using `moviepy`.
- Storage of metadata and embeddings in PostgreSQL with `pgvector`.
- Semantic similarity search over highlights.
- Clean modular architecture (OOP).
- Dockerized environment for both backend and frontend.
- Interactive React frontend for asking questions about the video content.

---

## Directory Structure

```
Home_Assignment/
├── app/
│   ├── api/
│   │   └── chat_router.py          # FastAPI endpoint for chat
│   ├── db/
│   │   └── pgvector_client.py      # Query highlights with similarity search
│   ├── processors/
│   │   ├── video_ingestor.py       # Input + segmentation orchestration
│   │   ├── video_splitter.py       # Splits videos into segments
│   │   └── highlight_extractor.py  # Handles LLM + embedding + saving
│   ├── utils/
│   │   ├── check_existence.py
│   │   ├── database.py
│   │   ├── embedding.py
│   │   ├── vision_summary.py
│   │   └── main_chat.py            # FastAPI app entrypoint
├── input_data/
│   ├── video_files/                # Input videos (30–90 sec)
│   └── temp_segments/              # Auto-split segments
├── docker/
│   └── sql/
│       └── init.sql                # Schema creation
├── frontend/
│   ├── Dockerfile                  # React-based UI
│   ├── package.json
│   ├── vite.config.js
│   └── main.jsx                    # UI source code
├── docker-compose.yml
├── requirements.txt
├── Dockerfile                      # Backend service
├── run_demo.py                     # Demo: split + process videos
├── main.py                         # Same as run_demo but cleaner
└── README.md
```

---

## How It Works

### Step 1: Video Highlight Extraction
1. Each input video is split into fixed-duration segments (default 5 seconds).
2. The middle frame of each segment is sent to OpenAI GPT-4o for visual description.
3. The description is embedded using `text-embedding-3-small`.
4. The result is stored in PostgreSQL, including:
   - `video_id`
   - `segment_path`
   - `timestamp`
   - `description` (visual)
   - `embedding` (vector)
   - `llm_summary`

### Step 2: Interactive Chat
- A React UI allows users to ask questions like "What happens with the dolphin?"
- FastAPI receives the query and embeds it.
- The system searches the database for the most similar highlights (`embedding <-> query_embedding`).
- The UI displays matching results and summaries (from the DB only, no LLM at runtime).

---

## Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/your-username/VideoHighlightExtractor.git
cd VideoHighlightExtractor
```

### 2. Add Input Videos
Place at least two `.mp4` or `.mov` files (30–90 seconds each) into:
```
input_data/video_files/
```

If the files are too large to include in the repository, see the section below for external hosting.

### 3. Create a .env file
```env
OPENAI_API_KEY=your-api-key-here
```

### 4. Start the System with Docker
```bash
docker-compose up --build
```

- FastAPI will be available at: http://localhost:8000/docs
- UI will be available at: http://localhost:3000

---

## Run the Demo Pipeline (optional)
```bash
python run_demo.py
```

Or directly:
```bash
python main.py
```

---

## API Usage

### POST `/chat`

Query the highlights using semantic similarity:

**Request:**
```json
{
  "query": "Describe the dolphin moment",
  "top_k": 3
}
```

**Response:**
```json
{
  "matches": [
    {
      "video_id": "example_1",
      "segment_path": "video_1_10_15.mp4",
      "timestamp": 10,
      "description": "A dolphin leaps through the wave",
      "summary": "A dolphin leaps through the wave"
    }
  ]
}
```

---

## Database Schema

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

- Embedding model: `text-embedding-3-small`
- Image description: `gpt-4o` using base64 image encoding
- All input is visual (no audio or speech-to-text)
- Chat is powered by semantic search only (no LLM call during chat)

---

## Demo Videos

Due to file size limitations on GitHub, the input videos are hosted externally.

You can access and download the required video files from this folder:

https://drive.google.com/drive/folders/1B2FQkMrVHcpoZFO3oVzSZHk9b1XDoxNz?usp=drive_link

Place them manually in the directory:

```
input_data/video_files/
```

---

