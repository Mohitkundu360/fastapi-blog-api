from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import init_db
from app.routers import auth, users, posts

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A simple and secure Blog API with JWT authentication",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)


@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    print("🚀 Starting Blog API...")
    init_db()
    print("✅ Database initialized successfully!")


@app.on_event("shutdown")
def on_shutdown():
    """Cleanup on shutdown"""
    print("👋 Shutting down Blog API...")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Blog API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)