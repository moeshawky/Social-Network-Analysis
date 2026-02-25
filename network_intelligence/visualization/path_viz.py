import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Dict
from network_intelligence.visualization.graph_viz import NetworkVisualizer

class PathVisualizer:
    def __init__(self):
        self.viz = NetworkVisualizer()

    def visualize_path(self, G: nx.Graph, path: List[str], output_path: str = None) -> plt.Figure:
        """Visualize full network with path highlighted."""
        highlight_nodes = {node: "path_node" for node in path}
        if len(path) > 0:
            highlight_nodes[path[0]] = "client"
            highlight_nodes[path[-1]] = "target"

        return self.viz.visualize_full_network(
            G,
            highlight_nodes=highlight_nodes,
            highlight_path=path,
            output_path=output_path,
            title=f"Path Visualization ({len(path)-1} hops)"
        )

    def visualize_introduction_chain(self, G: nx.Graph, chain: Dict[str, Any], output_path: str = None) -> plt.Figure:
        """Visualize introduction chain (same as path for now)."""
        path = chain.get("path", [])
        return self.visualize_path(G, path, output_path)
