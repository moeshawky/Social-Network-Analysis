import networkx as nx
import uuid
from typing import List, Dict, Any, Optional
from network_intelligence.identity.entity import PlatformIdentity, UnifiedEntity
from network_intelligence.identity.resolver import IdentityResolver

class GraphBuilder:
    def __init__(self, identity_resolver: IdentityResolver):
        self.resolver = identity_resolver
        self.graph = nx.MultiGraph()
        self.all_identities: List[PlatformIdentity] = []
        self.all_edges: List[Dict] = []
        self.handle_map: Dict[str, str] = {}

    def add_data_source(self, nodes: List[PlatformIdentity], edges: List[Dict], platform: str) -> None:
        """Add data from a single platform. Triggers identity resolution."""
        # Add new data
        self.all_identities.extend(nodes)
        self.all_edges.extend(edges)

        # Run resolution
        unified_entities = self.resolver.resolve(self.all_identities)

        # Rebuild graph
        self.graph.clear()
        self.handle_map.clear()

        # Re-populate nodes from resolved entities
        for entity in unified_entities:
            attrs = {
                "canonical_name": entity.canonical_name,
                "platforms": list(entity.platforms_present),
                "confidence": entity.overall_confidence,
                "type": "person",
                "entity_id": entity.entity_id
            }

            # Map all identity handles to this entity ID
            for ident in entity.identities:
                key = f"{ident.platform}:{ident.handle}"
                self.handle_map[key] = entity.entity_id

                # Best effort attribute merging
                if ident.title and "title" not in attrs:
                    attrs["title"] = ident.title
                if ident.company and "company" not in attrs:
                    attrs["company"] = ident.company

            self.graph.add_node(entity.entity_id, **attrs)

        # Add all edges
        for edge in self.all_edges:
            src_handle = edge["source"]
            tgt_handle = edge["target"]
            plt = edge["platform"]

            src_key = f"{plt}:{src_handle}"
            tgt_key = f"{plt}:{tgt_handle}"

            u = self.handle_map.get(src_key)
            v = self.handle_map.get(tgt_key)

            # Handle missing nodes (stubs)
            if not u:
                u = self._create_stub_entity(src_handle, plt)
            if not v:
                v = self._create_stub_entity(tgt_handle, plt)

            self.graph.add_edge(u, v, **edge)

    def _create_stub_entity(self, handle: str, platform: str) -> str:
        """Create a stub entity for a node mentioned in an edge but not in profiles."""
        # Create identity so it persists for future resolutions
        ident = PlatformIdentity(
            platform=platform,
            handle=handle,
            display_name=handle,
            profile_url="",
            numeric_id=None,
            title=None,
            company=None,
            verified=False,
            raw_data={"stub": True}
        )
        self.all_identities.append(ident)

        # Create ephemeral entity ID and node for current graph state
        entity_id = str(uuid.uuid4())

        self.graph.add_node(entity_id,
                            canonical_name=handle,
                            platforms=[platform],
                            confidence=0.0,
                            type="stub",
                            entity_id=entity_id)

        key = f"{platform}:{handle}"
        self.handle_map[key] = entity_id

        return entity_id

    def build(self) -> nx.MultiGraph:
        """Finalize graph construction."""
        return self.graph

    def get_simplified_graph(self) -> nx.Graph:
        """Collapse MultiGraph to simple Graph by summing edge weights per pair."""
        simple_graph = nx.Graph()

        for u, v, data in self.graph.edges(data=True):
            w = data.get('weight', 1.0)
            if simple_graph.has_edge(u, v):
                simple_graph[u][v]['weight'] += w
            else:
                simple_graph.add_edge(u, v, weight=w)

        for node, attrs in self.graph.nodes(data=True):
            simple_graph.add_node(node, **attrs)

        return simple_graph
