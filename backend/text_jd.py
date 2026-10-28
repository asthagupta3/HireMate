
import json

import pytest
from docx import Document
from io import BytesIO

from app.ai.job_description_parser import (
    JobDescriptionError,
    parse_job_description,
    parse_job_description_text,
)


SAMPLE_JD = (
    "We are hiring a Python developer with SQL experience. "
    "The candidate will build APIs and maintain databases."
)


def test_parse_txt():
    result = parse_job_description(
        "job.txt", SAMPLE_JD.encode("utf-8")
    )
    assert "Python developer" in result
    assert "SQL experience" in result


def test_parse_json():
    payload = json.dumps({
        "title": "Python Developer",
        "description": SAMPLE_JD,
        "requirements": ["Python", "SQL"],
    }).encode("utf-8")

    result = parse_job_description("job.json", payload)
    assert "Python Developer" in result
    assert "SQL" in result


def test_parse_pasted_text():
    result = parse_job_description_text(SAMPLE_JD)
    assert "Python developer" in result


def test_reject_unsupported_extension():
    with pytest.raises(JobDescriptionError):
        parse_job_description("job.exe", b"some content")


def test_reject_empty_file():
    with pytest.raises(JobDescriptionError):
        parse_job_description("job.txt", b"")


def test_reject_short_text():
    with pytest.raises(JobDescriptionError):
        parse_job_description_text("Too short")


def test_parse_docx():
    buffer = BytesIO()
    document = Document()
    document.add_paragraph(SAMPLE_JD)
    document.save(buffer)

    result = parse_job_description("job.docx", buffer.getvalue())
    assert "Python developer" in result
