# ArticleHub API

Simple articles & auth API built with **FastAPI** and **MongoDB**.

## Tech stack

- FastAPI
- MongoDB (async driver)
- Pydantic & pydantic-settings
- JWT auth
- Pytest (+ mongomock for tests)

## Setup

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
docker compose up --build
```