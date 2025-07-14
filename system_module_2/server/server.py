from fastapi import FastAPI
from system_module_2.server.endpoints import films, people

'''
Start in Local http://127.0.0.1:8000 - "http://localhost:8000":
    uvicorn system_module_2.server.server:app --reload
Specify IP and Port:
    uvicorn system_module_2.server.server:app --reload --host 127.0.0.1 --port 8000
'''

app = FastAPI(title="IMDb API", description="REST API to query IMDb data")

# Register endpoints
app.include_router(people.router, prefix="/people", tags=["People"])
app.include_router(films.router, prefix="/films", tags=["Films"])
