import fitz


def extract_text(pdf_path: str) -> str:
    """
    Extract text from every page of a PDF resume.

    Parameters
    ----------
    pdf_path : str
        Path to the uploaded PDF.

    Returns
    -------
    str
        Complete extracted text.
    """

    try:
        document = fitz.open(pdf_path)

        pages = []

        for page in document:
            page_text = page.get_text()

            if page_text:
                pages.append(page_text)

        document.close()

        text = "\n".join(pages)

        return text.strip()

    except Exception as e:
        raise RuntimeError(
            f"Failed to extract PDF text: {str(e)}"
        )