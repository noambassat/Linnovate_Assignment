# app/processors/highlight_extractor.py

import os
from typing import List, Dict
from app.utils.vision_summary import generate_description_from_video
from app.utils.embedding import get_embedding
from app.utils.database import save_highlight_to_db
from app.utils.check_existence import highlight_exists


class HighlightExtractor:
    def __init__(self, segment_dir: str, video_id: str):
        self.segment_dir = segment_dir
        self.video_id = video_id

    def list_segments(self) -> List[str]:
        return [
            os.path.join(self.segment_dir, f)
            for f in sorted(os.listdir(self.segment_dir))
            if f.endswith(".mp4")
        ]

    def extract_all(self):
        segments = self.list_segments()
        for path in segments:
            if highlight_exists(self.video_id, path):
                print(f"Already exists in DB, skipping: {os.path.basename(path)}")
                continue
            try:
                highlight = self.process_segment(path)
                save_highlight_to_db(highlight)
                print(f"Saved highlight from {os.path.basename(path)}")
            except Exception as e:
                print(f"Error processing {path}: {e}")

    def process_segment(self, video_path: str) -> Dict:
        print(f"Extracting highlights from: {os.path.basename(video_path)}")

        description = generate_description_from_video(video_path)
        embedding = get_embedding(description)

        return {
            "video_id": self.video_id,
            "segment_path": os.path.basename(video_path),
            "timestamp": self.extract_timestamp_from_filename(video_path),
            "description": description,
            "embedding": embedding,
            "llm_summary": description,
        }

    def extract_timestamp_from_filename(self, filename: str) -> float:
        basename = os.path.basename(filename)
        parts = basename.replace(".mp4", "").split("_")
        try:
            return float(parts[-2])
        except Exception:
            return -1.0
