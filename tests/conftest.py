import pytest
import networkx as nx
from network_intelligence.identity.entity import PlatformIdentity, UnifiedEntity

@pytest.fixture
def sample_fb_identity():
    return PlatformIdentity(
        platform="facebook",
        handle="john.doe",
        display_name="John Doe",
        profile_url="http://facebook.com/john.doe",
        numeric_id="123",
        title=None,
        company=None,
        verified=False,
        raw_data={}
    )

@pytest.fixture
def sample_li_identity():
    return PlatformIdentity(
        platform="linkedin",
        handle="johndoe",
        display_name="John Doe",
        profile_url="http://linkedin.com/in/johndoe",
        numeric_id=None,
        title="Engineer",
        company="Tech Corp",
        verified=True,
        raw_data={}
    )

@pytest.fixture
def sample_tw_identity():
    return PlatformIdentity(
        platform="twitter",
        handle="johnd",
        display_name="John D",
        profile_url="http://twitter.com/johnd",
        numeric_id="456",
        title="Tech Enthusiast",
        company=None,
        verified=False,
        raw_data={}
    )

@pytest.fixture
def sample_identities(sample_fb_identity, sample_li_identity, sample_tw_identity):
    return [sample_fb_identity, sample_li_identity, sample_tw_identity]

@pytest.fixture
def sample_graph():
    G = nx.MultiGraph()
    G.add_node("1", canonical_name="Alice", platforms=["facebook"])
    G.add_node("2", canonical_name="Bob", platforms=["facebook", "linkedin"])
    G.add_node("3", canonical_name="Charlie", platforms=["linkedin"])

    G.add_edge("1", "2", key=0, platform="facebook", weight=1.0)
    G.add_edge("2", "3", key=0, platform="linkedin", weight=1.5)
    return G
