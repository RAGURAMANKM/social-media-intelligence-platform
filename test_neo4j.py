from neo4j import GraphDatabase


# ==================================================
# NEO4J CONNECTION SETTINGS
# ==================================================

URI = "bolt://localhost:7687"
USERNAME = "neo4j"

# IMPORTANT:
# Replace ONLY the value below with the password
# you created when setting up your Neo4j database.
PASSWORD = "Lava90909"


# ==================================================
# TEST CONNECTION
# ==================================================

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


try:

    driver.verify_connectivity()

    print("=" * 60)
    print("NEO4J CONNECTION SUCCESSFUL")
    print("=" * 60)

    print("URI:", URI)
    print("Username:", USERNAME)
    print("Database connection is working.")


except Exception as e:

    print("=" * 60)
    print("NEO4J CONNECTION FAILED")
    print("=" * 60)

    print("Error:", e)


finally:

    driver.close()