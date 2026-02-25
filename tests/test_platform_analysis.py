import pytest
import networkx as nx
from network_intelligence.analysis.platform_analysis import PlatformAnalyzer

def test_single_platform_analysis(sample_graph):
    analyzer = PlatformAnalyzer()

    # Analyze facebook
    res = analyzer.analyze_single_platform(sample_graph, "facebook")

    # FB nodes: 1 and 2
    assert res["platform"] == "facebook"
    assert res["metrics"]["node_count"] == 2
    assert res["metrics"]["edge_count"] == 1

def test_cross_platform_analysis(sample_graph):
    analyzer = PlatformAnalyzer()

    res = analyzer.analyze_cross_platform(sample_graph)

    assert res["metrics"]["node_count"] == 3
    assert res["metrics"]["edge_count"] == 2

def test_compare_person(sample_graph):
    analyzer = PlatformAnalyzer()

    # Node 2 is on FB and LI
    res = analyzer.compare_person_across_platforms(sample_graph, "2")

    assert "facebook" in res
    assert "linkedin" in res

    # Node 1 is only on FB
    res = analyzer.compare_person_across_platforms(sample_graph, "1")
    assert "facebook" in res
    assert "linkedin" not in res # because not in platforms list of node 1
