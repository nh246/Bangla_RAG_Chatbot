"""
FastAPI application for Bengali RAG FAQ Bot.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings, CATEGORY_MAP
from app.models import (
    QuestionRequest,
    AnswerResponse,
    CategoryDetectionRequest,
    CategoryResponse,
    CategoriesResponse,
    CategoryInfo,
    HealthResponse,
    ErrorResponse
)
from app.services.vector_store import vector_store_manager
from app.services.rag_service import ask_faq_bot, detect_category

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize vector store on application startup."""
    logger.info("Starting up application...")
    try:
        vector_store_manager.initialize()
        logger.info("Application startup complete!")
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        raise


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Bengali RAG FAQ Bot API",
        "version": settings.api_version,
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get(
    "/api/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health Check",
    description="Check if the API and vector store are operational"
)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        vector_store_initialized=vector_store_manager.is_initialized
    )


@app.get(
    "/api/categories",
    response_model=CategoriesResponse,
    tags=["Categories"],
    summary="List Categories",
    description="Get all available FAQ categories"
)
async def get_categories():
    """Get all available categories."""
    categories = [
        CategoryInfo(key=key, name=name)
        for key, name in CATEGORY_MAP.items()
        if key != "general"  # Exclude general category
    ]
    return CategoriesResponse(categories=categories)


@app.post(
    "/api/detect-category",
    response_model=CategoryResponse,
    tags=["Categories"],
    summary="Detect Category",
    description="Detect the category of a question (for debugging/testing)"
)
async def detect_question_category(request: CategoryDetectionRequest):
    """Detect the category of a question."""
    try:
        category_eng = detect_category(request.question)
        category_bangla = CATEGORY_MAP.get(category_eng, "সাধারণ")
        
        return CategoryResponse(
            category=category_eng,
            category_bangla=category_bangla
        )
    except Exception as e:
        logger.error(f"Error detecting category: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to detect category: {str(e)}"
        )


@app.post(
    "/api/ask",
    response_model=AnswerResponse,
    tags=["FAQ"],
    summary="Ask Question",
    description="Ask a question and get an answer from the FAQ bot",
    responses={
        200: {
            "description": "Successful response with answer",
            "model": AnswerResponse
        },
        400: {
            "description": "Invalid request",
            "model": ErrorResponse
        },
        500: {
            "description": "Server error",
            "model": ErrorResponse
        }
    }
)
async def ask_question(request: QuestionRequest):
    """
    Main FAQ endpoint - asks a question and returns an answer.
    
    - **question**: The question in Bengali
    """
    try:
        # Validate vector store is initialized
        if not vector_store_manager.is_initialized:
            raise HTTPException(
                status_code=503,
                detail="Vector store not initialized. Please try again later."
            )
        
        # Get answer from RAG service
        answer, category_eng, difficulty = ask_faq_bot(request.question)
        category_bangla = CATEGORY_MAP.get(category_eng, "সাধারণ")
        
        return AnswerResponse(
            answer=answer,
            category=category_eng,
            category_bangla=category_bangla,
            difficulty=difficulty
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your question: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
