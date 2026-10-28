from app.ai.resume_analyzer import analyze_resume


def test_analyze_resume_includes_feedback():
    text = """
    John Smith
    john@example.com
    9876543210

    Education
    MSc Mathematics

    Skills
    Python, SQL

    Projects
    Built a dashboard using Python and SQL.
    """

    result = analyze_resume(text)

    assert "feedback" in result
    assert isinstance(result["feedback"], list)
    assert len(result["feedback"]) > 0