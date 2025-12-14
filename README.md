# Bengali RAG FAQ Bot - FastAPI Backend

A FastAPI-based backend for a Bengali FAQ bot using Retrieval-Augmented Generation (RAG) technology. The system uses FAISS for vector search and integrates with GitHub's AI models for intelligent question answering.

## Features

- 🤖 **AI-Powered FAQ Bot** - Answers questions in Bengali using RAG technology
- 🔍 **Smart Category Detection** - Automatically classifies questions into topics (Education, Health, Travel, Technology, Sports)
- 📊 **Difficulty Assessment** - Determines question complexity (Easy, Medium, Hard)
- 🚀 **Fast & Efficient** - Uses FAISS for rapid vector similarity search
- 💻 **CPU-Optimized** - Works smoothly without a dedicated GPU
- 🌐 **RESTful API** - Clean, well-documented API endpoints
- 📝 **Interactive Docs** - Automatic API documentation with Swagger UI

## Demo Video

[Watch the project demo video](https://drive.google.com/file/d/1pkz4BFhadfm3VtgYZ6OrVUI63lGwiww8/view?usp=sharing)

## Technology Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **LangChain** - Framework for LLM applications
- **FAISS** - Facebook AI Similarity Search (CPU version)
- **Sentence Transformers** - Multilingual embeddings for Bengali support
- **OpenAI API** - Via GitHub Models for text generation
- **Pydantic** - Data validation using Python type annotations

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and FAQ data
│   ├── models.py            # Pydantic request/response models
│   └── services/
│       ├── __init__.py
│       ├── rag_service.py   # RAG logic (retrieval, generation)
│       └── vector_store.py  # Vector store initialization
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Clone or Navigate to Project

```bash
cd "E:\OStad Ai Engeneering\Module 17\assignment\project"
```

### 3. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** First-time installation will download the multilingual embedding model (~420MB). This is a one-time download.

### 5. Configure Environment Variables

Create a `.env` file from the template:

```bash
copy .env.example .env
```

Edit `.env` and add your GitHub token:

```env
GITHUB_TOKEN=your_actual_github_token_here
MODEL_NAME=openai/gpt-4o-mini
BASE_URL=https://models.github.ai/inference
```

### 6. Run the Server

```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m app.main
```

The server will start on `http://localhost:8000`

## API Endpoints

### 📍 Root Endpoint

**GET** `/`

Returns basic API information.

```json
{
  "message": "Bengali RAG FAQ Bot API",
  "version": "1.0.0",
  "docs": "/docs",
  "health": "/api/health"
}
```

---

### 🏥 Health Check

**GET** `/api/health`

Check if the API and vector store are operational.

**Response:**
```json
{
  "status": "healthy",
  "vector_store_initialized": true
}
```

---

### 📚 List Categories

**GET** `/api/categories`

Get all available FAQ categories.

**Response:**
```json
{
  "categories": [
    {"key": "education", "name": "শিক্ষা"},
    {"key": "health", "name": "স্বাস্থ্য"},
    {"key": "travel", "name": "ভ্রমণ"},
    {"key": "technology", "name": "প্রযুক্তি"},
    {"key": "sports", "name": "খেলাধুলা"}
  ]
}
```

---

### 🔍 Detect Category

**POST** `/api/detect-category`

Detect the category of a question (useful for debugging).

**Request:**
```json
{
  "question": "প্রাথমিক শিক্ষা কত বছরের হয়?"
}
```

**Response:**
```json
{
  "category": "education",
  "category_bangla": "শিক্ষা"
}
```

---

### 💬 Ask Question (Main Endpoint)

**POST** `/api/ask`

Ask a question and get an answer from the FAQ bot.

**Request:**
```json
{
  "question": "প্রাথমিক শিক্ষা কত বছরের হয়?"
}
```

**Response:**
```json
{
  "answer": "বাংলাদেশে প্রাথমিক শিক্ষা ৫ বছরের।",
  "category": "education",
  "category_bangla": "শিক্ষা",
  "difficulty": "easy"
}
```

## Testing the API

### Using cURL

```bash
# Health check
curl http://localhost:8000/api/health

# List categories
curl http://localhost:8000/api/categories

# Ask a question
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"প্রাথমিক শিক্ষা কত বছরের হয়?\"}"
```

### Using the Interactive Docs

Visit `http://localhost:8000/docs` in your browser to access the **Swagger UI** where you can:
- See all available endpoints
- Test API calls directly from the browser
- View request/response schemas
- See example requests and responses

### Example Questions to Test

```python
# Education
"প্রাথমিক শিক্ষা কত বছরের হয়?"
"উচ্চশিক্ষার জন্য কী প্রয়োজন?"

# Health
"সুস্থ থাকার মূল উপায় কী?"
"দৈনিক কতটুকু পানি পান করা উচিত?"

# Travel
"বাংলাদেশের দীর্ঘতম সমুদ্র সৈকত কোনটি?"
"সুন্দরবন কেন বিখ্যাত?"

# Technology
"এআই (AI) বলতে কী বোঝো?"
"ক্লাউড স্টোরেজ কী?"

# Sports
"বাংলাদেশের সবচেয়ে জনপ্রিয় খেলা কোনটি?"
"ফুটবল খেলায় কতজন খেলোয়াড় থাকে?"

# Out of scope (tests fallback)
"চাঁদে যেতে কত সময় লাগে?"
```

## FAQ Dataset

The bot currently has **25 FAQ entries** across **5 categories**:

- **শিক্ষা (Education)** - 5 questions
- **স্বাস্থ্য (Health)** - 5 questions
- **ভ্রমণ (Travel)** - 5 questions
- **প্রযুক্তি (Technology)** - 5 questions
- **খেলাধুলা (Sports)** - 5 questions

Each entry includes:
- Question in Bengali
- Answer in Bengali
- Category metadata
- Difficulty level (easy, medium, hard)

## How It Works

1. **Question Submission** - User sends a Bengali question via `/api/ask`
2. **Category Detection** - LLM classifies the question into a topic
3. **Difficulty Assessment** - LLM determines the question complexity
4. **Vector Search** - FAISS finds relevant FAQ entries using semantic similarity
5. **Answer Generation** - LLM generates a contextual answer using retrieved documents
6. **Response** - Returns answer with metadata (category, difficulty)

## Performance Notes

- **CPU-Optimized** - Runs efficiently on systems without GPU
- **First Request** - May take 2-3 seconds (model loading)
- **Subsequent Requests** - Typically < 1 second
- **Offline Mode** - Embedding model works offline after initial download
- **LLM Calls** - Requires internet connection for GitHub AI models

## Troubleshooting

### Import Errors

If you get import errors, ensure all dependencies are installed:
```bash
pip install -r requirements.txt --upgrade
```

### Vector Store Not Initialized

Check the logs during startup. The embedding model download may take time on first run.

### API Key Issues

- Verify your `GITHUB_TOKEN` in `.env` is correct
- Ensure the token has appropriate permissions
- Check if the GitHub Models API is accessible

### Port Already in Use

If port 8000 is busy, specify a different port:
```bash
uvicorn app.main:app --reload --port 8080
```

## Extending the Bot

### Adding More FAQs

Edit `app/config.py` and add entries to the `FAQ_DATA` list:

```python
FAQ_DATA = [
    # ... existing entries ...
    ("আপনার প্রশ্ন?", "আপনার উত্তর।", {"category": "education", "difficulty": "easy"}),
]
```

### Adding New Categories

1. Add to `FAQ_DATA` with new category
2. Update `CATEGORY_MAP` in `app/config.py`
3. Update category detection prompt in `app/services/rag_service.py`

## License

This project is created for educational purposes.

## Support

For issues or questions, please check:
- API Documentation: `http://localhost:8000/docs`
- Logs: Check terminal output for detailed error messages
