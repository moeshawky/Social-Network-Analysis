import pytest
import networkx as nx
from network_intelligence.graph.builder import GraphBuilder
from network_intelligence.identity.resolver import IdentityResolver

def test_graph_builder_add_data_source(sample_identities):
    resolver = IdentityResolver()
    builder = GraphBuilder(resolver)

    nodes = sample_identities
    edges = [
        {"source": "john.doe", "target": "johndoe", "platform": "facebook", "weight": 1.0}
    ]

    # This example edge is weird because source/target are handles from different platforms
    # but in reality add_data_source is called per platform.
    # Let's fix.

    fb_nodes = [n for n in nodes if n.platform == "facebook"]
    # Add another FB node
    from network_intelligence.identity.entity import PlatformIdentity
    fb_friend = PlatformIdentity(
        platform="facebook",
        handle="jane.doe",
        display_name="Jane Doe",
        profile_url="",
        numeric_id="999",
        title=None,
        company=None,
        verified=False,
        raw_data={}
    )
    fb_nodes.append(fb_friend)

    fb_edges = [
        {"source": "john.doe", "target": "jane.doe", "platform": "facebook", "weight": 1.0}
    ]

    builder.add_data_source(fb_nodes, fb_edges, "facebook")
    G = builder.build()

    assert G.number_of_nodes() == 2
    assert G.number_of_edges() == 1

def test_graph_builder_incremental(sample_identities):
    resolver = IdentityResolver()
    builder = GraphBuilder(resolver)

    from network_intelligence.identity.entity import PlatformIdentity

    # Custom mergeable identities
    fb_node = PlatformIdentity(
        platform="facebook",
        handle="john.doe",
        display_name="John Doe",
        profile_url="",
        numeric_id=None,
        title="Engineer",
        company="Acme",
        verified=False,
        raw_data={}
    )

    li_node = PlatformIdentity(
        platform="linkedin",
        handle="john.doe",
        display_name="John Doe",
        profile_url="",
        numeric_id=None,
        title="Engineer",
        company="Acme",
        verified=False,
        raw_data={}
    )

    # Phase 1: FB
    builder.add_data_source([fb_node], [], "facebook")

    assert builder.build().number_of_nodes() == 1

    # Phase 2: LI (same person)
    builder.add_data_source([li_node], [], "linkedin")

    # Should resolve to same entity
    G = builder.build()
    assert G.number_of_nodes() == 1 # Merged
    node_id = list(G.nodes)[0]
    platforms = G.nodes[node_id]["platforms"]
    assert "facebook" in platforms
    assert "linkedin" in platforms

def test_get_simplified_graph(sample_graph):
    # Create builder and mock internal graph
    resolver = IdentityResolver()
    builder = GraphBuilder(resolver)
    builder.graph = sample_graph

    simple_G = builder.get_simplified_graph()
    assert isinstance(simple_G, nx.Graph)
    assert not isinstance(simple_G, nx.MultiGraph)
    assert simple_G.number_of_nodes() == 3
    assert simple_G.number_of_edges() == 2
