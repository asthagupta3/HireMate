
from app.ai.llm_matcher import MatchReport
from app.ai.scoring import calculate_match_score


def make_report(requirements):
    return MatchReport(
        summary="Test report",
        strengths=[],
        gaps=[],
        requirements=requirements,
        improvement_suggestions=[],
    )


def test_all_requirements_supported():
    report = make_report([
        {
            "requirement": "Python",
            "importance": "essential",
            "status": "supported",
            "evidence": "Used Python",
            "reasoning": "Direct evidence",
            "recommendation": "None",
        },
    ])

    assert calculate_match_score(report) == 100


def test_no_requirements_evidenced():
    report = make_report([
        {
            "requirement": "Oracle DBA",
            "importance": "essential",
            "status": "not_evidenced",
            "evidence": "",
            "reasoning": "No evidence",
            "recommendation": "Add relevant experience if applicable",
        },
    ])

    assert calculate_match_score(report) == 0


def test_essential_requirements_have_more_weight():
    report = make_report([
        {
            "requirement": "Oracle DBA",
            "importance": "essential",
            "status": "not_evidenced",
            "evidence": "",
            "reasoning": "No evidence",
            "recommendation": "N/A",
        },
        {
            "requirement": "Optional cloud exposure",
            "importance": "desirable",
            "status": "supported",
            "evidence": "Used AWS",
            "reasoning": "Direct evidence",
            "recommendation": "N/A",
        },
    ])

    assert calculate_match_score(report) == 25


def test_partial_evidence():
    report = make_report([
        {
            "requirement": "SQL",
            "importance": "essential",
            "status": "partially_supported",
            "evidence": "Used SQL",
            "reasoning": "Limited evidence",
            "recommendation": "Add examples if accurate",
        },
    ])

    assert calculate_match_score(report) == 50
