import pytest
import networkx as nx
from network_intelligence.analysis.metrics import NetworkMetrics

def test_metrics_compute_all(sample_graph):
    G = nx.Graph(sample_graph)

    metrics = NetworkMetrics()
    res = metrics.compute_all(G)

    assert res["node_count"] == 3
    assert res["edge_count"] == 2
    assert res["density"] == 2/3 # 2 edges, 3 possible (3*2/2=3). So 2/3 = 0.66

    assert res["is_connected"] is True
    assert res["diameter"] == 2

def test_resilience(sample_graph):
    G = nx.Graph(sample_graph)
    metrics = NetworkMetrics()

    # Remove node 2 (bridge)
    res = metrics.analyze_resilience(G, nodes_to_remove=1)

    assert res["removed_nodes"] == ["2"]
    assert res["final_components"] == 2 # 1 and 3 are separated
    assert res["fragmented"] is True
