from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
from docx import Document
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

IMAGE_TYPES = ("png", "jpg")
ocr_model = ocr_predictor(pretrained=True)

def get_file_extension(filename: str):
    return filename.split(".")[-1]


def is_img(file: UploadFile):
    if get_file_extension(file.filename) in IMAGE_TYPES:
        return True
    return False

def read_pdf_document(_file: UploadFile):
    reader = PdfReader(_file.file)
    pages_text = []
    for page in reader.pages:
        pages_text.append(page.extract_text())
    return "\n\n".join(pages_text)
        
def read_docx(_file: UploadFile):
    doc = Document(_file.file)
    paras_text = []
    for para in doc.paragraphs:
        paras_text.append(para.text)
    return "\n".join(paras_text)

def parse_text_document(_file: UploadFile):
    file_extension = get_file_extension(_file.filename)
    match file_extension.lower():
        case "pdf":
            text = read_pdf_document(_file)
        # case "docx":
        #     text = read_docx(_file)
        case _:
            raise HTTPException(status_code=400, detail="Bad Request. Only PDF or Docx supported for text documents")
    return text