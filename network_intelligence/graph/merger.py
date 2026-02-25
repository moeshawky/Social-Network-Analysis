import networkx as nx
from typing import Dict
from network_intelligence.graph.builder import GraphBuilder
from network_intelligence.identity.resolver import IdentityResolver
from network_intelligence.identity.entity import PlatformIdentity

class GraphMerger:
    def __init__(self):
        self.resolver = IdentityResolver()
        self.builder = GraphBuilder(self.resolver)

    def merge(self, graphs: Dict[str, nx.MultiGraph]) -> nx.MultiGraph:
        """
        Merge platform-specific graphs into one unified graph.
        Keys are platform names: {"facebook": G_fb, "linkedin": G_li, "twitter": G_tw}
        """
        for platform, G in graphs.items():
            nodes = []
            edges = []

            # Extract nodes
            for node, attrs in G.nodes(data=True):
                # Construct PlatformIdentity from node attributes
                # Assuming node ID is handle if not specified
                handle = attrs.get("handle", str(node))
                ident = PlatformIdentity(
                    platform=platform,
                    handle=handle,
                    display_name=attrs.get("name") or attrs.get("canonical_name") or handle,
                    profile_url=attrs.get("url", ""),
                    numeric_id=attrs.get("numeric_id"),
                    title=attrs.get("title"),
                    company=attrs.get("company"),
                    verified=attrs.get("verified", False),
                    raw_data=attrs
                )
                nodes.append(ident)

            # Extract edges
            for u, v, k, data in G.edges(keys=True, data=True):
                edge = data.copy()
                edge["source"] = str(u) # Assuming node ID corresponds to handle
                edge["target"] = str(v)
                edge["platform"] = platform
                if "weight" not in edge:
                    edge["weight"] = 1.0
                edges.append(edge)

            self.builder.add_data_source(nodes, edges, platform)

        return self.builder.build()
