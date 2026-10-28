
from app.ai.resume_feedback import generate_resume_feedback


def test_missing_contact_information():
    analysis = {
        "email": None,
        "phone": None,
        "sections": {
            "education": ["MSc Mathematics"],
            "skills": ["Python", "SQL"],
            "projects": ["Built a data analysis dashboard"],
        },
    }

    feedback = generate_resume_feedback(analysis)

    issues = [item["issue"] for item in feedback]

    assert "Email address not detected" in issues
    assert "Phone number not detected" in issues


def test_missing_resume_sections():
    analysis = {
        "email": "candidate@example.com",
        "phone": "9876543210",
        "sections": {},
    }

    feedback = generate_resume_feedback(analysis)

    issues = [item["issue"] for item in feedback]

    assert "Education section not detected" in issues
    assert "Skills section not detected" in issues
    assert "Projects section not detected" in issues


def test_empty_projects_section():
    analysis = {
        "email": "candidate@example.com",
        "phone": "9876543210",
        "sections": {
            "education": ["MSc Mathematics"],
            "skills": ["Python"],
            "projects": [],
        },
    }

    feedback = generate_resume_feedback(analysis)

    issues = [item["issue"] for item in feedback]

    assert "Projects section appears empty" in issues


def test_detailed_projects_do_not_trigger_short_description_warning():
    analysis = {
        "email": "candidate@example.com",
        "phone": "9876543210",
        "sections": {
            "education": ["MSc Mathematics"],
            "skills": ["Python"],
            "projects": [
                "Developed a customer churn prediction model "
                "using Python and scikit-learn, evaluated its "
                "performance, and compared classification metrics."
            ],
        },
    }

    feedback = generate_resume_feedback(analysis)

    issues = [item["issue"] for item in feedback]

    assert "Project descriptions may lack detail" not in issues


def test_feedback_has_expected_fields():
    analysis = {
        "email": None,
        "phone": None,
        "sections": {},
    }

    feedback = generate_resume_feedback(analysis)

    assert len(feedback) > 0

    expected_fields = {
        "category",
        "severity",
        "issue",
        "explanation",
        "suggestion",
    }

    for item in feedback:
        assert set(item.keys()) == expected_fields
        assert item["severity"] in {"info", "warning"}
