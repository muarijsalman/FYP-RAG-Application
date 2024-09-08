from typing import Dict
from fastapi import APIRouter, Depends, UploadFile, HTTPException
from vectordb.pineconedb import PineconeVectorDB
from models.embed import EmbeddingModel
from pydantic import BaseModel
from utils import as_form, get_aws_public_url
from models.document_parser import is_img
from io import BytesIO
from PIL import Image
from cloudflare.storage import CloudflareR2


@as_form
class TextualQueryInputParams(BaseModel):
    query: str

@as_form
class ImageQueryInputParams(BaseModel):
    image: UploadFile

class QueryRouter(APIRouter):
    def __init__(self):
        self.router = APIRouter()
        self.vectordb = PineconeVectorDB()
        self.embed_model = EmbeddingModel()
        self.cloudflare_public_url = get_aws_public_url()
        self.r2_storage = CloudflareR2()
        
        self.router.add_api_route('/query-posters', self.image_query, methods=["POST"])
        self.router.add_api_route('/query-posters/', self.image_query, methods=["POST"])
        
        self.router.add_api_route('/query-reports', self.textual_query, methods=["POST"])
        self.router.add_api_route('/query-reports/', self.textual_query, methods=["POST"])
    
    
    def _get_ids_from_matches(self, matches: Dict, folder: str, extension: str):
        unique_ids = {}
        project_title_mapper = {}
        for match in matches:
            project_id = match['metadata']['fyp-id']
            project_title = match['metadata']['title']
            if not project_id in project_title_mapper:
                project_title_mapper[project_id] = project_title
            if project_id in unique_ids:
                unique_ids[project_id] += 1
            else:
                unique_ids[project_id] = 1
        sorted_ids = sorted(unique_ids, key=unique_ids.get, reverse=True)
        return_dict = list(map(
            lambda x: {
                "project_id": x,
                "project_title": project_title_mapper[x],
                "project_url": f"{self.cloudflare_public_url.strip("/")}/{folder}/{x}.{extension}"
            }
        , sorted_ids))
        return return_dict
    
    def textual_query(self, input_data: TextualQueryInputParams = Depends()):
        query_embedding = self.embed_model.encode_text(input_data.query).squeeze(0)
        matches = self.vectordb.query_db(
            query_vector=query_embedding.tolist(),
            top_k=10,
            filters={
                "source": "report"
            }
        )
        return self._get_ids_from_matches(matches, folder="reports", extension="pdf")

    async def image_query(self, input_data: ImageQueryInputParams = Depends()):
        if not is_img(input_data.image):
            raise HTTPException(status_code=400, detail="Only image file types supported.")
        
        contents = await input_data.image.read()
        img = Image.open(BytesIO(contents))
        img_encoding = self.embed_model.encode_image(img).squeeze(0)
        matches = self.vectordb.query_db(
            query_vector=img_encoding.tolist(),
            top_k=10,
            filters={
                "source": "poster"
            }
        )
        return self._get_ids_from_matches(matches, folder="posters", extension="png")
        
        
        
        