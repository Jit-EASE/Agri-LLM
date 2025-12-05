# ingestion/pdf_extract.py

def extract_pdf_text(pdf_bytes: bytes, max_pages: int = 5) -> str:
    try:
        import PyPDF2
        from io import BytesIO

        reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        pages_text = []
        for page in reader.pages[:max_pages]:
            text = page.extract_text() or ""
            pages_text.append(text)
        return "\n".join(pages_text).strip()
    except Exception:
        return ""
