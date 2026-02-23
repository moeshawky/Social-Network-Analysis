# Social Network Analysis: Link Analysis using Facebook Dataset

## Description
This project focuses on **Social Network Analysis (SNA)** using a real-world dataset from Facebook. It constructs a friendship network as a graph and performs comprehensive **Link Analysis** to identify influential individuals, community bridges, and the overall cohesion of the network.

By applying graph theory and network measures, the project answers critical questions about network connectivity, authority, and clustering.

## Key Features
- **Graph Construction**: Transforming raw edge-list data into an undirected graph using `NetworkX`.
- **Centrality Measures**:
    - **Degree Centrality**: Identifying the most popular/well-connected nodes.
    - **Closeness Centrality**: Measuring the reachability of nodes.
    - **Betweenness Centrality**: Finding "gatekeepers" or bridges between communities.
    - **Eigenvector Centrality**: Identifying influential nodes connected to other important nodes.
- **Community Analysis**:
    - Computing **Local Clustering Coefficients** to determine network density.
    - Detecting and visualizing communities within the social network.
- **Network Statistics**: Detailed metrics including Density, Diameter, and Average Shortest Path Length.
- **Visualization**: Force-directed (Spring Layout) visualizations highlighting top hubs and distinct communities.

## Dataset
- **Source**: SNAP Facebook Combined Network (Stanford Large Network Dataset Collection).
- **Details**: Contains anonymized mutual friendship data from survey participants.
- **Format**: Edge list representing undirected connections.

## Technologies Used
- **Python**: Core programming language.
- **NetworkX**: Comprehensive graph analysis and manipulation.
- **Matplotlib**: Data visualization and graph plotting.
- **NumPy & Pandas**: Data handling and statistical computations.
- **Jupyter Notebook**: Interactive analysis environment.

## Installation & Setup
1. Clone the repository or download the source files.
2. Install the required dependencies:
   ```bash
   pip install networkx matplotlib numpy pandas
   ```
3. Open the `Social_Network_Analysis.ipynb` notebook in a Jupyter environment.
4. Run all cells to download the dataset, process the graph, and view the analysis.

## Analysis Results
- **Most Influential Person**: Identified via Eigenvector Centrality (Node ID 1912).
- **Core Bridge Node**: Identified via Betweenness Centrality (Node ID 107).
- **Network Structure**: Determined to be **Tightly Connected** with a clustering coefficient of ~0.60.
- **Centralization**: The network is **Moderately Centralized**, suggesting a balance between hubs and distributed connections.

## Author
*Analysis performed as part of a Social Network Analysis study.*
