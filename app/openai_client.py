import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set. Add it to your .env file.")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def clean_json(text: str) -> str:
    """
    Removes markdown fences, JSON labels, and extra text around the array.
    """
    if text is None:
        raise ValueError("Response content is empty.")

    text = text.strip()

    # First, strip any markdown fences around the payload.
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text, flags=re.IGNORECASE)

    # If the model added a leading "json" label after the fence, strip it.
    if text.lower().startswith("json"):
        text = text[4:].lstrip()

    # Try to extract the actual JSON array if the model added extra commentary.
    match = re.search(r"\[[\s\S]*\]", text)
    if match:
        text = match.group(0)

    return text.strip()

def generate_flashcards(topic: str):
    prompt = f"""
    Create exactly 10 flashcards for the topic "{topic}".

    RULES:
    - Return ONLY valid JSON
    - No explanation
    - No markdown
    - Format exactly like below

    [
      {{ "question": "Question text", "answer": "Answer text" }}
    ]
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )

    raw_output = response.choices[0].message.content
    if raw_output is None:
        raise ValueError("OpenAI returned no content.")

    cleaned_output = clean_json(raw_output)

    try:
        return json.loads(cleaned_output)
    except json.JSONDecodeError as exc:
        raise ValueError(f"OpenAI returned invalid JSON: {cleaned_output[:200]}") from exc
