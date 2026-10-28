import re
from app.ai.resume_feedback import generate_resume_feedback

SKILL_CATEGORIES = {

    "programming": [
        "python",
        "java",
        "c++",
        "c",
        "javascript",
        "typescript",
        "go",
        "scala",
        "r"
    ],

    "data_engineering": [
        "pyspark",
        "spark",
        "hadoop",
        "kafka",
        "airflow",
        "etl",
        "data pipeline",
        "big data",
        "hive",
        "databricks"
    ],

    "databases": [
        "sql",
        "mysql",
        "postgresql",
        "postgres",
        "mongodb",
        "oracle",
        "redis",
        "sqlite"
    ],

    "cloud": [
        "aws",
        "azure",
        "gcp",
        "google cloud",
        "s3",
        "ec2"
    ],

    "machine_learning": [
        "machine learning",
        "deep learning",
        "pytorch",
        "tensorflow",
        "scikit-learn",
        "sklearn",
        "nlp",
        "computer vision"
    ],

    "web": [
        "fastapi",
        "django",
        "flask",
        "react",
        "node.js",
        "node"
    ],

    "devops": [
        "docker",
        "kubernetes",
        "linux",
        "git",
        "github",
        "ci/cd"
    ],
    
    "data_analytics": [

        "power bi",
        "tableau",
        "excel",
        "advanced excel",
        "looker",
        "matplotlib",
        "seaborn",
        "plotly",
        "pandas",
        "numpy",
        "statistics",
        "data visualization",
        "business intelligence"
    ]

}


def normalize_text(text: str) -> str:
    """
    Normalize resume text for analysis.
    """

    text = text.replace("\r", "\n")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n+",
        "\n",
        text
    )

    return text.strip()


def extract_email(text: str):
    """
    Extract email address from resume.
    """

    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    match = re.search(
        pattern,
        text
    )

    return match.group(0) if match else None


def extract_phone(text: str):
    """
    Extract common Indian/international phone formats.
    """

    patterns = [

        r"\+91[-\s]?\d{10}",

        r"\b\d{10}\b",

        r"\+\d{1,3}[-\s]?\d{7,12}"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group(0)

    return None


def extract_name(text: str):
    """
    Basic name extraction.

    This is intentionally conservative.
    Later we can replace this with an NLP model.
    """

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    for line in lines[:10]:

        lower = line.lower()

        if (
            "resume" in lower
            or "curriculum vitae" in lower
            or "email" in lower
            or "phone" in lower
        ):
            continue

        if "@" in line:
            continue

        words = line.split()

        if 2 <= len(words) <= 4:

            if all(
                word.replace(".", "").isalpha()
                for word in words
            ):
                return line

    return None


def extract_skills(text: str):
    """
    Extract skills and organize them by category.
    """

    text_lower = text.lower()

    result = {}

    for category, skills in SKILL_CATEGORIES.items():

        found = []

        for skill in skills:

            pattern = (
                r"(?<!\w)"
                + re.escape(skill.lower())
                + r"(?!\w)"
            )

            if re.search(pattern, text_lower):

                found.append(skill)

        result[category] = found

    return result


def extract_sections(text: str):
    """
    Detect common resume sections.
    """

    sections = {}

    current_section = None

    section_names = {
        "education": [
            "education",
            "academic background"
        ],

        "experience": [
            "experience",
            "work experience",
            "professional experience"
        ],

        "projects": [
            "projects",
            "academic projects",
            "personal projects"
        ],

        "certifications": [
            "certifications",
            "certificates"
        ],

        "skills": [
            "skills",
            "technical skills"
        ],

        "achievements": [
            "achievements",
            "accomplishments"
        ]
    }

    for line in text.split("\n"):

        clean_line = line.strip()

        if not clean_line:
            continue

        lower = clean_line.lower()

        detected = None

        for section, names in section_names.items():

            if lower in names:

                detected = section
                break

        if detected:

            current_section = detected

            sections[current_section] = []

            continue

        if current_section:

            sections[current_section].append(
                clean_line
            )

    return sections


def calculate_score(skills, sections):
    """
    Simple baseline resume score.

    This is NOT an ML score yet.
    """

    skill_count = sum(
        len(value)
        for value in skills.values()
    )

    score = 0

    score += min(
        skill_count * 3,
        45
    )

    if "education" in sections:
        score += 15

    if "experience" in sections:
        score += 15

    if "projects" in sections:
        score += 15

    if "certifications" in sections:
        score += 10

    return min(
        score,
        100
    )


def analyze_resume(text: str):
    text = normalize_text(text)

    skills = extract_skills(text)
    sections = extract_sections(text)

    analysis = {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": skills,
        "sections": sections,
        "score": calculate_score(skills, sections),
    }

    analysis["feedback"] = generate_resume_feedback(analysis)

    return analysis
