import os
import networkx as nx
from pyvis.network import Network


# ============================================================
# INTERACTIVE SOCIAL MEDIA GRAPH
# ============================================================

print("=" * 70)
print("INTERACTIVE SOCIAL MEDIA GRAPH VISUALIZATION")
print("=" * 70)


# ============================================================
# 1. LOAD GRAPH
# ============================================================

INPUT_FILE = "data/processed/social_interaction_graph_analytics.graphml"

OUTPUT_DIR = "reports/graph_visualizations"

os.makedirs(OUTPUT_DIR, exist_ok=True)

G = nx.read_graphml(INPUT_FILE)

print("\nGraph loaded successfully!")

print("Total Nodes:", G.number_of_nodes())
print("Total Edges:", G.number_of_edges())


# ============================================================
# 2. CREATE PYVIS NETWORK
# ============================================================

net = Network(
    height="850px",
    width="100%",
    directed=G.is_directed(),
    bgcolor="#111827",
    font_color="white",
    notebook=False
)


# ============================================================
# 3. NODE COLORS
# ============================================================

node_colors = {
    "commenter": "#3498DB",
    "channel": "#2ECC71",
    "video": "#E67E22"
}


# ============================================================
# 4. ADD NODES
# ============================================================

print("\nAdding graph nodes...")

for node, attributes in G.nodes(data=True):

    node_type = attributes.get("node_type", "unknown")

    label = attributes.get("label", str(node))

    pagerank = float(
        attributes.get("pagerank", 0)
    )

    degree = float(
        attributes.get("degree_centrality", 0)
    )

    community = attributes.get(
        "community_id", "unknown"
    )

    color = node_colors.get(
        node_type, "#95A5A6"
    )

    size = 10 + (degree * 100)

    tooltip = f"""
    <b>Node:</b> {label}<br>
    <b>Node Type:</b> {node_type}<br>
    <b>PageRank:</b> {pagerank:.6f}<br>
    <b>Degree Centrality:</b> {degree:.6f}<br>
    <b>Community:</b> {community}
    """

    net.add_node(
        node,
        label=str(label),
        title=tooltip,
        color=color,
        size=size,
        group=str(community)
    )


# ============================================================
# 5. ADD EDGES
# ============================================================

print("Adding graph edges...")

for source, target, attributes in G.edges(data=True):

    net.add_edge(
        source,
        target,
        color="#64748B",
        width=1
    )


# ============================================================
# 6. PHYSICS SETTINGS
# ============================================================

net.set_options("""
{
    "nodes": {
        "font": {
            "size": 12
        },
        "borderWidth": 1
    },
    "edges": {
        "smooth": {
            "type": "dynamic"
        },
        "color": {
            "inherit": false
        }
    },
    "physics": {
        "enabled": true,
        "barnesHut": {
            "gravitationalConstant": -3000,
            "centralGravity": 0.2,
            "springLength": 120,
            "springConstant": 0.04,
            "damping": 0.09
        },
        "stabilization": {
            "enabled": true,
            "iterations": 150
        }
    },
    "interaction": {
        "hover": true,
        "navigationButtons": true,
        "keyboard": true,
        "tooltipDelay": 200
    }
}
""")


# ============================================================
# 7. SAVE INTERACTIVE GRAPH
# ============================================================

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "social_interaction_network.html"
)

net.write_html(
    OUTPUT_FILE,
    notebook=False,
    open_browser=False
)


# ============================================================
# 8. COMPLETION
# ============================================================

print("\nInteractive graph saved successfully!")

print("Output File:", OUTPUT_FILE)

print("Total Nodes:", len(net.nodes))

print("Total Edges:", len(net.edges))

print("\n" + "=" * 70)

print("INTERACTIVE GRAPH VISUALIZATION COMPLETED!")

print("=" * 70)