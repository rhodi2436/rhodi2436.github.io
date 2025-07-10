import os
import glob
import re
from datetime import datetime
from openai import OpenAI

client = OpenAI()

DRAFTS_DIR = "_content/drafts"
POSTS_DIR = "_posts"

def call_openai(prompt_text):
    response = client.responses.create(
        prompt={
            "id": "pmpt_686f5b452dfc8196b0bd7ec522997c4b0d825a0ed93c110e",
            "version": "2",
        },
        input=prompt_text
    )
    return response.output_text

def extract_title_and_date(md_text):
    front_matter = re.search(r"---\s*\n(.*?)\n---", md_text, re.DOTALL)
    if not front_matter:
        raise ValueError("找不到 front matter")

    content = front_matter.group(1)
    title_match = re.search(r"title:\s*(.*)", content)
    date_match = re.search(r"date:\s*(\d{4}-\d{2}-\d{2})", content)

    title = title_match.group(1).strip() if title_match else "untitled"
    date = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")

    return title, date

def slugify(text):
    text = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text.strip())  # 保留中英文、数字、下划线、连字符
    return re.sub(r"[-]+", "-", text).strip("-")

def process_drafts():
    os.makedirs(POSTS_DIR, exist_ok=True)
    drafts = glob.glob(f"{DRAFTS_DIR}/*.md")

    for path in drafts:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        result = call_openai(content)

        try:
            title, date = extract_title_and_date(result)
        except ValueError as e:
            print(f"跳过 {path}，因为无法解析标题: {e}")
            continue

        filename = f"{date}-{slugify(title)}.md"
        output_path = os.path.join(POSTS_DIR, filename)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"✅ 已生成：{output_path}")

if __name__ == "__main__":
    process_drafts()
