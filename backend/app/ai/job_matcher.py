
from .resume_analyzer import extract_skills


def compare_resume_to_job(
    resume_text: str,
    job_description: str,
) -> dict:
    """
    Compare resume skills with skills mentioned
    in a job description.

    The score measures skill coverage only.
    It does not predict ATS decisions.
    """

    if not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description.strip():
        raise ValueError("Job description cannot be empty.")

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Flatten skills from all categories into sets.
    candidate = {
        skill
        for skills in resume_skills.values()
        for skill in skills
    }

    required = {
        skill
        for skills in job_skills.values()
        for skill in skills
    }

    matched = sorted(candidate & required)
    missing = sorted(required - candidate)

    if required:
        score = round(100 * len(matched) / len(required))
    else:
        score = None

    return {
        "skill_coverage_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skill_count": len(candidate),
        "job_skill_count": len(required),
        "message": (
            "No supported skills were detected in the "
            "job description."
            if not required
            else "Skill coverage is not a shortlisting probability."
        ),
    }
