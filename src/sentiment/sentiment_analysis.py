import pandas as pd
import torch

from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# Project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Input and output files
INPUT_FILE = BASE_DIR / "data" / "processed" / "youtube_preprocessed.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "youtube_sentiment.csv"

# Multilingual sentiment model
MODEL_NAME = "cardiffnlp/xlm-roberta-base-sentiment-multilingual"


def load_sentiment_model():

    print("Loading multilingual sentiment model...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME
    )

    model.eval()

    print("Model loaded successfully!")

    return tokenizer, model


def predict_sentiment(text, tokenizer, model):

    inputs = tokenizer(
        str(text),
        return_tensors="pt",
        truncation=True,
        max_length=128
    )

    with torch.inference_mode():

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1
        )

    predicted_id = probabilities.argmax(dim=1).item()

    sentiment = model.config.id2label[predicted_id]

    confidence = probabilities[0][predicted_id].item()

    return sentiment, round(confidence, 4)


def run_sentiment_analysis():

    if not INPUT_FILE.exists():
        raise FileNotFoundError("Preprocessed CSV file not found.")

    # Read preprocessed data
    df = pd.read_csv(INPUT_FILE)

    if df.empty:
        raise ValueError("The input dataset is empty.")

    # Load model
    tokenizer, model = load_sentiment_model()

    sentiments = []
    confidence_scores = []

    print("\nStarting sentiment analysis...")

    for index, row in df.iterrows():

        text = row["cleaned_text"]

        sentiment, confidence = predict_sentiment(
            text,
            tokenizer,
            model
        )

        sentiments.append(sentiment)
        confidence_scores.append(confidence)

        print(
            f"Processed {index + 1}/{len(df)}: "
            f"{sentiment}"
        )

    # Add predictions
    df["sentiment"] = sentiments
    df["confidence"] = confidence_scores

    # Save results
    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nSentiment analysis completed!")

    print("Total records:", len(df))

    print("\nSentiment distribution:")
    print(df["sentiment"].value_counts())

    print("\nSaved file:", OUTPUT_FILE)


if __name__ == "__main__":

    run_sentiment_analysis()