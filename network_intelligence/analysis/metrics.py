import networkx as nx
import numpy as np
from typing import Dict, Any

class NetworkMetrics:
    def compute_all(self, G: nx.Graph) -> Dict[str, Any]:
        """Compute all network-level metrics."""
        is_connected = nx.is_connected(G) if G.number_of_nodes() > 0 else False

        metrics = {
            "node_count": G.number_of_nodes(),
            "edge_count": G.number_of_edges(),
            "density": nx.density(G),
            "is_connected": is_connected,
            "transitivity": nx.transitivity(G),
            "average_clustering": nx.average_clustering(G),
            "assortativity": nx.degree_assortativity_coefficient(G) if G.number_of_edges() > 0 else 0.0,
            "components": nx.number_connected_components(G) if G.number_of_nodes() > 0 else 0
        }

        if is_connected and G.number_of_nodes() > 1:
            metrics["diameter"] = nx.diameter(G)
            metrics["avg_shortest_path"] = nx.average_shortest_path_length(G)
        else:
            metrics["diameter"] = None
            metrics["avg_shortest_path"] = None
            # Maybe compute for largest component?
            if G.number_of_nodes() > 0:
                largest_cc = max(nx.connected_components(G), key=len)
                subG = G.subgraph(largest_cc)
                if subG.number_of_nodes() > 1:
                    metrics["largest_component_diameter"] = nx.diameter(subG)
                    metrics["largest_component_avg_path"] = nx.average_shortest_path_length(subG)
                    metrics["largest_component_fraction"] = len(largest_cc) / G.number_of_nodes()

        return metrics

    def analyze_resilience(self, G: nx.Graph, nodes_to_remove: int = 1) -> Dict[str, Any]:
        """Measure fragmentation after removing top N betweenness nodes."""
        if G.number_of_nodes() <= nodes_to_remove:
            return {"resilience": "collapsed"}

        initial_clustering = nx.average_clustering(G)
        initial_components = nx.number_connected_components(G)

        # Find top betweenness nodes
        betweenness = nx.betweenness_centrality(G, k=min(100, G.number_of_nodes()))
        top_nodes = sorted(betweenness, key=betweenness.get, reverse=True)[:nodes_to_remove]

        G_removed = G.copy()
        G_removed.remove_nodes_from(top_nodes)

        final_clustering = nx.average_clustering(G_removed)
        final_components = nx.number_connected_components(G_removed)

        return {
            "removed_nodes": top_nodes,
            "initial_clustering": initial_clustering,
            "final_clustering": final_clustering,
            "clustering_change": final_clustering - initial_clustering,
            "initial_components": initial_components,
            "final_components": final_components,
            "component_change": final_components - initial_components,
            "fragmented": final_components > initial_components
        }
