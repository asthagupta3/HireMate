
from typing import Any


def generate_resume_feedback(
    analysis: dict[str, Any],
) -> list[dict[str, str]]:
    """
    Generate transparent, rule-based resume improvement suggestions.

    This is a heuristic feedback engine, not an ATS prediction model.
    """

    feedback = []

    def add_feedback(
        category: str,
        severity: str,
        issue: str,
        explanation: str,
        suggestion: str,
    ) -> None:
        feedback.append({
            "category": category,
            "severity": severity,
            "issue": issue,
            "explanation": explanation,
            "suggestion": suggestion,
        })

    # 1. Contact information
    if not analysis.get("email"):
        add_feedback(
            category="Contact Information",
            severity="warning",
            issue="Email address not detected",
            explanation=(
                "The analyzer could not find an email address "
                "in the extracted resume text."
            ),
            suggestion=(
                "Add a professional email address near the top "
                "of your resume."
            ),
        )

    if not analysis.get("phone"):
        add_feedback(
            category="Contact Information",
            severity="info",
            issue="Phone number not detected",
            explanation=(
                "The analyzer could not identify a phone number."
            ),
            suggestion=(
                "Consider including a reachable phone number "
                "if appropriate for your applications."
            ),
        )

    # 2. Important resume sections
    sections = analysis.get("sections", {})

    recommended_sections = {
        "education": (
            "Education section not detected",
            "Add your degree, institution, and relevant academic details.",
        ),
        "skills": (
            "Skills section not detected",
            "Add a clearly labelled skills section with relevant skills.",
        ),
        "projects": (
            "Projects section not detected",
            "Include relevant academic, personal, or professional projects.",
        ),
    }

    for section_name, details in recommended_sections.items():
        issue, suggestion = details

        if section_name not in sections:
            add_feedback(
                category="Resume Structure",
                severity="warning",
                issue=issue,
                explanation=(
                    f"No clearly labelled {section_name} section "
                    "was detected. The information may still exist "
                    "under another heading."
                ),
                suggestion=suggestion,
            )

    # 3. Project descriptions
    if "projects" in sections:
        project_lines = [
            line.strip()
            for line in sections["projects"]
            if line.strip()
        ]

        if not project_lines:
            add_feedback(
                category="Projects",
                severity="warning",
                issue="Projects section appears empty",
                explanation=(
                    "A project heading was found, but no content "
                    "was detected underneath it."
                ),
                suggestion=(
                    "Describe each project, your contribution, "
                    "the tools used, and the outcome."
                ),
            )
        elif not any(len(line.split()) >= 8 for line in project_lines):
            add_feedback(
                category="Projects",
                severity="info",
                issue="Project descriptions may lack detail",
                explanation=(
                    "The detected project content consists of short "
                    "lines. The analyzer cannot determine whether "
                    "these descriptions communicate meaningful work."
                ),
                suggestion=(
                    "Expand relevant project descriptions to explain "
                    "the problem, your actions, tools, and measurable "
                    "results where available."
                ),
            )

    # 4. General feedback
    if not feedback:
        add_feedback(
            category="General",
            severity="info",
            issue="No issues detected by the current checks",
            explanation=(
                "The basic structural checks did not identify "
                "any of the issues they are designed to detect."
            ),
            suggestion=(
                "Review the resume for role relevance, clear "
                "achievements, factual accuracy, and readable formatting."
            ),
        )

    return feedback
