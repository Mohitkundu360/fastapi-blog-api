Blog API - FastAPI Project
A simple, secure, and well-structured Blog API built with FastAPI, SQLAlchemy, JWT Authentication, and SQLite.
🚀 Features

✅ User Registration & Login with JWT Authentication
✅ Protected Routes for Authenticated Users
✅ Full CRUD Operations for Blog Posts
✅ SQLite Database with SQLAlchemy ORM
✅ Pydantic Schemas for Request/Response Validation
✅ Swagger UI Documentation at /docs
✅ ReDoc Documentation at /redoc
✅ Modular and Scalable Code Structure
✅ Role-based Authorization (Author-only edit/delete)
✅ Password Hashing with Bcrypt
✅ CORS Support

📁 Project Structure
blog_api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── database.py             # Database connection
│   │
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── schemas/                # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── token.py
│   │
│   ├── routers/                # API routes
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── posts.py
│   │
│   ├── crud/                   # Database operations
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   │
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── security.py
│       └── dependencies.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
🛠️ Installation
1. Clone the repository
bashgit clone <repository-url>
cd blog_api
2. Create virtual environment
bashpython -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
3. Install dependencies
bashpip install -r requirements.txt
4. Set up environment variables
bashcp .env.example .env
# Edit .env and add your own SECRET_KEY
5. Run the application
bashpython -m app.main
# or
uvicorn app.main:app --reload
The API will be available at: http://localhost:8000
📚 API Documentation
Once the server is running, visit:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

🔐 API Endpoints
Authentication

POST /auth/register - Register a new user
POST /auth/login - Login and get JWT token

Users

GET /users/me - Get current user profile
GET /users/ - Get all users (protected)
GET /users/{user_id} - Get user by ID (protected)
PUT /users/{user_id} - Update user (own profile only)
DELETE /users/{user_id} - Delete user (own profile only)

Posts

POST /posts/ - Create a new post (protected)
GET /posts/ - Get all published posts (public)
GET /posts/all - Get all posts (protected)
GET /posts/my-posts - Get current user's posts (protected)
GET /posts/{post_id} - Get post by ID (public if published)
PUT /posts/{post_id} - Update post (author only)
DELETE /posts/{post_id} - Delete post (author only)

💡 Usage Examples
1. Register a new user
bashcurl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "secretpassword"
  }'
2. Login
bashcurl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secretpassword"
Response:
json{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
3. Create a post (with authentication)
bashcurl -X POST "http://localhost:8000/posts/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Blog Post",
    "content": "This is the content of my first blog post.",
    "published": true
  }'
4. Get all published posts
bashcurl -X GET "http://localhost:8000/posts/"
🔒 Security Features

Password Hashing: Passwords are hashed using Bcrypt
JWT Authentication: Secure token-based authentication
Protected Routes: Endpoints require valid JWT tokens
Authorization: Users can only edit/delete their own posts
SQL Injection Prevention: SQLAlchemy ORM protects against SQL injection
Input Validation: Pydantic schemas validate all inputs

🧪 Testing
You can test the API using:

Swagger UI at /docs
Postman
cURL commands
Python requests library

📝 Configuration
Edit .env file to customize:

DATABASE_URL - Database connection string
SECRET_KEY - JWT secret key (generate a secure one!)
ALGORITHM - JWT algorithm (default: HS256)
ACCESS_TOKEN_EXPIRE_MINUTES - Token expiration time

🚀 Deployment
For production deployment:

Set DEBUG=False in config
Use a strong SECRET_KEY
Use PostgreSQL instead of SQLite
Set up HTTPS
Use a production ASGI server like Gunicorn with Uvicorn workers