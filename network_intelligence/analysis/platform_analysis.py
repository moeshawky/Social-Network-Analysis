import networkx as nx
from typing import Dict, List, Any
from network_intelligence.analysis.centrality import CentralityAnalyzer
from network_intelligence.analysis.metrics import NetworkMetrics

class PlatformAnalyzer:
    def __init__(self):
        self.centrality = CentralityAnalyzer()
        self.metrics = NetworkMetrics()

    def _get_platform_subgraph(self, G: nx.MultiGraph, platform: str) -> nx.Graph:
        """Extract subgraph for a single platform."""
        # Filter edges
        edges = []
        for u, v, k, data in G.edges(keys=True, data=True):
            if data.get("platform") == platform:
                edges.append((u, v, data))

        # Create new graph from these edges
        subG = nx.Graph() # Simple graph for analysis usually
        for u, v, data in edges:
            if subG.has_edge(u, v):
                # If multiple edges of same platform (e.g. friend + follows), take max weight?
                # Or sum? Let's sum
                subG[u][v]['weight'] += data.get('weight', 1.0)
            else:
                subG.add_edge(u, v, **data)

        # Add nodes that belong to this platform even if isolated
        for node, attrs in G.nodes(data=True):
            if platform in attrs.get("platforms", []):
                if not subG.has_node(node):
                    subG.add_node(node, **attrs)

        return subG

    def analyze_single_platform(self, G: nx.MultiGraph, platform: str) -> Dict[str, Any]:
        """Run full analysis on one platform's subgraph."""
        subG = self._get_platform_subgraph(G, platform)

        return {
            "platform": platform,
            "metrics": self.metrics.compute_all(subG),
            "centrality": self.centrality.compute_all(subG)
        }

    def analyze_cross_platform(self, G: nx.MultiGraph) -> Dict[str, Any]:
        """Run full analysis on merged graph."""
        # Need to simplify MultiGraph to Graph for most standard metrics
        # Builder has get_simplified_graph logic but we don't have builder instance here.
        # Let's implement simplification logic here or assume G passed is already simple?
        # The type hint says MultiGraph.

        simple_G = nx.Graph()
        for u, v, data in G.edges(data=True):
            w = data.get('weight', 1.0)
            if simple_G.has_edge(u, v):
                simple_G[u][v]['weight'] += w
            else:
                simple_G.add_edge(u, v, weight=w)

        # Copy node attributes
        for node, attrs in G.nodes(data=True):
            simple_G.add_node(node, **attrs)

        return {
            "platform": "cross_platform",
            "metrics": self.metrics.compute_all(simple_G),
            "centrality": self.centrality.compute_all(simple_G)
        }

    def compare_person_across_platforms(self, G: nx.MultiGraph, entity_id: str) -> Dict[str, Any]:
        """Compare one person's metrics across all their platforms."""
        if not G.has_node(entity_id):
            return {"error": "Entity not found"}

        node_platforms = G.nodes[entity_id].get("platforms", [])
        comparison = {}

        for plt in node_platforms:
            subG = self._get_platform_subgraph(G, plt)
            # Compute specific metrics for this node in this subgraph
            try:
                deg = nx.degree_centrality(subG).get(entity_id, 0)
                bet = nx.betweenness_centrality(subG, k=min(100, len(subG))).get(entity_id, 0)
            except:
                deg = 0
                bet = 0

            comparison[plt] = {
                "degree_centrality": deg,
                "betweenness_centrality": bet
            }

        return comparison

    def platform_presence_report(self, G: nx.MultiGraph) -> Dict[str, Any]:
        """Report on cross-platform coverage."""
        counts = {
            "total_nodes": G.number_of_nodes(),
            "multi_platform": 0,
            "single_platform": 0,
            "by_platform": {}
        }

        for node, attrs in G.nodes(data=True):
            plts = attrs.get("platforms", [])
            if len(plts) > 1:
                counts["multi_platform"] += 1
            else:
                counts["single_platform"] += 1

            for p in plts:
                counts["by_platform"][p] = counts["by_platform"].get(p, 0) + 1

        return counts
