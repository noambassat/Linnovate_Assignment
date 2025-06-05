# # app/utils/llm_client.py
import os
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_highlights_from_video(video_path: str) -> str:
    try:
        prompt = f"""Analyze this video segment and write the main event or action it contains.
        Segment path: {video_path} (this is for context, don't include in answer)."""

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert video content summarizer."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error extracting highlights from {video_path}: {e}")
        return ""