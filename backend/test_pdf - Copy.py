from app.ai.pdf_parser import extract_text


text = extract_text(
    "app/uploads/MA25M102 (6).pdf"
)


print(text[:1000])