import pandas as pd

file_path = "data/processed/youtube_topics.csv"

df = pd.read_csv(file_path)

print("=" * 70)
print("TOPIC-WISE COMMENT INSPECTION")
print("=" * 70)

for topic, group in df.groupby("topic"):

    print("\n" + "=" * 70)

    print("TOPIC:", topic)
    print("TOTAL COMMENTS:", len(group))

    print("-" * 70)

    for index, row in group.head(10).iterrows():

        text = str(row["original_text"])

        text = text.replace("\n", " ")

        print("\nComment:", text[:400])

print("\n" + "=" * 70)
print("INSPECTION COMPLETED")
print("=" * 70)