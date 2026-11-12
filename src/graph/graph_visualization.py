import os
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd


# ============================================================
# SOCIAL MEDIA GRAPH VISUALIZATION
# ============================================================

print("=" * 70)
print("SOCIAL MEDIA GRAPH VISUALIZATION")
print("=" * 70)


# ============================================================
# 1. LOAD GRAPH
# ============================================================

INPUT_FILE = "data/processed/social_interaction_graph_analytics.graphml"

OUTPUT_DIR = "reports/graph_visualizations"

os.makedirs(OUTPUT_DIR, exist_ok=True)

G = nx.read_graphml(INPUT_FILE)

print("\nGraph loaded successfully!")

print("Total nodes:", G.number_of_nodes())
print("Total edges:", G.number_of_edges())


# ============================================================
# 2. PREPARE GRAPH
# ============================================================

# Convert graph to undirected for visualization

UG = G.to_undirected()

# Extract node attributes

communities = nx.get_node_attributes(G, "community_id")

pagerank = nx.get_node_attributes(G, "pagerank")

degree = nx.get_node_attributes(G, "degree_centrality")

node_types = nx.get_node_attributes(G, "node_type")

labels = nx.get_node_attributes(G, "label")


# ============================================================
# 3. GENERATE GRAPH LAYOUT
# ============================================================

print("\nGenerating graph layout...")

pos = nx.spring_layout(
    UG,
    seed=42,
    k=0.25,
    iterations=100
)


# ============================================================
# 4. COMMUNITY-BASED GRAPH VISUALIZATION
# ============================================================

print("\nCreating community visualization...")

plt.figure(figsize=(18, 14))

community_values = [
    int(communities[node])
    for node in UG.nodes()
]

node_sizes = [
    100 + (degree.get(node, 0) * 1500)
    for node in UG.nodes()
]

nx.draw_networkx_edges(
    UG,
    pos,
    alpha=0.15,
    edge_color="gray"
)

nodes = nx.draw_networkx_nodes(
    UG,
    pos,
    node_size=node_sizes,
    node_color=community_values,
    cmap=plt.cm.tab20,
    alpha=0.9
)

# Label top 15 influential nodes

top_nodes = sorted(
    pagerank,
    key=pagerank.get,
    reverse=True
)[:15]

top_labels = {
    node: labels.get(node, node)
    for node in top_nodes
}

nx.draw_networkx_labels(
    UG,
    pos,
    labels=top_labels,
    font_size=8,
    font_weight="bold"
)

plt.colorbar(
    nodes,
    label="Community ID"
)

plt.title(
    "Social Media Interaction Network - Communities",
    fontsize=18
)

plt.axis("off")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "social_network_communities.png"
    ),
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 5. NODE TYPE VISUALIZATION
# ============================================================

print("Creating node type visualization...")

node_type_counts = pd.Series(
    list(node_types.values())
).value_counts()

plt.figure(figsize=(10, 6))

node_type_counts.plot(
    kind="bar",
    edgecolor="black"
)

plt.title("Social Network - Node Type Distribution")

plt.xlabel("Node Type")

plt.ylabel("Number of Nodes")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "node_type_distribution.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 6. TOP 10 PAGERANK NODES
# ============================================================

print("Creating PageRank visualization...")

pagerank_df = pd.DataFrame({
    "Node": list(pagerank.keys()),
    "PageRank": list(pagerank.values())
})

pagerank_df["Label"] = pagerank_df["Node"].map(
    lambda node: labels.get(node, node)
)

pagerank_df = pagerank_df.sort_values(
    by="PageRank",
    ascending=False
).head(10)

plt.figure(figsize=(12, 7))

plt.barh(
    pagerank_df["Label"],
    pagerank_df["PageRank"],
    edgecolor="black"
)

plt.gca().invert_yaxis()

plt.title("Top 10 Influential Nodes - PageRank")

plt.xlabel("PageRank Score")

plt.ylabel("Node")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "top_10_pagerank.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 7. TOP 10 DEGREE CENTRALITY NODES
# ============================================================

print("Creating degree centrality visualization...")

degree_df = pd.DataFrame({
    "Node": list(degree.keys()),
    "Degree Centrality": list(degree.values())
})

degree_df["Label"] = degree_df["Node"].map(
    lambda node: labels.get(node, node)
)

degree_df = degree_df.sort_values(
    by="Degree Centrality",
    ascending=False
).head(10)

plt.figure(figsize=(12, 7))

plt.barh(
    degree_df["Label"],
    degree_df["Degree Centrality"],
    edgecolor="black"
)

plt.gca().invert_yaxis()

plt.title("Top 10 Nodes - Degree Centrality")

plt.xlabel("Degree Centrality")

plt.ylabel("Node")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "top_10_degree_centrality.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 8. COMMUNITY DISTRIBUTION
# ============================================================

print("Creating community distribution visualization...")

community_df = pd.DataFrame({
    "Community": list(communities.values())
})

community_counts = community_df[
    "Community"
].value_counts().sort_index()

plt.figure(figsize=(12, 6))

community_counts.plot(
    kind="bar",
    edgecolor="black"
)

plt.title("Social Network Community Distribution")

plt.xlabel("Community ID")

plt.ylabel("Number of Nodes")

plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "community_distribution.png"
    ),
    dpi=300
)

plt.close()


# ============================================================
# 9. COMPLETION
# ============================================================

print("\nVisualization files saved successfully!")

print("\nOutput Directory:", OUTPUT_DIR)

print("\nGenerated Files:")

for file in os.listdir(OUTPUT_DIR):

    print(" -", file)


print("\n" + "=" * 70)

print("GRAPH VISUALIZATION COMPLETED SUCCESSFULLY!")

print("=" * 70)