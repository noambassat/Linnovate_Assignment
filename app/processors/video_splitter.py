# app/processors/video_splitter.py

from moviepy.editor import VideoFileClip
import os
from typing import List, Tuple

class VideoSplitter:
    def __init__(self, video_path: str, segment_duration: int = 5):
        self.video_path = video_path
        self.segment_duration = segment_duration
        self.clip = VideoFileClip(video_path)

    def split_video(self) -> List[Tuple[float, float]]:
        """
        Splits the video into segments of fixed duration.
        Returns a list of (start_time, end_time) tuples.
        """
        total_duration = self.clip.duration
        segments = []
        start = 0.0
        while start < total_duration:
            end = min(start + self.segment_duration, total_duration)
            segments.append((start, end))
            start = end
        return segments

    def extract_segment(self, start: float, end: float, output_dir: str) -> str:
        """
        Extracts a segment from the video and saves it to the output directory.
        Returns the path to the saved segment file.
        """
        base_name = os.path.splitext(os.path.basename(self.video_path))[0]
        filename = f"{base_name}_{int(start)}_{int(end)}.mp4"
        output_path = os.path.join(output_dir, filename)
        self.clip.subclip(start, end).write_videofile(output_path, codec='libx264', audio=False, verbose=False, logger=None)
        return output_path

    def close(self):
        """
        Releases the video clip resource.
        """
        self.clip.close()
