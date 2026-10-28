
from app.ai.job_matcher import compare_resume_to_job


def test_job_matching():
    resume = """
    Skills: Python, SQL, Pandas, scikit-learn
    """

    job = """
    Requirements: Python, SQL, Power BI, AWS
    """

    result = compare_resume_to_job(resume, job)

    assert result["matched_skills"] == ["python", "sql"]
    assert result["missing_skills"] == ["aws", "power bi"]
    assert result["skill_coverage_score"] == 50


def test_empty_job_skills():
    result = compare_resume_to_job(
        "Python and SQL experience",
        "Excellent communication skills",
    )

    assert result["skill_coverage_score"] is None
    assert result["missing_skills"] == []


def test_empty_resume():
    try:
        compare_resume_to_job("", "Python developer")
        assert False, "Expected ValueError"
    except ValueError:
        pass
