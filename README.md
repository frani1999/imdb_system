# IMDb System

## Overview

This project implements a system to access IMDb data using:

- Ingestion of IMDb data from https://datasets.imdbws.com into a **system Database**
- **REST API server** to get information about films and people
- **CLI client** to query data from **REST API server** and show the responses
- **Docker** to have a production-ready solution that can be run anywhere

---

## Project Structure

```plaintext
├── system_module_1/            # Database creation, modeling and ingestion
├── system_module_2/
│   ├── client/                 # CLI client
│   └── server/                 # API REST server, endpoints, SQL queries
├── tests/                      # Unit testing
├── .env                        # Production environment
├── .env.local                  # Development environment
├── docker-compose.yml          # Docker configuration
├── Dockerfile                  # Build docker image
```


---

## Getting Started

Please refer to:

- [`User_documentation.md`](User_documentation.md) → How to run and use the system
- [`Implementation_notes.md`](Implementation_notes.md) → Internal architecture and design

---