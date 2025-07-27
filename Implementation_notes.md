# Implementation Notes

[imdb_system](https://github.com/frani1999/imdb_system.git) aims to implement a system to access IMDb data. 
For this purpose, the following modules have been developed:
  * **system_module_1** → Ingestion of IMDb data (from https://datasets.imdbws.com) into a [PostgreSQL](https://www.postgresql.org/) system database.
  * **system_module_2** → Client-server architecture for scalability and stability.
    * **Server:** REST API with two endpoints to get information about people and films, stored in PostgreSQL system database.
    * **Client:** CLI application to query data from **REST API server** and show the responses.

![imdb_system Diagram](images/imdb_system_diagram.jpg)

----

## 1. Project Architecture

```plaintext
imdb_system
├── images/                     # Documentation images
├── system_module_1/            # Database creation, modeling and ingestion
│   ├── db.py                   # PostgreSQL Database creation
│   ├── ingest.py               # Data ingestion into system database 
│   └── models.py               # System database modeling
│
├── system_module_2/            # REST API Client-server architecture
│   ├── client/                 # CLI client
│   │   └── client.py           # People and movies requests
│   └── server/                 # API REST server, endpoints, SQL queries
│       ├── server.py           # REST API creation and endpoints registration
│       ├── endpoints/          # REST API endpoints
│       │   ├── films.py        # Endpoint to get films
│       │   └── people.py       # Endpoint to get people
│       └── services/           # Access from REST API to Database
│           └── queries.py      # SQL queries (film, person)
│
├── tests/                      # Unit testing
│   ├── test_conc_request.py    # Test concurrent request to REST API server
│   ├── test_films.py           # Test get films
│   ├── test_ingest.py          # Test data ingestion into database
│   └── test_people.py          # Test get people 
│
├── .env                        # Production environment (database URL)
├── .env.local                  # Development environment (database URL)
├── docker-compose.yml          # Docker configuration
├── Dockerfile                  # Build docker image
├── Implementation_notes.md     # Technical description of the project
├── README.md                   # General description of the project
├── User_documentation.md       # Usage description of the project
└── requirements.txt            # Python dependencies of the project
```

----

## 2. Detailed Functionality

### 2.1 system_module_1

The main program for system_module_1 is [ingest.py](system_module_1/ingest.py). This code implements:

  1. **Create and prepare the database (`setup_database()` function)**.
     1. Create a PostgreSQL system database called `imdb_db.db`, that is defined in [db.py](system_module_1/db.py). 
        * **NOTE:** URL Database will be chosen depending on the environment of execution. For local development, uses URL in [.env.local](.env.local). For docker production, the URL used is in [.env](.env). 
        ```bash
            # PostgreSQL system database URL local development (.env.local)
            DATABASE_URL=postgresql://imdb_user:imdb_pass@localhost:5431/imdb_db
            # PostgreSQL system database URL for docker production (.env)
            DATABASE_URL=postgresql://imdb_user:imdb_pass@db:5432/imdb_db
         ```
     2. Database shall have two tables, `Person` and `Title`, whose data format is specified in [models.py](system_module_1/models.py).
        * **NOTE:** These classes have been created with the required information only. More fields can be added if required in the future (e.g. *isAdult* in titles).
     3. If database is just created, code will drop both tables for restart the data ingestion. This feature will be useful to clean up database and reload the data.
  2. **Download files from https://datasets.imdbws.com (`download_file(filename)` function).**
     1. This function will download `title.basics.tsv.gz` (films information) and `name.basics.tsv.gz` (people information) zipped files. 
  3. **interleaved ingest (`interleaved_ingest(batch_size)`function).**
     1. This function will unzip, open and read `title.basics.tsv.gz` and `name.basics.tsv.gz`.
     2. The code will read interleaved data from both files in batches, the size of which shall be specified in the parameter *batch_size* (10000 by default). This means that code will read first 10000 people and then 10000 titles.
     3. Each batch shall be ingested in PostgreSQL system database.
  4. **Other functions.**
     1. `ingest_all()` → ingest first all people (`name.basics.tsv.gz`), next all titles (`title.basics.tsv.gz`).
        * **NOTE:** this function is deprecated, as it is inefficient to separate ingest.
     2. `load_titles(session, filepath, batch_size)` → function to ingest only titles.
     3. `load_names(session, filepath, batch_size)` → function to ingest only people.

### 2.2 system_module_2

#### 2.2.1 Client

The main program for system_module_2/client is [client.py](system_module_2/client/client.py). This code implements:

  1. **CLI (Command Line Interface).** Client shall be run with commands lines indicating:
     * **Type of request** → people or films.
     * **REST API URL** → `http://<host>:<port>`. If not specified, `http://localhost:8000` shall be taken.
     ```bash
        # Take the default API REST URL (http://localhost:8000)
        # Search for people
        python -m system_module_2.client.client people "Bruce Lee"
        # Search for films
        python -m system_module_2.client.client films "Blacksmith Scene"
        # Take the specified API REST URL (--api-url)
        # Search for people
        python -m system_module_2.client.client people "Bruce Lee" --api-url http://localhost:8000
        # Search for films
        python -m system_module_2.client.client films "Blacksmith Scene" --api-url http://localhost:8000
        ```
  2. **Request functions to REST API server.** Each *Type of request* implements a function to make a request to REST API server.
     * `people` | `"Bruce lee"` | `http://localhost:8000` → `http://localhost:8000/people/Bruce lee`
     * `films` | `"Blacksmith Scene"` | `http://localhost:8000` → `http://localhost:8000/films/Blacksmith Scene` 

#### 2.2.2 Server

The main program for system_module_2/server is [server.py](system_module_2/server/server.py). This code implements:

  1. **REST API Creation.** App creation with FastAPI, titled *IMDb API*.
  2. **Inclusion of endpoints *APIRouters*.** Assignment of endpoints to the REST API, which are defined in:
     * [.../endpoints/films.py](system_module_2/server/endpoints/films.py) → endpoint to get films. This code shall run when REST API captures a request of type `http://<host>:<port>/films/...`.
     * [.../endpoints/people.py](system_module_2/server/endpoints/people.py) → endpoint to get people. This code shall run when REST API captures a request of type `http://<host>:<port>/people/...`.
     * **NOTE 1:** Concurrent sessions are supported because the endpoints are declared as `async`.
     * **NOTE 2:** each endpoint manages its own session with PostgreSQL system database (`SessionLocal()`). This means that each client shall open a different database session to access the database.
  3. **API REST Server response to CLI client.** Server shall send a summary of the information found in PostgreSQL system database. The functions to query SQL data are implemented at [.../services/queries.py](system_module_2/server/services/queries.py), and are called by [.../endpoints/](system_module_2/server/endpoints/).
     * **NOTE:** SQL queries will return the first match of a name or a film, but sometimes there are more than one match. This is something that can be improved in the future by searching in other files from https://datasets.imdbws.com/ (e.g. `title.ratings.tsv.gz` and show the top-rated result for a film).

### 2.3 Unit Tests

different types of tests have been defined for:

  * **Test ingestion** ([test_ingest.py](tests/test_ingest.py)).
    * Test `load_names(...)`, `load_titles(...)` and `interleaved_ingest(...)` functions from [ingest.py](system_module_1/ingest.py).
    * **Requirements:** 
      * No requirements.
    * **Procedure:** 
      * Creates a *sqlite* in-memory database (RAM).
      * Creates fake tsv files with only one row for people and title.
    * **Verdict:** Checks if data created in fake tsv files has been successfully loaded into the *sqlite* in-memory database.
  * **Tests endpoints and requests** ([test_films.py](tests/test_films.py) and [test_people.py](tests/test_people.py)).
    * Test the server endpoints functions in [.../server/endpoints/](system_module_2/server/endpoints/).
    * **Requirements:** 
      * API REST Server must be running.
      * The ingest process must have entered at least the first batch of size 10000 into the PostgreSQL system database.
    * **Procedure:** 
      * Requests the films or people stored in `film_list` and `people_list`.
    * **Verdict:** Checks that the server gives a valid response and that the requested data is found. 
  * **Test concurrent requests** ([test_conc_requests.py](tests/test_conc_requests.py)).
    * Test that the server can manage Concurrent client sessions.
    * * **Requirements:** 
      * API REST Server must be running.
      * The ingest process must have entered at least the first batch of size 10000 into the PostgreSQL system database.
    * **Procedure:** 
      * many request threads shall be created as specified in the parameter `self.num_requests`.
      * The target URL shall be the same for each thread, specified in `self.target_url`.
    * **Verdict:** Checks if server gives response for each concurrent client.

----

## 3. Libraries Used

To check the list of used libraries, go to [requirements.txt](requirements.txt).

### 3.1 system_module_1
  * **Database creation** ([**db.py**](system_module_1/db.py))
    * [*sqlalchemy*](https://www.sqlalchemy.org/) → create the PostgreSQL system database.
    * [*os*](https://docs.python.org/3/library/os.html) and [*dotenv*](https://pypi.org/project/python-dotenv/) → load the database URL from [.env](.env) (URL for development) or from [.env.local](.env.local) (URL for production). 
  * **Database modeling** ([**models.py**](system_module_1/models.py))
    * [*sqlalchemy*](https://www.sqlalchemy.org/) → customize the system database (define columns and data type).
  * **Ingestion** ([**ingest.py**](system_module_1/ingest.py))
    * [*requests*](https://pypi.org/project/requests/) → download `name.basics.tsv.gz` (people) and `title.basics.tsv.gz` (films) files.
    * [*os*](https://docs.python.org/3/library/os.html) → place and locate the downloaded files.
    * [*gzip*](https://docs.python.org/3/library/gzip.html) → unzip `name.basics.tsv.gz` and `title.basics.tsv.gz` files.
    * [csv](https://docs.python.org/3/library/csv.html) → read information from  `name.basics.tsv` and `title.basics.tsv` (unzipped files).
    * [*sqlalchemy*](https://www.sqlalchemy.org/) → save data into the PostgreSQL system database.

### 3.2 system_module_2
  * **CLI Client** ([**client.py**](system_module_2/client/client.py))
    * [typer](https://typer.tiangolo.com/) → build CLI.
    * [*requests*](https://pypi.org/project/requests/) → get information from REST API server.
  * **Server** ([**.../server/**](system_module_2/server/))
    * **Endpoints** ([**films.py**](system_module_2/server/endpoints/films.py) and [**people.py**](system_module_2/server/endpoints/people.py))
      * [*fastapi*](https://fastapi.tiangolo.com/) → create the *APIRouters*.
    * **Services** ([**queries.py**](system_module_2/server/services/queries.py))
      * [*sqlalchemy*](https://www.sqlalchemy.org/) → make SQL queries to PostgreSQL system database.
    * **REST API Server** ([**server.py**](system_module_2/server/server.py))
      * [*fastapi*](https://fastapi.tiangolo.com/) → create the REST API server and assign the *APIRouters* defined in [endpoints](system_module_2/server/endpoints).
      * [*uvicorn*](https://www.uvicorn.org/) → REST API server execution.

### 3.3 Unit Tests
  * [**test_ingest.py**](tests/test_ingest.py)
    * [*unittest*](http://docs.python.org/3/library/unittest.html) → define unit test.
    * [*gzip*](https://docs.python.org/3/library/gzip.html) → create, save and unzip fake *.tsv* files.
    * [*sqlalchemy*](https://www.sqlalchemy.org/) → save data into the PostgreSQL system database.
  * [**test_conc_requests.py**](tests/test_conc_requests.py)
    * [*unittest*](http://docs.python.org/3/library/unittest.html) → define unit test.
    * [*requests*](https://pypi.org/project/requests/) → get information from REST API server.
    * [*concurrent.futures*](https://docs.python.org/3/library/concurrent.futures.html) → run multiple CLI Clients.
  * [**test_films.py**](tests/test_films.py)
    * [*unittest*](http://docs.python.org/3/library/unittest.html) → define unit test.
    * [*requests*](https://pypi.org/project/requests/) → get information from REST API server.
  * [**test_people.py**](tests/test_people.py)
    * [*unittest*](http://docs.python.org/3/library/unittest.html) → define unit test.
    * [*requests*](https://pypi.org/project/requests/) → get information from REST API server.

----

## 4. Docker Deployment

### 4.1 Docker configuration 
The docker configuration shall be done in [docker-compose.yml](docker-compose.yml). 
  * **Services**
    * **db** → Store the production PostgreSQL system database.
      * Assign user (`POSTGRES_USER: imdb_user`), pass (`POSTGRES_PASSWORD: imdb_password`) and name (`POSTGRES_DB: imdb_db`) of the PostgreSQL system database.
      * Mapping ports to `5432:5432`.
      * Create a volume to store data into the PostgreSQL system database (`imdb_pgdata:/var/lib/postgresql/data`).
      * Test if PostgreSQL system database is ready to receive connections (`test: [ "CMD-SHELL", "pg_isready -U imdb_user" ]`).
    * **api** → Configure the REST API Server to build on docker.
      * Build information indicated in [Dockerfile](Dockerfile).
      * Put Condition to run server: db service must pass the *healthcheck* tests.
      * Mapping ports to `8000:8000`.
      * Copy project directory inside docker in path `.:/app`.
      * Choose the production environment file [.env](.env).
### 4.2 Build docker image 
The docker image Building shall be done in [Dockerfile](Dockerfile).
  * `FROM python:3.10-slim` → Use Python 3.10.
  * `WORKDIR /app` → Create the working directory.
  * `ENV PYTHONPATH=/app` → Change the python path to root folder.
  * `COPY requirements.txt .` → Copy dependencies file.
  * `RUN pip install --no-cache-dir -r requirements.txt` → Install python dependencies.
  * `EXPOSE 8000` and `EXPOSE 5432` → Expose service ports.
  * `COPY system_module_1/ ./system_module_1/` and `COPY system_module_2/ ./system_module_2/` → Copy the source code to the docker.
  * `CMD ["uvicorn", "system_module_2.server.server:app", "--host", "0.0.0.0", "--port", "8000"]` → execute server when start container.

----

## 5. Future Lines
 
[imdb_system](https://github.com/frani1999/imdb_system.git) may need the following potential improvements and fixes:
  1. **In unit tests for endpoints, set the API_REST_URL outside the code.** Now it is inside the code. The parameter can be extracted:
     1. By setting it as an environment variable in [.env.local](.env.local) and extract with [*os*](https://docs.python.org/3/library/os.html) and [*dotenv*](https://pypi.org/project/python-dotenv/) (similar to [db.py](system_module_1/db.py)).
     2. As a parameter in run command (similar as [client.py](system_module_2/client/client.py)).
     ```bash
        python -m unittest tests.test_ingest --api-url http://localhost:8000
        python -m unittest tests.test_films --api-url http://localhost:8000
        python -m unittest tests.test_people --api-url http://localhost:8000
        python -m unittest tests.test_conc_requests --api-url http://localhost:8000
        ```
  2. **In unit tests for endpoints, use the *TestClient* class from FastAPI.** This will make possible to run unit tests without an API REST Server previously running. Some example codes are:
```python
from fastapi.testclient import TestClient
from system_module_2.server.server import app

client = TestClient(app)

def test_get_person():
    response = client.get("/people/Bruce Lee")
    assert response.status_code == 200
    assert "Bruce Lee" in response.json().get("summary", "")
```
```python
from fastapi.testclient import TestClient
from system_module_2.server.server import app

client = TestClient(app)

def test_get_film():
    response = client.get("/films/Blacksmith Scene")
    assert response.status_code == 200
    assert "Blacksmith Scene" in response.json().get("summary", "")
```
  3. **Summary request given in [queries.py](system_module_2/server/services/queries.py) can be completed with more data extracted form https://datasets.imdbws.com/.** It is possible to read and store in PostgreSQL system database more tables with different data, and search people and films information by the `id`. The other *tsv* files are:
   * `title.akas.tsv.gz` → information about films region, language, etc.
   * `title.crew.tsv.gz` → information about films directors and writers.
   * `title.episode.tsv.gz` → information about episodes for TV Series.
   * `title.principals.tsv.gz` → information about persons involved in a film.
   * `title.ratings.tsv.gz` → information about films ratings.
  4. **Migrate REST API to HTTPS.** HTTPS via NGINX (inverse proxy) + TLS Certificates (Let's Encrypt).
   * Ensures that all communication is encrypted.
   * How to make it:
     * Use inverse proxy ([NGINX](https://nginx.org/) or [Traefik](https://traefik.io/traefik)) in front of the API.
     * configure a [Let's Encrypt](https://letsencrypt.org/) SSL certificate (Let's Encrypt offers free, automatically renewable certificates).