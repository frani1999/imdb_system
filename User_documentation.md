# User Documentation

## 1. Requirements
For download, configure and run [imdb_system](https://github.com/frani1999/imdb_system.git), user must have installed:
- **Python 3.10** (recommended version) → download [here](https://www.python.org/downloads/release/python-3100/)
- **Git** → download [here](https://git-scm.com/)
- **Docker** → download [here](https://www.docker.com/)
- Internet access for download [IMDb data](https://datasets.imdbws.com/)

----

# 2. Getting Started

Run next commands in terminal: 

1. **Clone repository**
```bash
   git clone https://github.com/frani1999/imdb_system.git
   cd imdb_system
   ```
2. **Install dependencies**
```bash
   pip install -r requirements.txt
```
---

# 3. Run IMDb System

## 3.1 Run into Local

1. **Run docker for PostgreSQL system database**
```bash
docker run --name imdb_pg -e POSTGRES_USER=imdb_user -e POSTGRES_PASSWORD=imdb_pass -e POSTGRES_DB=imdb_db -p 5431:5432 -d postgres
```
2. **Run ingest**

```bash
python -m system_module_1.ingest
```
3. **Run server**
```bash
# REST API Server address can be configured in parameters --host and --port
uvicorn system_module_2.server.server:app --reload --host 127.0.0.1 --port 8000
```
4. **Run clients**
```bash
# Take the default API REST URL (http://localhost:8000)
python -m system_module_2.client.client people "Bruce Lee"
python -m system_module_2.client.client films "Blacksmith Scene"
# Take the specified API REST URL (--api-url)
python -m system_module_2.client.client people "Bruce Lee" --api-url http://localhost:8000
python -m system_module_2.client.client films "Blacksmith Scene" --api-url http://localhost:8000
```

---

## 3.2 Run into Docker

1. **Docker: Build + Run Server**
```bash
# Build image
docker-compose build
# Start services
docker-compose up -d
```
After that, the server will run in docker.

2. **Execute Ingest into docker**

Starts Load data in PostgreSQL
```bash
docker-compose exec api python -m system_module_1.ingest
```

3. **Execute Client CLI into docker**
```bash
# Type one of these commands for person (example)
docker-compose exec api python -m system_module_2.client.client people "Bruce Lee"
docker-compose exec api python -m system_module_2.client.client people "Bruce Lee" --api-url http://localhost:8000
# Type one of these commands for film (example)
docker-compose exec api python -m system_module_2.client.client films "Blacksmith Scene"
docker-compose exec api python -m system_module_2.client.client films "Blacksmith Scene" --api-url http://localhost:8000
```

---

## 3.3 Run Unit Tests

All the implemented tests are intended to check the proper behavior of the developed functionalities.

### 3.3.1 Test ingest

```bash
python -m unittest tests.test_ingest
```

### 3.3.2 Tests endpoints and requests

```bash
# Run test_films.py
python -m unittest tests.test_films
# Run test_people.py
python -m unittest tests.test_people
```

### 3.3.3 Test concurrent requests

```bash
python -m unittest tests.test_conc_requests
```

---

# 4. Others

## 4.1 Database URL

PostgreSQL system database URL will be set automatically depending on the environment of execution (see [db.py](system_module_1/db.py)).

  * Database URL for Local ([.env.local](.env.local)) → ```postgresql://imdb_user:imdb_pass@localhost:5431/imdb_db```

  * Database URL for Docker ([.env](.env)) → ```postgresql://imdb_user:imdb_pass@db:5432/imdb_db```

## 4.2 Server Host and port

REST API Server host and port can be set in these two lines of [Dockerfile](Dockerfile).

```bash
# Port exposed
EXPOSE 8000 # REST API Server port
EXPOSE 5432 # PostgreSQL system database port

# Start server
CMD ["uvicorn", "system_module_2.server.server:app", "--host", "0.0.0.0", "--port", "8000"]
```
