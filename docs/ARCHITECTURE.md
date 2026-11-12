\# System Architecture



\## 1. Project Overview



The Social Media Intelligence Platform is a modular Python application that collects and analyzes YouTube data using text analytics, topic modeling, graph analytics, and Neo4j.



\## 2. Processing Architecture



YouTube Data Collection

&#x20;       |

&#x20;       v

Text Preprocessing

&#x20;       |

&#x20;       +---------------------+

&#x20;       |                     |

&#x20;       v                     v

Sentiment Analysis      Topic Modeling

&#x20;       |                     |

&#x20;       v                     v

Sentiment Trends        Topic Trends

&#x20;       |                     |

&#x20;       +----------+----------+

&#x20;                  |

&#x20;                  v

&#x20;      Social Interaction Graph

&#x20;                  |

&#x20;                  v

&#x20;          NetworkX Analytics

&#x20;                  |

&#x20;                  v

&#x20;         Graph Visualization

&#x20;                  |

&#x20;                  v

&#x20;             GraphML

&#x20;                  |

&#x20;                  v

&#x20;            Neo4j Database



\## 3. Project Modules



| Module | Directory | Purpose |

|---|---|---|

| Data Ingestion | src/ingestion/ | Collect YouTube data |

| Preprocessing | src/preprocessing/ | Clean collected text |

| Sentiment | src/sentiment/ | Analyze sentiment |

| Topics | src/topics/ | Discover discussion topics |

| Graph | src/graph/ | Construct and analyze networks |

| Misinformation | src/misinformation/ | Reserved for future development |

| Search | src/search/ | Reserved for future development |



\## 4. Graph Data Model



Node types:

\- Channel

\- Video

\- Commenter



Relationships:

\- Channel -\[:PUBLISHES]-> Video

\- Video -\[:HAS\_COMMENTER]-> Commenter



\## 5. Storage Architecture



\- data/raw/ : Original collected data

\- data/processed/ : Processed datasets and graph files

\- dashboards/ : Generated analytical visualizations

\- reports/graph\_visualizations/ : Graph reports and interactive visualizations



\## 6. Database Integration



NetworkX graph data is exported in GraphML format and imported into Neo4j for graph storage and exploration.



\## 7. Security



\- API keys and database credentials are stored in a local .env file.

\- .env is excluded from Git.

\- Virtual environments and raw collected data are excluded from Git.

