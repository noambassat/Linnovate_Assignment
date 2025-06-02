# main.py

from app.processors.video_ingestor import ensure_directory, get_video_files, process_video

VIDEO_DIR = "input_data/video_files"
OUTPUT_DIR = "input_data/temp_segments"

def main():
    ensure_directory(OUTPUT_DIR)
    video_files = get_video_files(VIDEO_DIR)

    if not video_files:
        print("No video files found in input_data/video_files/")
        return

    for video_path in video_files:
        process_video(video_path, OUTPUT_DIR)

    print("Done.")

if __name__ == "__main__":
    main()
