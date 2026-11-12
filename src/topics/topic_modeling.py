import re
import html
import pandas as pd
import emoji

from sentence_transformers import SentenceTransformer

from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer

from sklearn.feature_extraction.text import CountVectorizer

from umap import UMAP
from hdbscan import HDBSCAN


INPUT_FILE = "data/processed/youtube_sentiment.csv"

OUTPUT_FILE = "data/processed/youtube_topics.csv"

SUMMARY_FILE = "data/processed/topic_summary.csv"


def clean_topic_text(text):

    if not isinstance(text, str):
        return ""

    # Remove emojis instead of converting them into descriptions
    text = emoji.replace_emoji(text, replace=" ")

    # Remove HTML entities
    text = html.unescape(text)

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", " ", text)

    # Lowercase
    text = text.lower()

    # Keep alphabetic words
    text = re.sub(r"[^a-z\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


print("=" * 55)
print("LOADING YOUTUBE COMMENTS")
print("=" * 55)

df = pd.read_csv(INPUT_FILE)

print("Total records:", len(df))

# Only use comments, not titles or descriptions
df = df[df["text_type"] == "comment"].copy()

print("Comment records:", len(df))

# Use original comments to avoid emoji descriptions
df["topic_text"] = df["original_text"].apply(clean_topic_text)

# Keep English comments
df = df[df["language"] == "en"].copy()

# Remove short comments
df["word_count"] = df["topic_text"].str.split().str.len()

df = df[df["word_count"] >= 6].copy()

# Remove duplicate comments
df = df.drop_duplicates(subset=["topic_text"])

# Remove empty records
df = df[df["topic_text"].str.strip() != ""]

documents = df["topic_text"].tolist()

print("English meaningful comments:", len(documents))

if len(documents) < 20:
    raise ValueError(
        "Not enough meaningful comments for topic modeling."
    )


print("\n" + "=" * 55)
print("LOADING EMBEDDING MODEL")
print("=" * 55)

embedding_model = SentenceTransformer(
    "paraphrase-multilingual-MiniLM-L12-v2"
)

print("Embedding model loaded successfully!")


print("\n" + "=" * 55)
print("CONFIGURING BERTOPIC")
print("=" * 55)


# Remove common and unhelpful words
custom_stopwords = [
    "the", "and", "for", "that", "this", "with",
    "you", "your", "are", "was", "were", "have",
    "has", "had", "but", "not", "they", "them",
    "their", "there", "what", "when", "where",
    "who", "why", "how", "can", "could", "would",
    "should", "will", "just", "like", "really",
    "one", "get", "got", "also", "know", "think",
    "see", "say", "said", "video", "watch",
    "watched", "youtube", "subscribe", "please",
    "thanks", "thank", "good", "great", "nice",
    "yes", "yeah", "lol", "oh", "im", "ive",
    "dont", "doesnt", "didnt", "its", "thats",
    "youre", "theyre", "amp"
]

vectorizer_model = CountVectorizer(
    stop_words=custom_stopwords,
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.85
)

umap_model = UMAP(
    n_neighbors=10,
    n_components=5,
    min_dist=0.0,
    metric="cosine",
    random_state=42
)

hdbscan_model = HDBSCAN(
    min_cluster_size=8,
    min_samples=2,
    metric="euclidean",
    cluster_selection_method="eom",
    prediction_data=True
)

ctfidf_model = ClassTfidfTransformer(
    reduce_frequent_words=True
)


print("\n" + "=" * 55)
print("STARTING BERTOPIC")
print("=" * 55)

topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    ctfidf_model=ctfidf_model,
    min_topic_size=8,
    nr_topics=None,
    calculate_probabilities=False,
    verbose=True
)

topics, probabilities = topic_model.fit_transform(documents)


print("\n" + "=" * 55)
print("TOPIC MODELING COMPLETED")
print("=" * 55)


# Save document-level topic results
df["topic"] = topics

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)


# Generate topic summary
topic_info = topic_model.get_topic_info()

topic_info.to_csv(
    SUMMARY_FILE,
    index=False,
    encoding="utf-8-sig"
)


# Display results
print("\nDocuments used:", len(documents))

number_of_topics = len(
    set(topics) - {-1}
)

print("Number of topics:", number_of_topics)

print("\nTopic distribution:")

print(
    topic_info[
        ["Topic", "Count", "Name"]
    ].to_string(index=False)
)


print("\nMain topic keywords:")

for topic_id in sorted(set(topics)):

    if topic_id == -1:
        continue

    keywords = topic_model.get_topic(topic_id)

    if keywords:

        print(f"\nTopic {topic_id}:")

        print(
            ", ".join(
                [word for word, score in keywords[:10]]
            )
        )


print("\nSaved successfully:")

print("1.", OUTPUT_FILE)

print("2.", SUMMARY_FILE)