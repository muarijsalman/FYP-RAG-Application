from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers.embed_router import EmbeddingRouter
from routers.query_router import QueryRouter

app = FastAPI()
app.include_router(EmbeddingRouter().router, prefix='/api')
app.include_router(QueryRouter().router, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)