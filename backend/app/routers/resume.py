
import os
from pydantic import BaseModel, Field
from ..ai.job_matcher import compare_resume_to_job
from fastapi import HTTPException
from ..ai.llm_matcher import evaluate_resume_with_ai
from ..ai.scoring import calculate_match_score

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

from ..ai.pdf_parser import extract_text
from ..ai.resume_analyzer import analyze_resume


router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


# ---------------------------------------------------------
# Upload directory
# ---------------------------------------------------------

UPLOAD_FOLDER = "app/uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ---------------------------------------------------------
# Upload Resume
# ---------------------------------------------------------

@router.post(
    "/upload",
    response_model=schemas.ResumeResponse
)
def upload_resume(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # 1. Validate file
    # -----------------------------------------------------

    if file.content_type != "application/pdf":

        raise HTTPException(
            status_code=400,
            detail="Only PDF files allowed"
        )

    # -----------------------------------------------------
    # 2. Save PDF
    # -----------------------------------------------------

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        buffer.write(
            file.file.read()
        )

    # -----------------------------------------------------
    # 3. Extract text from PDF
    # -----------------------------------------------------

    text = extract_text(
        file_path
    )

    if not text.strip():

        raise HTTPException(
            status_code=400,
            detail="Could not extract text from resume"
        )

    # -----------------------------------------------------
    # 4. Analyze resume
    # -----------------------------------------------------

    analysis = analyze_resume(
        text
    )

    # -----------------------------------------------------
    # 5. Convert skills dictionary into string
    #
    # Example:
    #
    # {
    #     "programming": ["python", "java"],
    #     "databases": ["sql", "mysql"]
    # }
    #
    # becomes:
    #
    # programming: python, java
    # databases: sql, mysql
    # -----------------------------------------------------

    skill_lines = []

    for category, skill_list in analysis["skills"].items():

        if skill_list:

            skill_lines.append(
                f"{category}: {', '.join(skill_list)}"
            )

    skills = "\n".join(
        skill_lines
    )

    # -----------------------------------------------------
    # 6. Extract projects section
    # -----------------------------------------------------

    projects_list = analysis["sections"].get(
        "projects",
        []
    )

    projects = "\n".join(
        projects_list
    )

    # -----------------------------------------------------
    # 7. Save resume to database
    # -----------------------------------------------------

    new_resume = models.Resume(

        user_id=current_user.id,

        filename=file.filename,

        filepath=file_path,

        extracted_text=text,

        email=analysis["email"],

        phone=analysis["phone"],

        skills=skills,

        projects=projects,

        score=analysis["score"]
    )

    db.add(
        new_resume
    )

    db.commit()

    db.refresh(
        new_resume
    )

    # -----------------------------------------------------
    # 8. Return structured resume
    # -----------------------------------------------------

    return new_resume


class JobMatchRequest(BaseModel):
    resume_id: int
    job_description: str = Field(
        min_length=30,
        max_length=20000,
    )


@router.post("/match")
def match_resume_to_job(
    request: JobMatchRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Find the requested resume belonging to this user.
    resume_record = (
        db.query(models.Resume)
        .filter(
            models.Resume.id == request.resume_id,
            models.Resume.user_id == current_user.id,
        )
        .first()
    )

    if resume_record is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    if not resume_record.extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Resume has no extracted text",
        )


    # Existing keyword-based matching
    result = compare_resume_to_job(
        resume_text=resume_record.extracted_text,
        job_description=request.job_description,
    )

    # AI-based evaluation
    try:
        ai_report = evaluate_resume_with_ai(
            resume_text=resume_record.extracted_text,
            job_description=request.job_description,
        )

        ai_score = calculate_match_score(ai_report)

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        # Log the real exception on the server, but don't expose
        # API keys or internal details to the client.
        print(f"AI evaluation failed: {type(exc).__name__}: {exc}")

        raise HTTPException(
            status_code=503,
            detail="AI evaluation is temporarily unavailable.",
        ) from exc

    return {
        "resume_id": resume_record.id,
        **result,
        "ai_evaluation": {
            **ai_report.model_dump(),
            "overall_fit_score": ai_score,
            "score_type": "heuristic_requirement_coverage",
            "message": (
                "This score measures evidence of job requirements "
                "in the supplied resume. It is not a shortlisting "
                "probability or a prediction of an employer's decision."
            ),
        },
    }

