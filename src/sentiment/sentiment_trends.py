import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load sentiment dataset
input_file = Path("data/processed/youtube_sentiment.csv")
df = pd.read_csv(input_file)

# Create output folder
output_folder = Path("dashboards")
output_folder.mkdir(exist_ok=True)

# --------------------------------
# 1. Overall Sentiment Distribution
# --------------------------------

sentiment_counts = df["sentiment"].value_counts()

plt.figure(figsize=(8, 5))
sentiment_counts.plot(kind="bar")

plt.title("Overall Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Records")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(output_folder / "sentiment_distribution.png")
plt.show()

# --------------------------------
# 2. Sentiment by Language
# --------------------------------

language_sentiment = pd.crosstab(
    df["language"],
    df["sentiment"]
)

language_sentiment.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Sentiment Distribution by Language")
plt.xlabel("Language")
plt.ylabel("Number of Records")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(output_folder / "sentiment_by_language.png")
plt.show()

# --------------------------------
# 3. Sentiment Trends Over Time
# --------------------------------

df["published_at"] = pd.to_datetime(
    df["published_at"],
    errors="coerce",
    utc=True
)

df = df.dropna(subset=["published_at"])

df["published_date"] = df["published_at"].dt.date

daily_sentiment = pd.crosstab(
    df["published_date"],
    df["sentiment"]
)

daily_sentiment.plot(
    kind="line",
    marker="o",
    figsize=(12, 6)
)

plt.title("Sentiment Trends Over Time")
plt.xlabel("Published Date")
plt.ylabel("Number of Records")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(output_folder / "sentiment_over_time.png")
plt.show()

print("\nSentiment trend analysis completed!")

print("\nOverall sentiment:")
print(sentiment_counts)

print("\nSentiment by language:")
print(language_sentiment)

print("\nCharts saved inside dashboards folder.")