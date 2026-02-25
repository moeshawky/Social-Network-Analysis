import networkx as nx
import os

class GraphExporter:
    def export_graphml(self, G: nx.Graph, filepath: str) -> None:
        """Export to GraphML."""
        nx.write_graphml(G, filepath)

    def export_adjacency_list(self, G: nx.Graph, filepath: str) -> None:
        """Export to adjacency list."""
        nx.write_adjlist(G, filepath)

    def export_edge_list(self, G: nx.Graph, filepath: str) -> None:
        """Export to edge list."""
        nx.write_edgelist(G, filepath)
