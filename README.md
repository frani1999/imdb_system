# 1. Getting Started

*Explain how to download, install and configure the project...* TBD

# 2. Run into Local

in project root (*.../imdb_system/*):

## 2.1 Run docker for postgresSQL

```bash
docker run --name imdb_pg -e POSTGRES_USER=imdb_user -e POSTGRES_PASSWORD=imdb_pass -e POSTGRES_DB=imdb_db -p 5431:5432 -d postgres
```

## 2.2 Run ingest

```bash
python -m system_module_1.ingest
```

## 2.3 Run Server

```bash
uvicorn system_module_2.server.server:app --reload --host 127.0.0.1 --port 8000
```

## 2.4 Run Clients

```bash
# Take the default API REST URL (http://localhost:8000)
python -m system_module_2.client.client people "Bruce Lee"
python -m system_module_2.client.client films "Blacksmith Scene"
# Take the specified API REST URL (--api-url)
python -m system_module_2.client.client people "Bruce Lee" --api-url http://localhost:8000
python -m system_module_2.client.client films "Blacksmith Scene" --api-url http://localhost:8000
```

## 2.5 Run Tests
TBD

# 3. Run into docker


## 3.1 Docker: Build + Run Server

in project root (*.../imdb_system/*):

```bash
# Build image
docker-compose build
# Start services
docker-compose up -d
```
After that, server will be running.

## 3.2 Execute Ingest into docker
Starting Load data in PostgreSQL
```bash
docker-compose exec api python -m system_module_1.ingest
```

## 3 Execute Client CLI into docker
```bash
# Type one of these commands for person (example)
docker-compose exec api python -m system_module_2.client.client people "Bruce Lee"
docker-compose exec api python -m system_module_2.client.client people "Bruce Lee" --api-url http://localhost:8000
# Type one of these commands for film (example)
docker-compose exec api python -m system_module_2.client.client films "Blacksmith Scene"
docker-compose exec api python -m system_module_2.client.client films "Blacksmith Scene" --api-url http://localhost:8000
```

# 4. Others

## 4.1 Database URL

Database URL will be set automatically depending on the environment of execution (see [db.py](system_module_1/db.py)).

#### Database URL for Local ([.env.local](.env.local)) 

```postgresql://imdb_user:imdb_pass@localhost:5431/imdb_db```

#### Database URL for Docker ([.env](.env)) 

```postgresql://imdb_user:imdb_pass@db:5432/imdb_db```

## 4.2 Server Host and port

Server host and port can be set in these two lines of [Dockerfile](Dockerfile).

```bash
# Port exposed
EXPOSE 8000

# Start server
CMD ["uvicorn", "system_module_2.server.server:app", "--host", "0.0.0.0", "--port", "8000"]
```