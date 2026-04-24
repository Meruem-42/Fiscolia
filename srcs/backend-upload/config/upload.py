from fastapi import FastAPI, File, UploadFile
import tempfile
import shutil
import os
import fitz
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions

app = FastAPI()

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    temp_path = None
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
		
		# Analyzing PDF
        result = analyze(temp_path)

        return {
			"message": "Recieved and analyzed file",
			"filename": file.filename,
			"content_type": file.content_type,
			"status": "success",
            "analysis": result,
		}
    
    finally:
		# Clean removal of the file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def detect_pdf_type(path: str) -> str:
    doc = fitz.open(path)

    total_chars = 0
    total_images = 0

    for page in doc:
        text = page.get_text().strip()
        total_chars += len(text)
        total_images += len(page.get_images())

    doc.close()

    # to modify according to our tested documents
    if total_chars > 100:
        return "native"
    if total_images > 0 and total_chars < 50:
        return "scanned"

    return "unknown"

def extract_native(path: str) -> str:
    """PDF natif : extraction directe, pas besoin d'OCR"""
    converter = DocumentConverter()
    result = converter.convert(path)
    return result.document.export_to_markdown()

def extract_scanned(path: str) -> str:
    """PDF scanné : activation de l'OCR dans Docling"""
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True

    converter = DocumentConverter(
        format_options={
            "pdf": PdfFormatOption(pipeline_options=pipeline_options)
        }
    )
    result = converter.convert(path)
    return result.document.export_to_markdown()

def analyze(path: str) -> dict:
    print("We will try to analyze and extract data from the uploaded file")
    pdf_type = detect_pdf_type(path)
    
    if pdf_type == "native":
        text = extract_native(path)
    else:
        text = extract_scanned(path)
    
    return {
        "pdf_type": pdf_type,
        "extracted_text": text,
    }