## Setup

This server has been developed and tested using Python 3.10.11.

### Install

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Initialize database

```
mysql -u root
...
mysql> create database mvc;
```

```bash
alembic upgrade head
```

### Environment Variables

## Run

From the root of this repo:
`cd app`

```bash
uvicorn main:app --reload
```

The local server will run on `http://127.0.0.1:8000`.

### View API Docs

The API documentation is viewable at `http://127.0.0.1:8000/docs`.
