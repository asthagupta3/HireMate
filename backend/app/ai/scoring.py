
from app.ai.llm_matcher import MatchReport


IMPORTANCE_WEIGHTS = {
    "essential": 3,
    "desirable": 1,
    "unspecified": 2,
}

STATUS_SCORES = {
    "supported": 1.0,
    "partially_supported": 0.5,
    "not_evidenced": 0.0,
}


def calculate_match_score(report: MatchReport) -> int:
    """Calculate an explainable, weighted requirement coverage score."""

    requirements = report.requirements

    if not requirements:
        return 0

    total_weight = 0
    earned_weight = 0.0

    for requirement in requirements:
        weight = IMPORTANCE_WEIGHTS[requirement.importance]
        score = STATUS_SCORES[requirement.status]

        total_weight += weight
        earned_weight += weight * score

    if total_weight == 0:
        return 0

    return round(100 * earned_weight / total_weight)
