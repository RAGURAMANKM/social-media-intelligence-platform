import json
from pathlib import Path

import pandas as pd

from text_cleaning import clean_text, detect_language


# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Input and output directories
INPUT_DIR = BASE_DIR / "data" / "raw" / "youtube"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def preprocess_youtube_data():

    # Find collected JSON files
    json_files = sorted(INPUT_DIR.glob("*.json"))

    if not json_files:
        raise FileNotFoundError("No YouTube JSON files found.")

    # Read the latest JSON file
    input_file = json_files[-1]

    print("Reading file:", input_file.name)

    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    processed_records = []

    # Process each video
    for video in data.get("videos", []):

        video_id = video.get("video_id")

        common_data = {
            "video_id": video_id,
            "channel_name": video.get("channel_name"),
            "published_at": video.get("published_at"),
            "view_count": video.get("view_count")
        }

        # Process title and description
        text_fields = [
            ("title", video.get("title")),
            ("description", video.get("description"))
        ]

        for text_type, original_text in text_fields:

            cleaned = clean_text(original_text)

            if cleaned:
                processed_records.append({
                    **common_data,
                    "text_type": text_type,
                    "original_text": original_text,
                    "cleaned_text": cleaned,
                    "language": detect_language(cleaned)
                })

        # Process comments
        for comment in video.get("comments", []):

            original_text = comment.get("text", "")
            cleaned = clean_text(original_text)

            if cleaned:
                processed_records.append({
                    **common_data,
                    "text_type": "comment",
                    "original_text": original_text,
                    "cleaned_text": cleaned,
                    "language": detect_language(cleaned)
                })

    # Convert records into DataFrame
    df = pd.DataFrame(processed_records)

    # Save processed dataset
    output_file = OUTPUT_DIR / "youtube_preprocessed.csv"

    df.to_csv(output_file, index=False, encoding="utf-8-sig")

    print("\nPreprocessing completed!")
    print("Total processed text records:", len(df))
    print("Output file:", output_file)

    if not df.empty:
        print("\nText type distribution:")
        print(df["text_type"].value_counts())

        print("\nLanguage distribution:")
        print(df["language"].value_counts())


if __name__ == "__main__":
    preprocess_youtube_data()