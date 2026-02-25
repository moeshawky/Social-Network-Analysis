import pytest
import networkx as nx
import os
from network_intelligence.data_sources.edge_list import EdgeListLoader
from network_intelligence.graph.builder import GraphBuilder
from network_intelligence.identity.resolver import IdentityResolver
from network_intelligence.analysis.centrality import CentralityAnalyzer

@pytest.fixture(scope="module")
def facebook_graph():
    loader = EdgeListLoader()
    # This will download if not present
    try:
        nodes, edges = loader.load()
    except Exception as e:
        pytest.skip(f"Could not load Facebook dataset: {e}")

    resolver = IdentityResolver()
    builder = GraphBuilder(resolver)
    builder.add_data_source(nodes, edges, "facebook_snap")

    # Use simple graph for centrality as per notebook logic
    return builder.get_simplified_graph()

def test_facebook_baseline_eigenvector(facebook_graph):
    # Notebook says Node 1912 is top eigenvector
    analyzer = CentralityAnalyzer()

    # We only compute eigenvector here to save time?
    # Analyzer computes all by default.
    # But we can call specific method.

    res = analyzer.eigenvector_centrality(facebook_graph)

    top_node = res[0]
    assert top_node["node"] == "Node 1912"
    # Score in notebook was 0.0954
    assert abs(top_node["score"] - 0.0954) < 0.01

def test_facebook_baseline_betweenness(facebook_graph):
    # Notebook says Node 107 is top betweenness
    analyzer = CentralityAnalyzer()

    res = analyzer.betweenness_centrality(facebook_graph)

    top_node = res[0]
    assert top_node["node"] == "Node 107"
    # Score in notebook was 0.4807
    assert abs(top_node["score"] - 0.4807) < 0.05
