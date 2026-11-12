# Social Media Intelligence Platform

An end-to-end social media intelligence project that collects YouTube data, analyzes audience sentiment, discovers discussion topics, tracks topic trends, and explores social interaction networks using graph analytics and Neo4j.

## Project Overview

The platform analyzes YouTube channel, video, and commenter relationships to extract insights from collected social media data.

### Implemented Modules

1. **YouTube Data Collection** – Collects YouTube video and comment data.
2. **Text Preprocessing** – Cleans and prepares collected text.
3. **Sentiment Analysis** – Analyzes sentiment in YouTube comments.
4. **Topic Modeling** – Identifies discussion topics.
5. **Topic Trend Analysis** – Examines topic distributions and trends.
6. **Social Network Construction** – Builds a graph of channels, videos, and commenters.
7. **Graph Analytics** – Uses NetworkX to calculate graph metrics and communities.
8. **Graph Visualization** – Generates static and interactive network visualizations.
9. **Neo4j Integration** – Imports the graph into a Neo4j database for graph exploration.

## Technology Stack

- Python
- Pandas and NumPy
- Scikit-learn
- NetworkX
- Matplotlib
- Plotly
- Streamlit (dependency available)
- YouTube Data API
- Neo4j
- GraphML
- HTML, JavaScript and CSS

## Project Structure

```text
social-media-intelligence-platform/
│
├── dashboards/
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   ├── ARCHITECTURE.md
│   └── GRAPH_ANALYTICS_REPORT.md
├── lib/
├── models/
├── notebooks/
├── reports/
│   └── graph_visualizations/
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   ├── sentiment/
│   ├── topics/
│   ├── graph/
│   ├── misinformation/
│   └── search/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
git clone YOUR_GITHUB_REPOSITORY_URL
cd social-media-intelligence-platform
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt

## Step 2 — Create architecture documentation

Run:

```powershell
@'
# System Architecture

## 1. Overview

The Social Media Intelligence Platform follows a modular data processing architecture.

## 2. Processing Pipeline

```text
YouTube Data Source
        |
        v
Data Ingestion
        |
        v
Text Preprocessing
        |
        +--------------------+
        |                    |
        v                    v
Sentiment Analysis     Topic Modeling
        |                    |
        v                    v
Sentiment Trends       Topic Trends
        |                    |
        +---------+----------+
                  |
                  v
       Social Interaction Graph
                  |
                  v
           NetworkX Analytics
                  |
          +-------+-------+
          |               |
          v               v
    Graph Metrics    Visualization
          |
          v
       GraphML Export
          |
          v
      Neo4j Database

## Step 3 — Create graph analytics report

Run:

```powershell
@'
# Graph Analytics Results Report

## 1. Executive Summary

The social interaction graph was constructed from the collected YouTube dataset and imported successfully into Neo4j.

The final graph contains 362 nodes and 352 directed relationships.

## 2. Dataset Overview

| Node Type | Count |
|---|---:|
| Channel | 10 |
| Video | 10 |
| Commenter | 342 |
| Total | 362 |

## 3. Relationship Overview

| Relationship | Count |
|---|---:|
| PUBLISHES | 10 |
| HAS_COMMENTER | 342 |
| Total | 352 |

## 4. Graph Structure

The graph follows this structure:

Channel -> Video -> Commenter

Each channel publishes a video, and each video is connected to its collected commenters.

The shortest path from a channel to its associated commenter is two relationships.

## 5. Community Analysis

The graph analysis identified 10 communities.

| Community | Commenters |
|---|---:|
| 0 | 49 |
| 1 | 49 |
| 2 | 48 |
| 3 | 48 |
| 4 | 46 |
| 5 | 44 |
| 6 | 42 |
| 7 | 16 |
| 8 | 0 |
| 9 | 0 |
| Total | 342 |

Communities 8 and 9 contain channel and video nodes but no collected commenters.

## 6. Channel-Level Commenter Distribution

| Channel | Commenters | Percentage |
|---|---:|---:|
| IBM Technology | 49 | 14.33% |
| CynoHub | 49 | 14.33% |
| edureka! | 48 | 14.04% |
| Letter Writer | 48 | 14.04% |
| Simplilearn | 46 | 13.45% |
| Science Simplified 4 All | 44 | 12.87% |
| LBC | 42 | 12.28% |
| Daljeet Kaur | 16 | 4.68% |
| 60 Minutes Australia | 0 | 0% |
| Peekaboo Kidz | 0 | 0% |
| Total | 342 | 100% |

Percentages are calculated using the 342 collected commenter relationships.

## 7. Graph Density

The observed directed graph density is approximately 0.2694%.

The relatively low density reflects the sparse structure of the network.

## 8. Cross-Video Interaction

No commenter was observed across multiple videos in the collected dataset.

This means that the current graph does not demonstrate shared commenter activity between the selected videos.

This is a dataset observation, not evidence that the channels have no audience overlap in reality.

## 9. Centrality and PageRank

Degree centrality and PageRank were calculated to examine structural importance within the graph.

Because the graph is organized around channel-video-commenter groups, centrality scores largely reflect the number and arrangement of collected relationships.

These metrics must not be interpreted as direct measures of real-world popularity, authority, or influence.

## 10. Neo4j Import Results

The graph was imported successfully into Neo4j Aura.

| Import Metric | Result |
|---|---:|
| Nodes imported | 362 |
| Relationships imported | 352 |
| Node types | 3 |
| Relationship types | 2 |

## 11. Conclusion

The project demonstrates an end-to-end social media analysis workflow combining text analytics, topic discovery, graph construction, graph analytics, visualization, and graph database integration.

The graph provides a structured representation of the collected YouTube channel, video, and commenter relationships.

Future work can expand the dataset, investigate cross-video interactions, and introduce additional social network analysis techniques.
