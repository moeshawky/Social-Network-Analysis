import networkx as nx
from typing import List, Dict, Any, Optional

class PathFinder:
    def find_shortest_path(self, G: nx.Graph, source: str, target: str) -> Dict[str, Any]:
        """Unweighted shortest path."""
        try:
            path = nx.shortest_path(G, source=source, target=target)
            return {
                "source": source,
                "target": target,
                "path": path,
                "length": len(path) - 1,
                "found": True
            }
        except nx.NetworkXNoPath:
            return {"source": source, "target": target, "found": False}

    def find_shortest_weighted_path(self, G: nx.Graph, source: str, target: str) -> Dict[str, Any]:
        """Weighted shortest path (Dijkstra). weight='weight'."""
        # Note: In our graph, higher weight = stronger connection.
        # Dijkstra minimizes sum of weights.
        # So we need to use 'distance' = 1/weight or similar.
        # Let's create a temporary view or attribute for distance.

        # Or use a weight function
        def weight_func(u, v, d):
            w = d.get('weight', 1.0)
            if w <= 0: return 100.0 # avoid zero/negative
            return 1.0 / w

        try:
            path = nx.dijkstra_path(G, source, target, weight=weight_func)
            return {
                "source": source,
                "target": target,
                "path": path,
                "length": len(path) - 1,
                "found": True,
                "method": "weighted"
            }
        except nx.NetworkXNoPath:
             return {"source": source, "target": target, "found": False}

    def find_all_paths(self, G: nx.Graph, source: str, target: str, max_length: int = 5) -> List[List[str]]:
        """All simple paths up to max length."""
        try:
            return list(nx.all_simple_paths(G, source, target, cutoff=max_length))
        except nx.NetworkXNoPath:
            return []

    def generate_introduction_chain(self, G: nx.Graph, source: str, target: str) -> Dict[str, Any]:
        """Human-readable introduction strategy."""
        path_data = self.find_shortest_weighted_path(G, source, target)
        if not path_data["found"]:
            return {"strategy": "No path found"}

        path = path_data["path"]
        steps = []

        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            edge_data = G.get_edge_data(u, v)

            # If MultiGraph, get_edge_data returns dict of edges keyed by key
            # We want the strongest edge
            if isinstance(G, nx.MultiGraph):
                # find edge with max weight
                best_key = max(edge_data, key=lambda k: edge_data[k].get('weight', 0))
                edge = edge_data[best_key]
            else:
                edge = edge_data

            platform = edge.get("platform", "unknown")
            rel = edge.get("relationship", "connected")

            steps.append({
                "from": u,
                "to": v,
                "via": platform,
                "relationship": rel,
                "action": f"Ask {u} to introduce to {v} via {platform} ({rel})"
            })

        return {
            "source": source,
            "target": target,
            "path": path,
            "steps": steps,
            "length": len(steps)
        }
