# FastAPI Blog API

REST backend for a blogging platform built with FastAPI, SQLAlchemy and SQLite, with JWT authentication.

## What it does
- Register and log in. Login returns a JWT bearer token. Passwords are hashed with Bcrypt.
- 14 REST endpoints for authentication, users and posts.
- Anyone can read published posts. Creating posts and reading other data needs a token.
- Updating or deleting a post returns 403 unless the caller is the post's author or a superuser.
- Pydantic schemas validate request and response bodies.
- Interactive docs: Swagger UI at `/docs`, ReDoc at `/redoc`.

## Project structure

    app/
      main.py          FastAPI entry point
      config.py        settings, read from .env
      database.py      SQLAlchemy engine and session
      models/          user.py, post.py
      schemas/         user.py, post.py, token.py
      routers/         auth.py, users.py, posts.py
      crud/            user.py, post.py
      utils/           security.py (hashing, JWT), dependencies.py

## Run locally
Prerequisites: Python 3.

    git clone https://github.com/Mohitkundu360/fastapi-blog-api.git
    cd fastapi-blog-api
    python -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
    cp .env.example .env
    uvicorn app.main:app --reload

On macOS or Linux, activate with `source venv/bin/activate`. Edit `.env` and set your own `SECRET_KEY`. Settings include `DATABASE_URL`, `SECRET_KEY`, `ALGORITHM` and `ACCESS_TOKEN_EXPIRE_MINUTES`. The API runs on http://localhost:8000.

## Endpoints

| Area | Method and path | Notes |
|---|---|---|
| Auth | POST `/auth/register` | create a user |
| Auth | POST `/auth/login` | returns a JWT |
| Users | GET `/users/me` | current user |
| Users | GET `/users/` | all users, token required |
| Users | GET `/users/{user_id}` | token required |
| Users | PUT `/users/{user_id}` | own profile only |
| Users | DELETE `/users/{user_id}` | own profile only |
| Posts | POST `/posts/` | token required |
| Posts | GET `/posts/` | published posts, public |
| Posts | GET `/posts/all` | all posts, token required |
| Posts | GET `/posts/my-posts` | current user's posts |
| Posts | GET `/posts/{post_id}` | public if published |
| Posts | PUT `/posts/{post_id}` | author or superuser, otherwise 403 |
| Posts | DELETE `/posts/{post_id}` | author or superuser, otherwise 403 |

## Example requests

Register:

    curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{"email":"user@example.com","username":"johndoe","password":"secretpassword"}'

Log in (form data):

    curl -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=johndoe&password=secretpassword"

Create a post:

    curl -X POST "http://localhost:8000/posts/" -H "Authorization: Bearer YOUR_TOKEN" -H "Content-Type: application/json" -d '{"title":"My first post","content":"Hello","published":true}'

## Security notes
- Passwords are hashed with Bcrypt. Tokens are signed JWTs.
- Database access goes through the SQLAlchemy ORM.
- Request bodies are validated by Pydantic schemas.
- Post update and delete check the author on the server side.

## Limitations
- No automated tests and no CI yet.
- SQLite by default, no migration tool.
- Not deployed. Use a strong `SECRET_KEY` and a production database before deploying anywhere.

## Author
Mohit Kundu. [GitHub](https://github.com/Mohitkundu360) | [LinkedIn](https://www.linkedin.com/in/mohitkundu-backend)
