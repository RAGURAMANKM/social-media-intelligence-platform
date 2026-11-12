import os

import networkx as nx
from neo4j import GraphDatabase


# ==================================================
# 1. NEO4J CONNECTION
# ==================================================

URI = "bolt://localhost:7687"
USERNAME = "neo4j"

# Replace with your Neo4j password.
# DO NOT share your password with anyone.
PASSWORD = "Lava90909"


# ==================================================
# 2. GRAPH FILE
# ==================================================

GRAPH_FILE = (
    "data/processed/"
    "social_interaction_graph.graphml"
)


# ==================================================
# 3. CONNECT TO NEO4J
# ==================================================

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# ==================================================
# 4. CREATE CONSTRAINTS
# ==================================================

def create_constraints(session):

    session.run("""
        CREATE CONSTRAINT channel_id_unique
        IF NOT EXISTS
        FOR (c:Channel)
        REQUIRE c.id IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT video_id_unique
        IF NOT EXISTS
        FOR (v:Video)
        REQUIRE v.id IS UNIQUE
    """)

    session.run("""
        CREATE CONSTRAINT commenter_id_unique
        IF NOT EXISTS
        FOR (c:Commenter)
        REQUIRE c.id IS UNIQUE
    """)


# ==================================================
# 5. CLEAR EXISTING GRAPH
# ==================================================

def clear_database(session):

    print("\nClearing existing Neo4j graph...")

    session.run("""
        MATCH (n)
        DETACH DELETE n
    """)

    print("Existing graph cleared.")


# ==================================================
# 6. CREATE NODE
# ==================================================

def create_node(session, node_id, node_type, label):

    if node_type == "channel":

        session.run("""
            MERGE (n:Channel {id: $id})
            SET n.name = $label
        """,
        id=node_id,
        label=label
        )

    elif node_type == "video":

        session.run("""
            MERGE (n:Video {id: $id})
            SET n.video_id = $label
        """,
        id=node_id,
        label=label
        )

    elif node_type == "commenter":

        session.run("""
            MERGE (n:Commenter {id: $id})
            SET n.username = $label
        """,
        id=node_id,
        label=label
        )


# ==================================================
# 7. CREATE RELATIONSHIP
# ==================================================

def create_relationship(
    session,
    source_id,
    target_id,
    relationship
):

    if relationship == "publishes":

        session.run("""
            MATCH (a:Channel {id: $source_id})
            MATCH (b:Video {id: $target_id})

            MERGE (a)-[:PUBLISHES]->(b)
        """,
        source_id=source_id,
        target_id=target_id
        )

    elif relationship == "has_commenter":

        session.run("""
            MATCH (a:Video {id: $source_id})
            MATCH (b:Commenter {id: $target_id})

            MERGE (a)-[:HAS_COMMENTER]->(b)
        """,
        source_id=source_id,
        target_id=target_id
        )


# ==================================================
# 8. MAIN IMPORT PROCESS
# ==================================================

print("=" * 70)
print("NEO4J GRAPH IMPORT")
print("=" * 70)


if not os.path.exists(GRAPH_FILE):

    raise FileNotFoundError(
        f"GraphML file not found: {GRAPH_FILE}"
    )


print("\nLoading GraphML:")

print(GRAPH_FILE)


G = nx.read_graphml(GRAPH_FILE)

print("\nGraphML loaded successfully.")

print("Nodes:", G.number_of_nodes())

print("Edges:", G.number_of_edges())


with driver.session() as session:

    # --------------------------------------------------
    # Create constraints
    # --------------------------------------------------

    print("\nCreating Neo4j constraints...")

    create_constraints(session)

    print("Constraints created.")


    # --------------------------------------------------
    # Clear previous data
    # --------------------------------------------------

    clear_database(session)


    # --------------------------------------------------
    # Import nodes
    # --------------------------------------------------

    print("\nImporting nodes...")

    node_count = 0

    for node_id, attributes in G.nodes(
        data=True
    ):

        node_type = attributes.get(
            "node_type"
        )

        label = attributes.get(
            "label",
            node_id
        )

        create_node(
            session,
            node_id,
            node_type,
            label
        )

        node_count += 1

        if node_count % 50 == 0:

            print(
                f"Imported nodes: {node_count}"
            )


    print(
        f"Total nodes imported: {node_count}"
    )


    # --------------------------------------------------
    # Import relationships
    # --------------------------------------------------

    print("\nImporting relationships...")

    relationship_count = 0

    for source, target, attributes in G.edges(
        data=True
    ):

        relationship = attributes.get(
            "relationship"
        )

        create_relationship(
            session,
            source,
            target,
            relationship
        )

        relationship_count += 1

        if relationship_count % 50 == 0:

            print(
                f"Imported relationships: "
                f"{relationship_count}"
            )


    print(
        f"Total relationships imported: "
        f"{relationship_count}"
    )


# ==================================================
# 9. CLOSE CONNECTION
# ==================================================

driver.close()


# ==================================================
# 10. FINAL STATUS
# ==================================================

print("\n" + "=" * 70)
print("NEO4J IMPORT COMPLETED SUCCESSFULLY")
print("=" * 70)

print(
    f"Nodes imported: {node_count}"
)

print(
    f"Relationships imported: "
    f"{relationship_count}"
)

print("=" * 70)