import os
import io
from fastapi import UploadFile
from PIL import Image
from pypdf import PdfReader
import docx

async def parse_file(file: UploadFile) -> str:
    """Parse different file types and extract their content."""
    content = await file.read()
    _, ext = os.path.splitext(file.filename)
    ext = ext.lower()

    try:
        if ext in {".jpg", ".jpeg", ".png"}:
            return await parse_image(content)
        elif ext == ".pdf":
            return await parse_pdf(content)
        elif ext in {".docx", ".doc"}:
            return await parse_docx(content)
        else:
            return f"Unsupported file type: {ext}. Please upload JPG, PNG, PDF, or DOCX files."
    except Exception as e:
        return f"Error parsing file: {str(e)}"
    finally:
        await file.seek(0)

async def parse_image(content: bytes) -> str:
    """Extract metadata from an image file."""
    try:
        with Image.open(io.BytesIO(content)) as image:
            width, height = image.size
            format_name = image.format
            mode = image.mode

            description = (
                f"Image: {width}x{height} pixels, {format_name} format, {mode} mode.\n"
                "This is an image file. The AI can see this image and refer to its contents in the conversation."
            )
            return description
    except Exception as e:
        return f"Error processing image: {str(e)}"

async def parse_pdf(content: bytes) -> str:
    """Extract text from a PDF file using pypdf."""
    try:
        pdf = PdfReader(io.BytesIO(content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text.strip() if text.strip() else "This PDF appears to be a scanned document with no extractable text."
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

async def parse_docx(content: bytes) -> str:
    """Extract text from a DOCX file."""
    try:
        doc = docx.Document(io.BytesIO(content))
        text = "\n".join(para.text for para in doc.paragraphs)

        for table in doc.tables:
            for row in table.rows:
                text += "\n" + " ".join(cell.text for cell in row.cells)

        return text.strip()
    except Exception as e:
        return f"Error processing DOCX: {str(e)}"
