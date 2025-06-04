# app/utils/vision_summary.py

import cv2
import base64
from PIL import Image
from io import BytesIO
from openai import OpenAI

def extract_frame_middle(video_path: str) -> Image.Image:
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    mid = total // 2
    cap.set(cv2.CAP_PROP_POS_FRAMES, mid)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError(f"Could not extract frame from {video_path}")
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)

def image_to_base64(img: Image.Image) -> str:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def generate_description_from_video(video_path: str) -> str:
    image = extract_frame_middle(video_path)
    img_b64 = image_to_base64(image)

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You describe images from video scenes."},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
                    {"type": "text", "text": "What's happening in this scene? Describe briefly."}
                ]
            }
        ],
        max_tokens=100
    )

    return response.choices[0].message.content.strip()
