import networkx as nx
import pandas as pd
from pathlib import Path

print("=" * 70)
print("SOCIAL MEDIA GRAPH ANALYTICS")
print("=" * 70)

# --------------------------------------------------
# 1. LOAD GRAPH
# --------------------------------------------------

input_file = Path("data/processed/social_interaction_graph.graphml")

G = nx.read_graphml(input_file)

print("\nGraph loaded successfully!")
print("Total nodes:", G.number_of_nodes())
print("Total edges:", G.number_of_edges())

# --------------------------------------------------
# 2. DEGREE CENTRALITY
# --------------------------------------------------

print("\nCalculating Degree Centrality...")

degree_scores = nx.degree_centrality(G)

# --------------------------------------------------
# 3. PAGERANK
# --------------------------------------------------

print("Calculating PageRank...")

pagerank_scores = nx.pagerank(
    G,
    alpha=0.85,
    max_iter=100
)

# --------------------------------------------------
# 4. COMMUNITY DETECTION
# --------------------------------------------------

print("Detecting communities...")

undirected_graph = G.to_undirected()

communities = nx.community.greedy_modularity_communities(
    undirected_graph
)

community_mapping = {}

for community_id, community in enumerate(communities):
    for node in community:
        community_mapping[node] = community_id

print("Total communities detected:", len(communities))

# --------------------------------------------------
# 5. ADD ANALYTICS TO GRAPH
# --------------------------------------------------

for node in G.nodes():

    G.nodes[node]["degree_centrality"] = float(
        degree_scores[node]
    )

    G.nodes[node]["pagerank"] = float(
        pagerank_scores[node]
    )

    G.nodes[node]["community_id"] = int(
        community_mapping[node]
    )

# --------------------------------------------------
# 6. CREATE RESULTS DATAFRAME
# --------------------------------------------------

results = []

for node, attributes in G.nodes(data=True):

    results.append({
        "node_id": node,
        "node_type": attributes.get("node_type", "unknown"),
        "label": attributes.get("label", node),
        "degree_centrality": degree_scores[node],
        "pagerank": pagerank_scores[node],
        "community_id": community_mapping[node]
    })

df = pd.DataFrame(results)

# --------------------------------------------------
# 7. SAVE RESULTS
# --------------------------------------------------

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

csv_file = output_dir / "graph_analytics.csv"

df.to_csv(csv_file, index=False)

graph_file = output_dir / "social_interaction_graph_analytics.graphml"

nx.write_graphml(G, graph_file)

print("\nAnalytics files saved successfully!")
print("CSV:", csv_file)
print("GraphML:", graph_file)

# --------------------------------------------------
# 8. TOP 10 PAGERANK NODES
# --------------------------------------------------

print("\nTOP 10 NODES BY PAGERANK")

top_nodes = df.sort_values(
    by="pagerank",
    ascending=False
).head(10)

print(
    top_nodes[
        ["label", "node_type", "pagerank", "degree_centrality", "community_id"]
    ].to_string(index=False)
)

# --------------------------------------------------
# 9. COMMUNITY DISTRIBUTION
# --------------------------------------------------

print("\nCOMMUNITY DISTRIBUTION")

community_summary = (
    df.groupby("community_id")
    .size()
    .reset_index(name="node_count")
    .sort_values("node_count", ascending=False)
)

print(community_summary.to_string(index=False))

# --------------------------------------------------
# 10. NODE TYPE DISTRIBUTION
# --------------------------------------------------

print("\nNODE TYPE DISTRIBUTION")

print(df["node_type"].value_counts())

print("\n" + "=" * 70)
print("GRAPH ANALYTICS COMPLETED SUCCESSFULLY!")
print("=" * 70)