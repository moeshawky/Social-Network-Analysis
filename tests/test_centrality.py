import pytest
import networkx as nx
from network_intelligence.analysis.centrality import CentralityAnalyzer

def test_centrality_compute_all(sample_graph):
    # Convert MultiGraph to Graph for analysis as analyzer expects simple graph for most part
    # But compute_all takes nx.Graph (which MultiGraph is subclass of, but algorithms might behave differently)
    # The analyzer logic doesn't explicitly convert.
    # Standard centrality functions in NX handle MultiGraph by treating as weighted or ignoring keys.
    # degree_centrality works on MultiGraph.

    G = nx.Graph(sample_graph) # Simplify
    analyzer = CentralityAnalyzer()

    results = analyzer.compute_all(G)

    assert "degree" in results
    assert "betweenness" in results
    assert "eigenvector" in results

    # Check degree
    # 2 is connected to 1 and 3. Degree 2.
    # 1 is connected to 2. Degree 1.
    # 3 is connected to 2. Degree 1.

    deg = results["degree"]
    # Should be sorted by score
    assert deg[0]["entity_id"] == "2" # Highest degree (using entity_id check)
    assert deg[0]["score"] == 1.0 # 2/2 = 1.0 normalized

def test_betweenness(sample_graph):
    G = nx.Graph(sample_graph)
    analyzer = CentralityAnalyzer()

    bet = analyzer.betweenness_centrality(G)
    # Node 2 is bridge. Betweenness should be high.
    # 1-2-3 path exists. 2 is on path 1-3.
    # 1 and 3 are leaves.

    node_2 = next(r for r in bet if r["entity_id"] == "2")
    assert node_2["score"] > 0

    node_1 = next(r for r in bet if r["entity_id"] == "1")
    assert node_1["score"] == 0.0

def test_eigenvector(sample_graph):
    G = nx.Graph(sample_graph)
    analyzer = CentralityAnalyzer()

    eig = analyzer.eigenvector_centrality(G)
    assert len(eig) == 3
