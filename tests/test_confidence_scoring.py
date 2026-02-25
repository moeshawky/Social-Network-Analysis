import pytest
from network_intelligence.identity.confidence import ConfidenceScorer

def test_confidence_scorer():
    scorer = ConfidenceScorer()

    signals = {
        "name_similarity": 1.0,
        "handle_similarity": 0.0,
        "company_match": 1.0,
        "title_match": 0.0,
        "mutual_connections": 0.0
    }

    # 0.3 * 1.0 + 0.2 * 1.0 = 0.5
    # total weights = 0.3+0.15+0.2+0.1+0.25 = 1.0

    score = scorer.score(signals)
    assert score == pytest.approx(0.5)

def test_explain():
    scorer = ConfidenceScorer()
    signals = {
        "name_similarity": 1.0,
        "handle_similarity": 1.0,
        "company_match": 1.0,
        "title_match": 1.0,
        "mutual_connections": 1.0
    }

    explanation = scorer.explain(signals)
    assert explanation["overall_confidence"] == 1.0
    assert explanation["tier"] == "auto_merge"
    assert "name_similarity" in explanation["signals"]
