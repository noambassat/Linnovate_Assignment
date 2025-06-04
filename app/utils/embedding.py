# app/utils/embedding.py

from openai import OpenAI
import os


api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_embedding(text: str) -> list:
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return []
