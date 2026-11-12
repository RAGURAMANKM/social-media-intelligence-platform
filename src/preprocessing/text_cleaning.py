import re
import html
import emoji

from langdetect import detect, LangDetectException
from langdetect import DetectorFactory

DetectorFactory.seed = 42


def clean_text(text):

    if not isinstance(text, str):
        return ""

    # Convert HTML entities into normal text
    text = html.unescape(text)

    # Convert emojis into meaningful words
    text = emoji.demojize(text, delimiters=(" ", " "))

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Convert text to lowercase
    text = text.lower()

    # Replace underscores from emoji names
    text = text.replace("_", " ")

    # Remove unnecessary special characters
    text = re.sub(r"[^\w\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


def detect_language(text):

    if not isinstance(text, str):
        return "unknown"

    text = text.strip()

    if len(text.split()) < 5:
        return "unknown"

    try:
        return detect(text)

    except LangDetectException:
        return "unknown"


if __name__ == "__main__":

    sample_text = "Artificial intelligence is transforming technology and changing the way people work every day."

    cleaned = clean_text(sample_text)

    language = detect_language(cleaned)

    print("Original text:", sample_text)
    print("Cleaned text:", cleaned)
    print("Detected language:", language)