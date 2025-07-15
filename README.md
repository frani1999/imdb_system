# Quick Start: Put into production

## Database URL
Add the URL where the Database will be allocated in [.env](.env) file. Recommended:
```bash
# Production
postgresql://imdb_user:imdb_pass@localhost/imdb_db 
# Local, Development
sqlite:///./system_module_1/imdb.db 
```
## Server Host and port

Change in [Dockerfile](Dockerfile) ```"--host", "0.0.0.0"``` by the server IP and ```EXPOSE 8000``` and ```"--port", "8000"```  by the port used.

```bash
# Port exposed
EXPOSE 8000

# Start server
CMD ["uvicorn", "system_module_2.server.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Docker: Build + Run

in project root (*.../imdb_system/*):

```bash
# Type these bash commands
docker-compose build
docker-compose up
```

## Execute Client CLI into docker
```bash
# Type this bash command for person (example)
docker-compose exec api python system_module_2/client/client.py people "Bruce Lee"
# Type this bash command for film (example)
docker-compose exec api python system_module_2/client/client.py films "Blacksmith Scene"
```

## Execute Ingest into docker
```bash
docker-compose exec api python system_module_1/ingest.py
```

MAYBE WE ADD THE COMMAND LINE FOR EXECUTE THE INGEST AND SERVER AT THE SAME TIME IN [Dockerfile](Dockerfile).
```bash
CMD ["sh", "-c", "python system_module_1/ingest.py && uvicorn system_module_2.server.server:app --host 0.0.0.0 --port 8000"]
```

# Future Lines
API CRUD 

