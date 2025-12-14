"""
Pydantic models for request and response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class QuestionRequest(BaseModel):
    """Request model for FAQ questions."""
    question: str = Field(..., min_length=1, description="The question in Bengali")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "প্রাথমিক শিক্ষা কত বছরের হয়?"
            }
        }


class AnswerResponse(BaseModel):
    """Response model for FAQ answers."""
    answer: str = Field(..., description="The answer in Bengali")
    category: str = Field(..., description="Category in English (e.g., education)")
    category_bangla: str = Field(..., description="Category in Bengali (e.g., শিক্ষা)")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, or hard")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "বাংলাদেশে প্রাথমিক শিক্ষা ৫ বছরের।",
                "category": "education",
                "category_bangla": "শিক্ষা",
                "difficulty": "easy"
            }
        }


class CategoryDetectionRequest(BaseModel):
    """Request model for category detection."""
    question: str = Field(..., min_length=1, description="The question to classify")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "প্রাথমিক শিক্ষা কত বছরের হয়?"
            }
        }


class CategoryResponse(BaseModel):
    """Response model for category detection."""
    category: str = Field(..., description="Detected category in English")
    category_bangla: str = Field(..., description="Detected category in Bengali")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "education",
                "category_bangla": "শিক্ষা"
            }
        }


class CategoryInfo(BaseModel):
    """Information about a single category."""
    key: str = Field(..., description="Category key in English")
    name: str = Field(..., description="Category name in Bengali")


class CategoriesResponse(BaseModel):
    """Response model listing all available categories."""
    categories: List[CategoryInfo]
    
    class Config:
        json_schema_extra = {
            "example": {
                "categories": [
                    {"key": "education", "name": "শিক্ষা"},
                    {"key": "health", "name": "স্বাস্থ্য"}
                ]
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Health status")
    vector_store_initialized: bool = Field(..., description="Whether vector store is ready")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "vector_store_initialized": True
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Invalid request",
                "detail": "Question field is required"
            }
        }
