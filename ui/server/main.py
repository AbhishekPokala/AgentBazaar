from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from config import settings
from db.database import init_db

# Import routers
from routers.agents import router as agents_router
from routers.tasks import router as tasks_router
from routers.invoke import router as invoke_router
from routers.hubchat import router as hubchat_router
from routers.messages import router as messages_router
from routers.payments import router as payments_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup/shutdown"""
    # Startup
    logger.info("Starting Agent Bazaar API...")
    logger.info("Initializing database...")
    await init_db()
    logger.info("Database initialized successfully")
    yield
    # Shutdown
    logger.info("Shutting down Agent Bazaar API...")


# Create FastAPI app
app = FastAPI(
    title="Agent Bazaar API",
    description="FastAPI backend for multi-agent orchestration platform",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents_router)
app.include_router(tasks_router)
app.include_router(invoke_router)
app.include_router(hubchat_router)
app.include_router(messages_router)
app.include_router(payments_router)


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "service": "Agent Bazaar API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.SERVER_PORT,
        reload=True
    )
