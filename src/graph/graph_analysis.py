import json
import glob
import os

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# ==================================================
# 1. CONFIGURATION
# ==================================================

RAW_FOLDER = "data/raw/youtube"

PROCESSED_FOLDER = "data/processed"

DASHBOARD_FOLDER = "dashboards"

CENTRALITY_FILE = os.path.join(
    PROCESSED_FOLDER,
    "graph_centrality.csv"
)

GRAPH_FILE = os.path.join(
    PROCESSED_FOLDER,
    "social_interaction_graph.graphml"
)

IMAGE_FILE = os.path.join(
    DASHBOARD_FOLDER,
    "social_interaction_network.png"
)


os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(DASHBOARD_FOLDER, exist_ok=True)


# ==================================================
# 2. FIND LATEST YOUTUBE JSON FILE
# ==================================================

files = glob.glob(
    os.path.join(RAW_FOLDER, "*.json")
)

if not files:
    raise FileNotFoundError(
        "No YouTube raw JSON files found."
    )

latest_file = max(
    files,
    key=os.path.getmtime
)

print("=" * 70)
print("YOUTUBE SOCIAL INTERACTION GRAPH ANALYSIS")
print("=" * 70)

print("\nLoading latest file:", latest_file)


# ==================================================
# 3. LOAD RAW JSON DATA
# ==================================================

with open(
    latest_file,
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)


videos = data.get("videos", [])

print("Total videos:", len(videos))


# ==================================================
# 4. CREATE DIRECTED GRAPH
# ==================================================

G = nx.DiGraph()

total_comments = 0

valid_comments = 0

unique_commenter_video_relationships = 0

unique_commenters = set()

unique_videos = set()

unique_channels = set()


for video in videos:

    video_id = str(
        video.get("video_id", "")
    ).strip()

    channel_name = str(
        video.get("channel_name", "Unknown")
    ).strip()

    if not video_id:
        continue

    # Create node IDs

    channel_node = f"channel:{channel_name}"

    video_node = f"video:{video_id}"

    unique_videos.add(video_id)

    unique_channels.add(channel_name)


    # --------------------------------------------------
    # Add channel node
    # --------------------------------------------------

    G.add_node(
        channel_node,
        node_type="channel",
        label=channel_name
    )


    # --------------------------------------------------
    # Add video node
    # --------------------------------------------------

    G.add_node(
        video_node,
        node_type="video",
        label=video_id
    )


    # --------------------------------------------------
    # Channel publishes video
    # --------------------------------------------------

    G.add_edge(
        channel_node,
        video_node,
        relationship="publishes"
    )


    # --------------------------------------------------
    # Extract comments
    # --------------------------------------------------

    comments = video.get("comments", [])

    for comment in comments:

        total_comments += 1

        author = str(
            comment.get("author", "")
        ).strip()

        if not author:
            continue

        valid_comments += 1

        author_node = f"commenter:{author}"

        unique_commenters.add(author)


        # --------------------------------------------------
        # Add commenter node
        # --------------------------------------------------

        G.add_node(
            author_node,
            node_type="commenter",
            label=author
        )


        # --------------------------------------------------
        # Video receives comments from commenter
        # --------------------------------------------------

        if not G.has_edge(video_node, author_node):

            G.add_edge(
                video_node,
                author_node,
                relationship="has_commenter"
            )

            unique_commenter_video_relationships += 1


# ==================================================
# 5. GRAPH STATISTICS
# ==================================================

print("\n" + "=" * 70)
print("GRAPH STATISTICS")
print("=" * 70)

print("Total nodes:", G.number_of_nodes())

print("Total edges:", G.number_of_edges())

print("Total comments extracted:", total_comments)

print("Comments with valid authors:", valid_comments)

print(
    "Unique commenter-video relationships:",
    unique_commenter_video_relationships
)

print("Unique channels:", len(unique_channels))

print("Unique videos:", len(unique_videos))

print("Unique commenters:", len(unique_commenters))


# ==================================================
# 6. NODE DISTRIBUTION
# ==================================================

node_types = {}

for node, attributes in G.nodes(data=True):

    node_type = attributes.get(
        "node_type",
        "unknown"
    )

    node_types[node_type] = (
        node_types.get(node_type, 0) + 1
    )


print("\nNode Distribution:")

for node_type, count in node_types.items():

    print(f"{node_type}: {count}")


# ==================================================
# 7. CENTRALITY CALCULATIONS
# ==================================================

print("\nCalculating centrality measures...")


degree_centrality = nx.degree_centrality(G)

pagerank = nx.pagerank(
    G,
    alpha=0.85
)


results = []

for node, attributes in G.nodes(data=True):

    results.append({

        "Node": node,

        "Node_Type": attributes.get(
            "node_type"
        ),

        "Label": attributes.get(
            "label"
        ),

        "Degree_Centrality": degree_centrality.get(
            node,
            0
        ),

        "PageRank": pagerank.get(
            node,
            0
        )

    })


centrality_df = pd.DataFrame(results)


centrality_df = centrality_df.sort_values(
    by="PageRank",
    ascending=False
)


# ==================================================
# 8. SAVE CENTRALITY RESULTS
# ==================================================

centrality_df.to_csv(
    CENTRALITY_FILE,
    index=False
)

print("\nCentrality CSV saved:", CENTRALITY_FILE)


# ==================================================
# 9. TOP 10 COMMENTERS
# ==================================================

commenter_df = centrality_df[
    centrality_df["Node_Type"] == "commenter"
].copy()


commenter_df = commenter_df.sort_values(
    by="PageRank",
    ascending=False
)


print("\n" + "=" * 70)
print("TOP 10 COMMENTERS BY PAGERANK")
print("=" * 70)


if len(commenter_df) > 0:

    print(
        commenter_df.head(10).to_string(
            index=False
        )
    )

else:

    print("No commenters found.")


# ==================================================
# 10. SAVE GRAPH AS GRAPHML
# ==================================================

nx.write_graphml(
    G,
    GRAPH_FILE
)

print("\nGraphML file saved:", GRAPH_FILE)


# ==================================================
# 11. NETWORK VISUALIZATION
# ==================================================

print("\nGenerating network visualization...")


plt.figure(figsize=(16, 12))


pos = nx.spring_layout(
    G,
    seed=42,
    k=0.8
)


node_colors = []

for node, attributes in G.nodes(data=True):

    node_type = attributes.get(
        "node_type"
    )

    if node_type == "channel":

        node_colors.append("skyblue")

    elif node_type == "video":

        node_colors.append("lightgreen")

    else:

        node_colors.append("orange")


nx.draw_networkx(
    G,
    pos,
    node_color=node_colors,
    node_size=500,
    font_size=6,
    arrows=True,
    with_labels=False,
    edge_color="gray",
    alpha=0.8
)


plt.title(
    "YouTube Social Interaction Network",
    fontsize=16
)

plt.axis("off")

plt.tight_layout()


plt.savefig(
    IMAGE_FILE,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("Network visualization saved:", IMAGE_FILE)


# ==================================================
# 12. FINAL STATUS
# ==================================================

print("\n" + "=" * 70)
print("GRAPH ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)

print("1. Centrality CSV generated")

print("2. GraphML file generated")

print("3. Network visualization generated")

print("4. PageRank calculated")

print("5. Top commenters identified")

print("=" * 70)