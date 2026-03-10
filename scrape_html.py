from bs4 import BeautifulSoup
import os


def scrape(input_file, output_file):
    if not os.path.exists(input_file):
        raise SystemExit(f"File not found: {input_file}")

    with open(input_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    lines = [line.strip() for line in text.splitlines()]
    cleaned = "\n".join(line for line in lines if line)

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"Scraped {input_file} -> {output_file}")
