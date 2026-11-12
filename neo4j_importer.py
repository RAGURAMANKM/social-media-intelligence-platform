import networkx as nx

from neo4j import GraphDatabase
from getpass import getpass
from collections import defaultdict


# ============================================================
# NEO4J CONNECTION SETTINGS
# ============================================================

URI = "bolt://localhost:7687"
USERNAME = "neo4j"

PASSWORD = getpass("Enter your Neo4j password: ")

GRAPH_FILE = (
    "data/processed/"
    "social_interaction_graph_analytics.graphml"
)


# ============================================================
# IMPORT SETTINGS
# ============================================================

NODE_LABELS = {
    "channel": "Channel",
    "video": "Video",
    "commenter": "Commenter"
}

RELATIONSHIP_TYPES = {
    "publishes": "PUBLISHES",
    "has_commenter": "HAS_COMMENTER"
}

BATCH_SIZE = 100


# ============================================================
# LOAD GRAPH
# ============================================================

print("=" * 70)
print("SOCIAL MEDIA INTELLIGENCE PLATFORM")
print("NEO4J GRAPH IMPORTER")
print("=" * 70)

print("\nLoading NetworkX graph...")

G = nx.read_graphml(GRAPH_FILE)

print("Graph loaded successfully!")
print("Total nodes:", G.number_of_nodes())
print("Total edges:", G.number_of_edges())


# ============================================================
# PREPARE NODE DATA
# ============================================================

nodes_by_type = defaultdict(list)

for node_id, attributes in G.nodes(data=True):

    node_type = attributes.get("node_type")

    if node_type not in NODE_LABELS:
        raise ValueError(
            f"Unknown node type: {node_type}"
        )

    properties = {
        key: value
        for key, value in attributes.items()
        if value is not None
    }

    properties["id"] = str(node_id)

    nodes_by_type[node_type].append({
        "id": str(node_id),
        "properties": properties
    })


# ============================================================
# PREPARE RELATIONSHIP DATA
# ============================================================

relationships_by_type = defaultdict(list)

for source, target, attributes in G.edges(data=True):

    relationship = attributes.get("relationship")

    if relationship not in RELATIONSHIP_TYPES:
        raise ValueError(
            f"Unknown relationship type: {relationship}"
        )

    relationships_by_type[relationship].append({
        "source": str(source),
        "target": str(target)
    })


# ============================================================
# NEO4J IMPORT FUNCTIONS
# ============================================================

def create_constraints(session):

    print("\nCreating uniqueness constraints...")

    for label in NODE_LABELS.values():

        query = (
            f"CREATE CONSTRAINT {label.lower()}_id_unique "
            f"IF NOT EXISTS "
            f"FOR (n:{label}) "
            f"REQUIRE n.id IS UNIQUE"
        )

        session.run(query).consume()

    print("Constraints created successfully!")


def import_nodes(session):

    print("\n" + "=" * 70)
    print("IMPORTING NODES")
    print("=" * 70)

    total_imported = 0

    for node_type, nodes in nodes_by_type.items():

        label = NODE_LABELS[node_type]

        print(
            f"\nImporting {label} nodes:",
            len(nodes)
        )

        query = f"""
        UNWIND $batch AS row

        MERGE (n:{label} {{id: row.id}})

        SET n += row.properties
        """

        for start in range(0, len(nodes), BATCH_SIZE):

            batch = nodes[
                start:start + BATCH_SIZE
            ]

            session.run(
                query,
                batch=batch
            ).consume()

            total_imported += len(batch)

        print(f"{label} nodes imported successfully!")

    print("\nTotal nodes processed:", total_imported)

    return total_imported


def import_relationships(session):

    print("\n" + "=" * 70)
    print("IMPORTING RELATIONSHIPS")
    print("=" * 70)

    total_imported = 0

    for relationship, edges in relationships_by_type.items():

        relationship_type = RELATIONSHIP_TYPES[relationship]

        print(
            f"\nImporting {relationship_type}:",
            len(edges)
        )

        query = f"""
        UNWIND $batch AS row

        MATCH (source {{id: row.source}})
        MATCH (target {{id: row.target}})

        MERGE (source)-[r:{relationship_type}]->(target)
        """

        for start in range(0, len(edges), BATCH_SIZE):

            batch = edges[
                start:start + BATCH_SIZE
            ]

            session.run(
                query,
                batch=batch
            ).consume()

            total_imported += len(batch)

        print(
            f"{relationship_type} relationships imported!"
        )

    print(
        "\nTotal relationships processed:",
        total_imported
    )

    return total_imported


# ============================================================
# VERIFY NEO4J DATA
# ============================================================

def verify_import(session):

    print("\n" + "=" * 70)
    print("VERIFYING NEO4J DATABASE")
    print("=" * 70)

    result = session.run("""
        MATCH (n)
        RETURN labels(n) AS NodeType, count(n) AS Count
        ORDER BY NodeType
    """)

    print("\nNODE DISTRIBUTION:")

    for record in result:

        print(
            record["NodeType"],
            ":",
            record["Count"]
        )

    result = session.run("""
        MATCH ()-[r]->()
        RETURN type(r) AS RelationshipType,
               count(r) AS Count
        ORDER BY RelationshipType
    """)

    print("\nRELATIONSHIP DISTRIBUTION:")

    for record in result:

        print(
            record["RelationshipType"],
            ":",
            record["Count"]
        )

    result = session.run("""
        MATCH (n)
        RETURN count(n) AS TotalNodes
    """)

    total_nodes = result.single()["TotalNodes"]

    result = session.run("""
        MATCH ()-[r]->()
        RETURN count(r) AS TotalRelationships
    """)

    total_relationships = result.single()[
        "TotalRelationships"
    ]

    print("\n" + "=" * 70)
    print("FINAL DATABASE COUNTS")
    print("=" * 70)

    print("Total nodes:", total_nodes)
    print("Total relationships:", total_relationships)

    return total_nodes, total_relationships


# ============================================================
# MAIN EXECUTION
# ============================================================

driver = None

try:

    print("\nConnecting to Neo4j...")

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    driver.verify_connectivity()

    print("Neo4j connection successful!")

    with driver.session() as session:

        create_constraints(session)

        import_nodes(session)

        import_relationships(session)

        total_nodes, total_relationships = verify_import(
            session
        )

    print("\n" + "=" * 70)

    if (
        total_nodes == G.number_of_nodes()
        and total_relationships == G.number_of_edges()
    ):

        print("NEO4J GRAPH IMPORT COMPLETED SUCCESSFULLY!")

    else:

        print("WARNING: IMPORT COUNTS DO NOT MATCH!")

    print("=" * 70)

except Exception as error:

    print("\n" + "=" * 70)
    print("NEO4J IMPORT FAILED")
    print("=" * 70)

    print("Error:", error)

finally:

    if driver:
        driver.close()

    print("\nNeo4j connection closed.")