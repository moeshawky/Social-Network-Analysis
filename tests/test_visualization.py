import pytest
import os
import networkx as nx
from network_intelligence.visualization.graph_viz import NetworkVisualizer
from network_intelligence.visualization.centrality_viz import CentralityVisualizer

def test_visualize_full_network(sample_graph, tmp_path):
    G = nx.Graph(sample_graph)
    viz = NetworkVisualizer()
    output = tmp_path / "network.png"

    viz.visualize_full_network(G, output_path=str(output))
    assert os.path.exists(output)

def test_visualize_ego(sample_graph, tmp_path):
    G = nx.Graph(sample_graph)
    viz = NetworkVisualizer()
    output = tmp_path / "ego.png"

    # Ego for node 2 (center)
    viz.visualize_ego_network(G, "2", radius=1, output_path=str(output))
    assert os.path.exists(output)

def test_visualize_bar_chart(tmp_path):
    viz = CentralityVisualizer()
    data = [
        {"node": "Alice", "score": 1.0},
        {"node": "Bob", "score": 0.5}
    ]
    output = tmp_path / "bar.png"

    viz.visualize_bar_chart(data, output_path=str(output))
    assert os.path.exists(output)
