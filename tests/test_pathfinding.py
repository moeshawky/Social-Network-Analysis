import pytest
import networkx as nx
from network_intelligence.analysis.pathfinding import PathFinder

def test_find_shortest_weighted_path(sample_graph):
    # G has 1-2 (w=1.0) and 2-3 (w=1.5).
    # Path 1->3 is 1->2->3.
    # Weight distance = 1/1 + 1/1.5 = 1 + 0.66 = 1.66

    # Add a shortcut 1-3 with low weight (high distance)
    # G.add_edge("1", "3", weight=0.1) # distance 10

    finder = PathFinder()

    res = finder.find_shortest_weighted_path(sample_graph, "1", "3")
    assert res["found"]
    assert res["path"] == ["1", "2", "3"]

def test_generate_introduction_chain(sample_graph):
    finder = PathFinder()

    chain = finder.generate_introduction_chain(sample_graph, "1", "3")

    assert chain["source"] == "1"
    assert chain["target"] == "3"
    assert len(chain["steps"]) == 2

    step1 = chain["steps"][0]
    assert step1["from"] == "1"
    assert step1["to"] == "2"
    assert step1["via"] == "facebook"

    step2 = chain["steps"][1]
    assert step2["from"] == "2"
    assert step2["to"] == "3"
    assert step2["via"] == "linkedin"
