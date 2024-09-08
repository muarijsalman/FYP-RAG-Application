from fastapi import APIRouter, UploadFile, Depends, HTTPException
from pydantic import BaseModel, UUID4
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PIL import Image
from io import BytesIO
import os
from cloudflare.storage import CloudflareR2
from vectordb.pineconedb import PineconeVectorDB
from models.embed import EmbeddingModel
from utils import as_form
from models.document_parser import parse_text_document, is_img, get_file_extension


@as_form
class EncodeRequestValidator(BaseModel):
    document: UploadFile
    project_title: str
    project_id: UUID4


class EmbeddingRouter(APIRouter):
    def __init__(self):
        self.router = APIRouter()
        self.vectordb = PineconeVectorDB()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50,
            length_function=len
        )
        self.embedding_model = EmbeddingModel()
        self.r2_storage = CloudflareR2()
        
        self.router.add_api_route('/encode-doc', self.encode_document, methods=["POST"])
        self.router.add_api_route('/encode-doc/', self.encode_document, methods=["POST"])
        
    
    async def encode_document(self, input_data: EncodeRequestValidator = Depends()):
        if not is_img(input_data.document):
            file_name = f"{input_data.project_id}.{get_file_extension(input_data.document.filename)}"
            file_path = os.path.join("reports", file_name)
            success = self.r2_storage.upload_document(input_data.document, file_path=file_path)
            if not success:
                raise HTTPException(status_code=500, detail="Error uploading document to bucket.")
            
            await input_data.document.seek(0)
            text = parse_text_document(input_data.document).replace("\n", " ") # DocumentReader Adds \n after every word for some reason. ToDo
            
            texts = self.text_splitter.create_documents([text])
            chunks = self.text_splitter.split_documents(texts)
            vectors = []
            for chunk_id, chunk in enumerate(chunks):
                embedding = self.embedding_model.encode_text(chunk.page_content)
                vectors.append({
                    "id": f"{input_data.project_id}_{chunk_id}",
                    "values": embedding.squeeze(0), # From [1,512] to 1-D [512] Embedding
                    "metadata": {
                        "fyp-id": str(input_data.project_id),
                        "text": chunk.page_content,
                        "chunk-id": chunk_id,
                        "title": input_data.project_title,
                        "source": "report"
                    }
                })
            self.vectordb.upsert_vectors(vectors)
            return True
        
        file_name = os.path.join("posters", f'{input_data.project_id}.png')
        success = self.r2_storage.upload_document(input_data.document, file_path=file_name)
        if not success:
            raise HTTPException(status_code=500, detail="Error uploading document to bucket.")
        await input_data.document.seek(0)
        contents = await input_data.document.read()
        img = Image.open(BytesIO(contents))
        embedding = self.embedding_model.encode_image(img).squeeze(0)
        vectors = [{
            "id": f"{input_data.project_id}_poster",
            "values": embedding,
            "metadata": {
                "fyp-id": str(input_data.project_id),
                "title": input_data.project_title,
                "source": "poster"
            }
        }]
        self.vectordb.upsert_vectors(vectors)
        
        return {
            "upload_success": True
        }
        