import pytest
import responses
from network_intelligence.data_sources.powermem import PowerMemClient

@responses.activate
def test_health_check():
    client = PowerMemClient(base_url="http://mock")

    responses.add(
        responses.GET,
        "http://mock/health",
        status=200
    )

    assert client.health_check() is True

@responses.activate
def test_query():
    client = PowerMemClient(base_url="http://mock")

    responses.add(
        responses.POST,
        "http://mock/api/search",
        json={"results": [{"content": "Alice", "metadata": {"name": "Alice"}}]},
        status=200
    )

    res = client.query("Alice")
    assert len(res) == 1
    assert res[0]["content"] == "Alice"

@responses.activate
def test_load_company_graph():
    client = PowerMemClient(base_url="http://mock")

    mock_results = [
        {
            "id": "1",
            "content": "Alice",
            "metadata": {
                "name": "Alice",
                "relationships": [
                    {"target": "Bob", "type": "colleague"}
                ]
            }
        },
        {
            "id": "2",
            "content": "Bob",
            "metadata": {"name": "Bob"}
        }
    ]

    responses.add(
        responses.POST,
        "http://mock/api/search",
        json={"results": mock_results},
        status=200
    )

    nodes, edges = client.load_company_graph("Acme")

    assert len(nodes) == 2
    assert len(edges) == 1
    assert edges[0]["source"] == "Alice"
    assert edges[0]["target"] == "Bob"

@responses.activate
def test_write_analysis():
    client = PowerMemClient(base_url="http://mock")

    responses.add(
        responses.POST,
        "http://mock/api/memory",
        status=200
    )

    success = client.write_analysis("Test", ["test"], {})
    assert success is True
