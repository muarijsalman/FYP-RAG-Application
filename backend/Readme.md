# RAG Implementation and FastAPI Wrapper for FYP Project Retrieval System

### Embedding Router

Endpoint: `/api/encode-doc`
<b>Input Parameters</b>

-   project_id: UUID4
-   document: UploadFile
-   project_title: str

Example CURL Request

```
curl --location 'http://localhost:8000/api/encode-doc' \
--form 'document=@"/Users/muhammadarham/Downloads/article_logos/BooksforSystemDesign/clean_arch.jpg"' \
--form 'project_title="\"Test Project\""' \
--form 'project_id="c6e65570-1e5b-41f7-baf5-18b7bcef7275"'
```

Example Response

```
{
    "upload_success": True
}
```

<hr>
### Query Router

Endpoint: `/api/query-reports`
<b>Input Parameters</b>

-   query: str

Example CURL Request

```
curl --location 'http://localhost:8000/api/query-reports' \
--form 'query="How to improve web development using LLMs?"'
```

Example Response
Returns a List of Dictionaires containing ID, Title, and Public URL of PDF Report

```
[
    {
        "project_id": "73ecaecd-a507-4f15-aa22-c273889b742f",
        "project_title": "FreeFlow – A No Code Web App Builder",
        "project_url": "https://pub-f1a5a2e275a945dcb4de83d2738a22bf.r2.dev/reports/73ecaecd-a507-4f15-aa22-c273889b742f.pdf"
    },
    {
        "project_id": "31c37527-dc1b-4c25-9fb7-b4e744f0a433",
        "project_title": "PALL: Personalized AI-driven Learning empowered by LLMs",
        "project_url": "https://pub-f1a5a2e275a945dcb4de83d2738a22bf.r2.dev/reports/31c37527-dc1b-4c25-9fb7-b4e744f0a433.pdf"
    }
]
```

<br>
Endpoint: `/api/query-posters`
<b>Input Parameters</b>

-   image: UploadFile

Example CURL Request

```
curl --location 'http://localhost:8000/api/query-posters' \
--form 'image=@"/Users/muhammadarham/Drive/LLMProjectData/data/posters/3.jpg"'
```

Example Response
Returns a List of Dictionaires containing ID, Title, and Public URL of PDF Report

```
[
    {
        "project_id": "011d9e6d-c64d-4de1-a7d1-362f5277701c",
        "project_title": "FuristicCinetic",
        "project_url": "https://pub-f1a5a2e275a945dcb4de83d2738a22bf.r2.dev/posters/011d9e6d-c64d-4de1-a7d1-362f5277701c.png"
    },
    {
        "project_id": "8dc17087-65b4-40e7-b320-21d23773ca70",
        "project_title": "Securing SCADA based Systems through Proactive Audit, Monitoring and Control",
        "project_url": "https://pub-f1a5a2e275a945dcb4de83d2738a22bf.r2.dev/posters/8dc17087-65b4-40e7-b320-21d23773ca70.png"
    },
    {
        "project_id": "b9607962-8f33-4e94-934c-84a599b3414f",
        "project_title": "AirAI: To Monitor Air Quality Using Artificial Intelligence",
        "project_url": "https://pub-f1a5a2e275a945dcb4de83d2738a22bf.r2.dev/posters/b9607962-8f33-4e94-934c-84a599b3414f.png"
    },
    {
        "project_id": "73ecaecd-a507-4f15-aa22-c273889b742f",
        "project_title": "FreeFlow – A No Code Web App Builder",
        "project_url": "https://pub-f1a5a2e275a945dcb4de83d2738a22bf.r2.dev/posters/73ecaecd-a507-4f15-aa22-c273889b742f.png"
    }
]
```
