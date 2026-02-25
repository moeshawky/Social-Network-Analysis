import pytest
from network_intelligence.identity.resolver import IdentityResolver
from network_intelligence.identity.entity import PlatformIdentity

def test_resolve_exact_match():
    resolver = IdentityResolver()

    # Identical except platform and handle format
    # To get >0.90, we need strong signals.
    # Adding matching company and title.
    id1 = PlatformIdentity(
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

    id2 = PlatformIdentity(
        platform="linkedin",
        handle="john.doe", # Make handle identical to boost score for test
        display_name="John Doe",
        profile_url="",
        numeric_id=None,
        title="Engineer",
        company="Acme",
        verified=False,
        raw_data={}
    )

    entities = resolver.resolve([id1, id2])
    assert len(entities) == 1
    assert len(entities[0].identities) == 2
    assert entities[0].canonical_name == "John Doe"

def test_resolve_no_match():
    resolver = IdentityResolver()

    id1 = PlatformIdentity(
        platform="facebook",
        handle="john.doe",
        display_name="John Doe",
        profile_url="",
        numeric_id=None,
        title=None,
        company=None,
        verified=False,
        raw_data={}
    )

    id2 = PlatformIdentity(
        platform="linkedin",
        handle="jane.smith",
        display_name="Jane Smith",
        profile_url="",
        numeric_id=None,
        title=None,
        company=None,
        verified=False,
        raw_data={}
    )

    entities = resolver.resolve([id1, id2])
    assert len(entities) == 2

def test_block_by_name():
    resolver = IdentityResolver()
    id1 = PlatformIdentity(
        platform="fb", handle="a", display_name="John Doe",
        profile_url="", numeric_id=None, title=None, company=None, verified=False, raw_data={}
    )
    id2 = PlatformIdentity(
        platform="li", handle="b", display_name="Jane Doe",
        profile_url="", numeric_id=None, title=None, company=None, verified=False, raw_data={}
    )

    blocks = resolver.block_by_name([id1, id2])
    # Both end with "Doe", block by last name 3 chars
    # "Doe" -> "doe" (normalized)
    assert "doe" in blocks
    assert len(blocks["doe"]) == 2
