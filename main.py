# main.py
import os

from app.processors.video_ingestor import ensure_directory, get_video_files, process_video
from app.processors.highlight_extractor import HighlightExtractor

VIDEO_DIR = "input_data/video_files"
SEGMENTS_DIR = "input_data/temp_segments"

def main():
    ensure_directory(SEGMENTS_DIR)
    video_files = get_video_files(VIDEO_DIR)

    if not video_files:
        print("No video files found in input_data/video_files/")
        return

    # ----- Step 1: Segment the videos -----
    # This block already ran — kept here for reference only.
    # for video_path in video_files:
    #     process_video(video_path, SEGMENTS_DIR)

    # ----- Step 2: Extract Highlights with LLM -----
    for video_path in video_files:
        video_id = os.path.basename(video_path).split(".")[0]
        extractor = HighlightExtractor(segment_dir=SEGMENTS_DIR, video_id=video_id)
        extractor.extract_all()

    print("Highlight extraction complete.")

if __name__ == "__main__":
    main()
