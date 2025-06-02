# app/processors/video_ingestor.py

import os
from typing import List
from app.processors.video_splitter import VideoSplitter

ALLOWED_EXTENSIONS = (".mp4", ".mov", ".avi", ".mkv")

def ensure_directory(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def get_video_files(directory: str) -> List[str]:
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(ALLOWED_EXTENSIONS)
    ]

def process_video(video_path: str, output_dir: str, segment_duration: int = 5):
    print(f"Processing: {os.path.basename(video_path)}")
    splitter = VideoSplitter(video_path, segment_duration=segment_duration)
    segments = splitter.split_video()
    print(f"Total segments: {len(segments)}")

    for idx, (start, end) in enumerate(segments):
        print(f"Segment {idx + 1}/{len(segments)}: {start:.2f}s → {end:.2f}s")
        output_path = splitter.extract_segment(start, end, output_dir)
        print(f"Saved to: {output_path}")

    splitter.close()
