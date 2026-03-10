import json
import os
import re

PROMPT = """You are a flashcard generator. Extract all key educational concepts from the text below and return ONLY a JSON array of flashcards. No explanation, no markdown, just raw JSON.

Format:
[
  {{
    "front": "Short term or concept name",
    "back": [
      "Full name / definition",
      "Additional detail or context",
      "Example (if relevant)"
    ]
  }}
]

Text:
{text}"""


def extract_json(raw):
    raw = raw.strip()
    match = re.search(r'```(?:json)?\s*([\s\S]+?)```', raw)
    if match:
        raw = match.group(1).strip()
    return json.loads(raw)


def run_claude(text, model="claude-haiku-4-5-20251001"):
    try:
        import anthropic
    except ImportError:
        raise SystemExit("Anthropic SDK not installed. Run: pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY environment variable not set.")

    print(f"Running with Claude ({model})...")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": PROMPT.format(text=text)}]
    )
    return extract_json(message.content[0].text)


def autogenerate(output_name, model=None):
    input_file = "web/page.txt"
    if not os.path.exists(input_file):
        raise SystemExit(f"File not found: {input_file}. Run 'scrape' first.")

    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    cards = run_claude(text, model=model or "claude-haiku-4-5-20251001")

    if not isinstance(cards, list):
        raise SystemExit("Model did not return a JSON array. Try again.")

    os.makedirs("sets", exist_ok=True)
    if not output_name.endswith(".json"):
        output_name += ".json"
    output_path = os.path.join("sets", output_name)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cards, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(cards)} flashcards -> {output_path}")
    return output_name
