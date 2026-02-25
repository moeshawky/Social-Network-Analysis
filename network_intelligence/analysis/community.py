import networkx as nx
from networkx.algorithms import community
import community as community_louvain # python-louvain
from typing import Dict, List, Any
from network_intelligence import config

class CommunityDetector:
    def detect_communities(self, G: nx.Graph, method: str = "louvain") -> Dict[str, Any]:
        """Detect communities using specified method."""
        if method == "louvain":
            # returns partition dict {node: community_id}
            partition = community_louvain.best_partition(G)
            communities = {}
            for node, comm_id in partition.items():
                if comm_id not in communities:
                    communities[comm_id] = []
                communities[comm_id].append(node)
            communities_list = list(communities.values())

        elif method == "greedy_modularity":
            # returns list of sets
            communities_list = list(community.greedy_modularity_communities(G))
            communities_list = [list(c) for c in communities_list]
            partition = {}
            for i, comm in enumerate(communities_list):
                for node in comm:
                    partition[node] = i

        elif method == "label_propagation":
            communities_list = list(community.label_propagation_communities(G))
            communities_list = [list(c) for c in communities_list]
            partition = {}
            for i, comm in enumerate(communities_list):
                for node in comm:
                    partition[node] = i
        else:
            raise ValueError(f"Unknown community detection method: {method}")

        # Filter small communities
        communities_list = [c for c in communities_list if len(c) >= config.MIN_COMMUNITY_SIZE]

        # Calculate modularity
        try:
            modularity = community.modularity(G, communities_list)
        except:
            modularity = 0.0

        return {
            "method": method,
            "communities": communities_list,
            "partition": partition, # map node -> comm_id
            "modularity": modularity,
            "community_count": len(communities_list)
        }

    def analyze_community_structure(self, G: nx.Graph, partition: Dict[str, int]) -> List[Dict]:
        """Analyze each community for leaders and bridges."""
        communities = {}
        for node, comm_id in partition.items():
            if comm_id not in communities:
                communities[comm_id] = []
            communities[comm_id].append(node)

        results = []
        for comm_id, nodes in communities.items():
            if len(nodes) < config.MIN_COMMUNITY_SIZE:
                continue

            subgraph = G.subgraph(nodes)

            # Leader: highest degree (simple proxy) or eigenvector
            # For speed, degree
            leader = max(subgraph.nodes, key=lambda n: subgraph.degree[n])

            # Bridge: highest betweenness relative to full graph?
            # Or boundary nodes?
            # Let's check boundary nodes (connected to outside)
            boundary_nodes = [n for n in nodes if any(partition[nbr] != comm_id for nbr in G[n])]

            results.append({
                "community_id": comm_id,
                "size": len(nodes),
                "leader": leader,
                "boundary_nodes_count": len(boundary_nodes),
                "density": nx.density(subgraph)
            })

        return sorted(results, key=lambda x: x["size"], reverse=True)
