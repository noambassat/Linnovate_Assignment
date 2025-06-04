# demo/run_demo.py

import os
from app.processors.video_ingestor import ensure_directory, get_video_files, process_video
from app.processors.highlight_extractor import HighlightExtractor

VIDEO_DIR = "input_data/video_files"
SEGMENTS_DIR = "input_data/temp_segments"

def run_demo():
    ensure_directory(SEGMENTS_DIR)
    video_files = get_video_files(VIDEO_DIR)

    if not video_files:
        print("No video files found.")
        return

    # Step 1: Split videos into segments
    for video_path in video_files:
        print(f"Splitting video: {os.path.basename(video_path)}")
        process_video(video_path, SEGMENTS_DIR)

    # Step 2: Extract highlights
    for video_path in video_files:
        video_id = os.path.basename(video_path).split(".")[0]
        extractor = HighlightExtractor(segment_dir=SEGMENTS_DIR, video_id=video_id)
        extractor.extract_all()

    print("Demo pipeline completed.")

if __name__ == "__main__":
    run_demo()
# This script runs the demo pipeline for video processing and highlight extraction.