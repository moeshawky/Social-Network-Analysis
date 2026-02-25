import networkx as nx
import numpy as np
from typing import Dict, List, Any
from network_intelligence import config

class CentralityAnalyzer:
    def compute_all(self, G: nx.Graph) -> Dict[str, List[Dict]]:
        """Compute all centrality measures."""
        return {
            "degree": self.degree_centrality(G),
            "closeness": self.closeness_centrality(G),
            "betweenness": self.betweenness_centrality(G),
            "eigenvector": self.eigenvector_centrality(G),
            "pagerank": self.pagerank(G),
            "katz": self.katz_centrality(G)
        }

    def _format_results(self, G: nx.Graph, centrality: Dict[Any, float], metric_name: str) -> List[Dict]:
        """Format centrality results."""
        sorted_nodes = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
        results = []
        for i, (node, score) in enumerate(sorted_nodes[:config.TOP_N_RESULTS]):
            # Fetch node attributes
            attrs = G.nodes[node]
            results.append({
                "node": attrs.get("canonical_name", str(node)),
                "entity_id": str(node),
                "score": float(score),
                "rank": i + 1,
                "platforms": attrs.get("platforms", []),
                "interpretation": f"Rank {i+1} in {metric_name}"
            })
        return results

    def degree_centrality(self, G: nx.Graph) -> List[Dict]:
        scores = nx.degree_centrality(G)
        return self._format_results(G, scores, "degree")

    def closeness_centrality(self, G: nx.Graph) -> List[Dict]:
        if G.number_of_nodes() > 5000:
            # Optimization from notebook
            top_degree = sorted(G.degree, key=lambda x: x[1], reverse=True)[:100]
            subgraph = G.subgraph([n for n, d in top_degree])
            scores = nx.closeness_centrality(subgraph)
        else:
            scores = nx.closeness_centrality(G)
        return self._format_results(G, scores, "closeness")

    def betweenness_centrality(self, G: nx.Graph) -> List[Dict]:
        k = min(1000, G.number_of_nodes())
        scores = nx.betweenness_centrality(G, k=k)
        return self._format_results(G, scores, "betweenness")

    def eigenvector_centrality(self, G: nx.Graph) -> List[Dict]:
        try:
            scores = nx.eigenvector_centrality(
                G,
                max_iter=config.EIGENVECTOR_MAX_ITER,
                tol=config.EIGENVECTOR_TOLERANCE
            )
        except nx.PowerIterationFailedConvergence:
            try:
                scores = nx.eigenvector_centrality(G, max_iter=config.EIGENVECTOR_MAX_ITER * 2)
            except:
                scores = nx.eigenvector_centrality_numpy(G)
        return self._format_results(G, scores, "eigenvector")

    def pagerank(self, G: nx.Graph) -> List[Dict]:
        try:
            scores = nx.pagerank(G)
        except:
             scores = {n: 0.0 for n in G.nodes()}
        return self._format_results(G, scores, "pagerank")

    def katz_centrality(self, G: nx.Graph) -> List[Dict]:
        try:
            scores = nx.katz_centrality(G)
        except:
             # Fallback or empty if fails (e.g. strict convergence)
             scores = {n: 0.0 for n in G.nodes()}
        return self._format_results(G, scores, "katz")

    def find_gatekeepers(self, G: nx.Graph, threshold: float = 0.1) -> List[Dict]:
        scores = nx.betweenness_centrality(G, k=min(1000, G.number_of_nodes()))
        gatekeepers = {n: s for n, s in scores.items() if s > threshold}
        return self._format_results(G, gatekeepers, "gatekeeper")
