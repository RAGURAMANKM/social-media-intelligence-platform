import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


# --------------------------------------------------
# STEP 1: LOAD TOPIC MODELLING RESULTS
# --------------------------------------------------

input_file = Path("data/processed/youtube_topics.csv")

if not input_file.exists():
    raise FileNotFoundError(
        "Topic modelling output not found. "
        "Run topic_modeling.py first."
    )

df = pd.read_csv(input_file)

print("Total records:", len(df))


# --------------------------------------------------
# STEP 2: CHECK REQUIRED COLUMNS
# --------------------------------------------------

required_columns = ["published_at", "topic"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing required column: {column}")


# --------------------------------------------------
# STEP 3: CONVERT PUBLISHING DATE
# --------------------------------------------------

df["published_at"] = pd.to_datetime(
    df["published_at"],
    errors="coerce",
    utc=True
)

df = df.dropna(subset=["published_at", "topic"]).copy()

df["topic"] = df["topic"].astype(int)

df["published_date"] = df["published_at"].dt.date

print("Valid records:", len(df))


# --------------------------------------------------
# STEP 4: CREATE TOPIC LABELS
# --------------------------------------------------

def get_topic_name(topic_id):

    if topic_id == -1:
        return "Outlier"

    return f"Topic {topic_id}"


df["topic_name"] = df["topic"].apply(get_topic_name)


# --------------------------------------------------
# STEP 5: CALCULATE TOPIC DISTRIBUTION
# --------------------------------------------------

topic_distribution = (
    df["topic_name"]
    .value_counts()
    .reset_index()
)

topic_distribution.columns = [
    "Topic",
    "Document_Count"
]

print("\nTopic Distribution:")

print(topic_distribution)


# --------------------------------------------------
# STEP 6: SAVE TOPIC DISTRIBUTION
# --------------------------------------------------

output_directory = Path("dashboards")

output_directory.mkdir(
    parents=True,
    exist_ok=True
)

topic_distribution.to_csv(
    "data/processed/topic_distribution.csv",
    index=False
)


# --------------------------------------------------
# STEP 7: CREATE TOPIC TREND DATA
# --------------------------------------------------

topic_trends = (
    df.groupby(["published_date", "topic_name"])
    .size()
    .reset_index(name="document_count")
)

print("\nTopic Trends:")

print(topic_trends)


# --------------------------------------------------
# STEP 8: CREATE PIVOT TABLE
# --------------------------------------------------

trend_pivot = topic_trends.pivot(
    index="published_date",
    columns="topic_name",
    values="document_count"
).fillna(0)

trend_pivot = trend_pivot.sort_index()

print("\nTopic Trend Table:")

print(trend_pivot)


# --------------------------------------------------
# STEP 9: SAVE TOPIC TREND DATA
# --------------------------------------------------

trend_pivot.to_csv(
    "data/processed/topic_trends.csv"
)


# --------------------------------------------------
# STEP 10: VISUALIZE TOPIC DISTRIBUTION
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    topic_distribution["Topic"],
    topic_distribution["Document_Count"]
)

plt.title("YouTube Topic Distribution")

plt.xlabel("Topics")

plt.ylabel("Number of Documents")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig(
    "dashboards/topic_distribution.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# STEP 11: VISUALIZE TOPIC TRENDS OVER TIME
# --------------------------------------------------

plt.figure(figsize=(12, 6))

for topic in trend_pivot.columns:

    plt.plot(
        trend_pivot.index.astype(str),
        trend_pivot[topic],
        marker="o",
        label=topic
    )

plt.title("YouTube Topic Trends Over Time")

plt.xlabel("Published Date")

plt.ylabel("Number of Documents")

plt.xticks(rotation=45)

plt.legend(title="Topics")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "dashboards/topic_trends_over_time.png",
    dpi=300
)

plt.close()


# --------------------------------------------------
# STEP 12: FINAL OUTPUT
# --------------------------------------------------

print("\nTopic trend analysis completed successfully!")

print("\nGenerated files:")

print("1. data/processed/topic_distribution.csv")

print("2. data/processed/topic_trends.csv")

print("3. dashboards/topic_distribution.png")

print("4. dashboards/topic_trends_over_time.png")