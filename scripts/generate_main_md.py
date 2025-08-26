import os
import sys
from datetime import datetime

# Minimal client using OpenAI's Python SDK.
# Requires: pip install openai
from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # set the model you want
OUTPUT_PATH = os.getenv("OUTPUT_PATH", "MAIN.md")
PROMPT_FILE = os.getenv("PROMPT_FILE", "prompt.md")

def load_prompt():
    if not os.path.exists(PROMPT_FILE):
        sys.stderr.write(f"Prompt file not found: {PROMPT_FILE}\n")
        sys.exit(1)
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()

def write_file(text: str):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text.strip() + "\n")

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        sys.stderr.write("OPENAI_API_KEY not set\n")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    prompt = load_prompt()

    # Single-shot generation. Keep it boring and deterministic-ish.
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a meticulous technical writer."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    content = resp.choices[0].message.content
    if not content:
        sys.stderr.write("No content generated.\n")
        sys.exit(1)

    write_file(content)
    print(f"[{datetime.utcnow().isoformat()}Z] Wrote {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
