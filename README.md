## FastAPI Web Application

This is a web application built with Python's FastAPI framework.
The application provides endpoints for:

- user signup, login,
- adding, retrieving, and deleting posts

The app user token-based authentication and caches posts in memory for optimal performance.

## Setup

This server has been developed and tested using Python 3.10.11.

### Install

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Environment Variables

Copy `.env.example` to `.env` and update `DATABASE_URL` to match your database settings

### Initialize database

```
mysql -u root
...
mysql> create database mvc;
```

Update `sqlalchemy.url = mysql+mysqlconnector://root:@localhost/mvc` in `alembic.ini`

```bash
alembic upgrade head
```

## Run

From the root of this repo:
`cd app`

```bash
uvicorn main:app --reload
```

The local server will run on `http://127.0.0.1:8000`.

### View API Docs

The API documentation is viewable at `http://127.0.0.1:8000/docs`.

### Test the API

Register

```bash
curl --header "Content-Type: application/json"  --data '{"email": "john@example.com", "password": "12345678"}' http://localhost:8000/signup
```

Login

```bash
curl -i -X POST -H "Content-Type: application/x-www-form-urlencoded"  -d "username=john@example.com&password=12345678"  http://localhost:8000/login
```

copy the access token returned

```bash
export ACCESS=accesstoken
```

Add post

```bash
curl -i -X POST  -H "Content-Type: application/json" --header "Authorization: Bearer $ACCESS" --data '{"text": "test"}' localhost:8000/posts
```

List posts

```bash
curl --header "Authorization: Bearer $ACCESS" localhost:8000/posts
```

Delete post

```bash
curl -i -X DELETE --header "Authorization: Bearer $ACCESS" localhost:8000/posts/1
```
