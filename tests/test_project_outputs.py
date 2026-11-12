from pathlib import Path

import networkx as nx
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"

GRAPH_FILE = DATA_DIR / "social_interaction_graph_analytics.graphml"


def test_processed_files_exist():
    expected_files = [
        "graph_analytics.csv",
        "graph_centrality.csv",
        "social_interaction_graph.graphml",
        "social_interaction_graph_analytics.graphml",
        "topic_distribution.csv",
        "topic_summary.csv",
        "topic_trends.csv",
        "youtube_network.graphml",
        "youtube_preprocessed.csv",
        "youtube_sentiment.csv",
        "youtube_topics.csv",
    ]

    for filename in expected_files:
        file_path = DATA_DIR / filename

        assert file_path.exists(), f"Missing file: {filename}"
        assert file_path.stat().st_size > 0, f"Empty file: {filename}"


def test_graph_node_count():
    graph = nx.read_graphml(GRAPH_FILE)

    assert graph.number_of_nodes() == 362


def test_graph_edge_count():
    graph = nx.read_graphml(GRAPH_FILE)

    assert graph.number_of_edges() == 352


def test_graph_node_types():
    graph = nx.read_graphml(GRAPH_FILE)

    node_types = {
        data.get("node_type")
        for _, data in graph.nodes(data=True)
    }

    assert node_types == {"channel", "video", "commenter"}


def test_graph_relationship_types():
    graph = nx.read_graphml(GRAPH_FILE)

    relationships = {
        data.get("relationship")
        for _, _, data in graph.edges(data=True)
    }

    assert relationships == {"publishes", "has_commenter"}


def test_graph_is_directed():
    graph = nx.read_graphml(GRAPH_FILE)

    assert graph.is_directed()


def test_graph_analytics_columns():
    file_path = DATA_DIR / "graph_analytics.csv"

    df = pd.read_csv(file_path)

    required_columns = {
        "node_id",
        "node_type",
        "label",
        "degree_centrality",
        "pagerank",
        "community_id",
    }

    assert required_columns.issubset(set(df.columns))


def test_sentiment_columns():
    file_path = DATA_DIR / "youtube_sentiment.csv"

    df = pd.read_csv(file_path)

    required_columns = {
        "video_id",
        "channel_name",
        "sentiment",
        "confidence",
    }

    assert required_columns.issubset(set(df.columns))


def test_topic_columns():
    file_path = DATA_DIR / "youtube_topics.csv"

    df = pd.read_csv(file_path)

    required_columns = {
        "video_id",
        "channel_name",
        "topic",
    }

    assert required_columns.issubset(set(df.columns))