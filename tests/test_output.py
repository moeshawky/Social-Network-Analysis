import pytest
import os
import json
from network_intelligence.output.json_output import JSONOutputGenerator
from network_intelligence.output.markdown_output import MarkdownOutputGenerator
from network_intelligence.output.powermem_writer import PowerMemWriter

@pytest.fixture
def sample_data():
    return {
        "company": "Acme",
        "graph_stats": {"nodes": 10, "edges": 20},
        "centrality": {
            "eigenvector": [
                {"rank": 1, "node": "Alice", "score": 0.9, "platforms": ["fb"]}
            ]
        },
        "metrics": {"density": 0.5, "average_clustering": 0.6},
        "communities": {"community_count": 2},
        "path_analysis": {
            "source": "Me",
            "target": "Alice",
            "introduction_chain": {
                "steps": [
                    {"from": "Me", "to": "Bob", "via": "linkedin", "relationship": "connected"}
                ]
            }
        },
        "identity_resolution": {"total_identities_processed": 5}
    }

def test_json_output(sample_data, tmp_path):
    gen = JSONOutputGenerator()
    out = tmp_path / "output.json"

    json_str = gen.generate(sample_data, str(out))

    assert os.path.exists(out)
    data = json.loads(json_str)
    assert data["workflow"] == "network-intelligence"
    assert data["centrality"]["eigenvector"][0]["node"] == "Alice"

def test_markdown_output(sample_data, tmp_path):
    gen = MarkdownOutputGenerator()
    out = tmp_path / "output.md"

    md_str = gen.generate(sample_data, str(out))

    assert os.path.exists(out)
    assert "# Network Intelligence Briefing" in md_str
    assert "Alice" in md_str
    assert "0.9000" in md_str

def test_powermem_writer(sample_data):
    # Mock health check and write
    # Assuming PowerMemWriter uses PowerMemClient which we can mock or the writer itself
    # Since we tested client separately, we can rely on integration or mock client inside writer

    pass # Skipped for now as it relies on live service or heavy mocking of internal client
