import re
from typing import List, Tuple


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return [(alt, url) for alt, url in matches]


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    pattern = r"(?<!\!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return [(anchor_text, url) for anchor_text, url in matches]
