from fastapi import FastAPI
from system_module_2.server.endpoints import endpoints

'''
Start in Local http://127.0.0.1:8000 - "http://localhost:8000":
    uvicorn system_module_2.server.server_One_endpoint:app --reload
Specify IP and Port:
    uvicorn system_module_2.server.server_One_endpoint:app --reload --host 127.0.0.1 --port 8000
'''

app = FastAPI(title="IMDb API", description="REST API to query IMDb data")

# Register endpoints
app.include_router(endpoints.router_people, prefix="/people", tags=["People"])
app.include_router(endpoints.router_films, prefix="/films", tags=["Films"])
