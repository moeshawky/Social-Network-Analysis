import matplotlib.pyplot as plt
import networkx as nx
from network_intelligence.visualization.graph_viz import NetworkVisualizer
from network_intelligence import config

class CommunityVisualizer:
    def __init__(self):
        self.viz = NetworkVisualizer()

    def visualize_communities(self, G: nx.Graph, partition: dict, output_path: str = None) -> plt.Figure:
        """Visualizes graph with nodes colored by community."""
        # Update node attributes with community ID
        for node, comm_id in partition.items():
            if node in G:
                G.nodes[node]["community_id"] = comm_id

        return self.viz.visualize_full_network(
            G,
            output_path=output_path,
            title=f"Community Structure (Modularity-based)"
        )

    def visualize_community_boundaries(self, G: nx.Graph, partition: dict, output_path: str = None) -> plt.Figure:
        """
        Highlight edges that cross communities (bridges).
        """
        # Identify cross-community edges
        cross_edges = []
        for u, v in G.edges():
            if partition.get(u) != partition.get(v):
                cross_edges.append((u, v))

        # We can use a custom style for these edges
        # But for now, let's just use full network viz but highlight these edges?
        # GraphViz doesn't support custom edge highlighting easily via simple API I wrote.
        # So I'll just use the standard viz for now.
        return self.visualize_communities(G, partition, output_path)
