# scripts/convert_notes.py
import os
import glob
from datetime import datetime
from openai import OpenAI

client = OpenAI()

DRAFTS_DIR = "content/drafts"
POSTS_DIR = "posts"

def call_openai(prompt_text):
    response = client.responses.create(
        prompt={
            "id": "pmpt_686f5b452dfc8196b0bd7ec522997c4b0d825a0ed93c110e",
            "version": "2",
            "input": {"note": prompt_text}
        }
    )
    return response.choices[0].message.content.strip()

def process_drafts():
    os.makedirs(POSTS_DIR, exist_ok=True)
    drafts = glob.glob(f"{DRAFTS_DIR}/*.md")

    for path in drafts:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        result = call_openai(content)

        filename = os.path.basename(path)
        date_prefix = datetime.now().strftime("%Y-%m-%d")
        output_file = os.path.join(POSTS_DIR, f"{date_prefix}-{filename}")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)

if __name__ == "__main__":
    process_drafts()
