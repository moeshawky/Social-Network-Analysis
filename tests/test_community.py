import pytest
import networkx as nx
from network_intelligence.analysis.community import CommunityDetector

def test_community_detection(sample_graph):
    G = nx.Graph(sample_graph)
    # Add more nodes to make communities viable
    G.add_edge("3", "4", weight=1.0)
    G.add_edge("4", "5", weight=1.0)
    G.add_edge("5", "3", weight=1.0)
    # 3-4-5 is a triangle
    # 1-2 is a line

    detector = CommunityDetector()

    res = detector.detect_communities(G, method="greedy_modularity")

    # Might find 2 communities: {1,2} and {3,4,5}
    # Or just one. It's greedy.

    assert "communities" in res
    assert res["modularity"] >= 0

def test_analyze_structure(sample_graph):
    G = nx.Graph(sample_graph)
    detector = CommunityDetector()

    partition = {n: 0 for n in G.nodes()} # Single community

    stats = detector.analyze_community_structure(G, partition)

    assert len(stats) == 1
    assert stats[0]["size"] == 3
