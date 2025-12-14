"""
RAG service for question answering.
Contains logic for category detection, difficulty detection, and document retrieval.
"""
from typing import List, Tuple
import logging
import time
from openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.config import settings, CATEGORY_MAP
from app.services.vector_store import vector_store_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(
    base_url=settings.base_url,
    api_key=settings.github_token
)


def detect_category(question: str) -> str:
    """
    Uses LLM to classify the question into one of the predefined topics.
    
    Args:
        question: The question to classify
        
    Returns:
        Category name in English (education, health, travel, technology, sports)
    """
    categories = "education, health, travel, technology, sports"
    system_prompt = (
        f"প্রশ্নটি পড়ে শুধুমাত্র একটা ক্যাটাগরি বলো (lowercase, English): {categories}। "
        "এর বাইরে কোনো শব্দ ব্যবহার করবে না। যদি উত্তর দিতে না পারো, তবে 'travel' বলো।"
    )
    
    try:
        response = client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0,
            max_tokens=10
        )
        cat = response.choices[0].message.content.strip().lower()
        
        # Validate category
        if cat in categories.split(', '):
            return cat
        
    except Exception as e:
        logger.error(f"Error in category detection: {e}")
        time.sleep(1)
    
    # Default fallback category
    return "travel"


def detect_difficulty(question: str) -> str:
    """
    Uses LLM to estimate the difficulty of the question.
    
    Args:
        question: The question to analyze
        
    Returns:
        Difficulty level: easy, medium, or hard
    """
    try:
        response = client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {
                    "role": "system",
                    "content": "প্রশ্নের কঠিনতা বলো: easy, medium, অথবা hard। শুধু একটা শব্দ (English lowercase)।"
                },
                {"role": "user", "content": question}
            ],
            temperature=0,
            max_tokens=10
        )
        diff = response.choices[0].message.content.strip().lower()
        return diff if diff in ["easy", "medium", "hard"] else "medium"
    except Exception as e:
        logger.error(f"Error in difficulty detection: {e}")
        return "medium"


def retrieve_relevant_docs(
    question: str,
    category: str,
    difficulty: str,
    k: int = 3
) -> List[Document]:
    """
    Retrieves relevant documents using filtered vector search.
    
    Args:
        question: The question to search for
        category: Category to filter by
        difficulty: Difficulty level to filter by
        k: Number of documents to retrieve
        
    Returns:
        List of relevant documents
    """
    documents = vector_store_manager.documents
    embedding_model = vector_store_manager.embedding_model
    
    if not documents or not embedding_model:
        logger.error("Vector store not initialized")
        return []
    
    # Step 1: Filter by Category AND Difficulty
    filtered_docs = [
        doc for doc in documents
        if doc.metadata["category"] == category and doc.metadata["difficulty"] == difficulty
    ]
    
    # Step 2: Fallback to Category ONLY (if Category+Difficulty filter fails)
    if not filtered_docs:
        logger.info(f"No docs found for category={category} + difficulty={difficulty}, trying category only")
        filtered_docs = [
            doc for doc in documents
            if doc.metadata["category"] == category
        ]
    
    if not filtered_docs:
        logger.warning(f"No documents found for category={category}")
        return []
    
    # Step 3: Perform Similarity Search on the filtered subset
    temp_store = FAISS.from_documents(filtered_docs, embedding_model)
    similar_docs = temp_store.similarity_search(question, k=k)
    
    # Fallback: return from main store if similarity search yields nothing
    if not similar_docs and filtered_docs:
        vector_store = vector_store_manager.vector_store
        if vector_store:
            return vector_store.similarity_search(question, k=1)
    
    return similar_docs


def ask_faq_bot(question: str) -> Tuple[str, str, str]:
    """
    Main RAG function to answer FAQ questions.
    
    Args:
        question: The question to answer
        
    Returns:
        Tuple of (answer, category_english, difficulty)
    """
    logger.info(f"Processing question: {question}")
    
    # AI Routing: Detect category and difficulty
    category_eng = detect_category(question)
    difficulty = detect_difficulty(question)
    category_bangla = CATEGORY_MAP.get(category_eng, "সাধারণ")
    
    logger.info(f"Detected - Topic: {category_bangla} ({category_eng}), Difficulty: {difficulty}")
    
    # Retrieval
    docs = retrieve_relevant_docs(question, category_eng, difficulty, k=3)
    
    if not docs:
        fallback_msg = "দুঃখিত, এই প্রশ্নের উত্তর আমার ডেটাসেটে (FAQ) পাওয়া যায়নি।"
        logger.warning("No relevant documents found")
        return fallback_msg, category_eng, difficulty
    
    # Generation with LLM
    context = "\n".join([doc.page_content for doc in docs])
    
    prompt = f"""তুমি একজন সহায়ক বাংলা FAQ বট।
নিচে দেওয়া তথ্যগুলো ব্যবহার করে ব্যবহারকারীর প্রশ্নটির একটি স্পষ্ট এবং সংক্ষিপ্ত উত্তর দাও।
যদি তথ্যগুলোর মধ্যে প্রশ্নটির সঠিক উত্তর **সরাসরি** না থাকে, তাহলে **অবশ্যই শুধুমাত্র এই বাক্যাংশটি ব্যবহার করো: 'দুঃখিত, এই প্রশ্নের উত্তর আমার ডেটাসেটে নেই।'**

তথ্য:
{context}

প্রশ্ন: {question}
উত্তর:"""
    
    try:
        response = client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": "You are a helpful Bengali FAQ assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=200
        )
        answer = response.choices[0].message.content.strip()
        logger.info(f"Generated answer: {answer}")
        return answer, category_eng, difficulty
        
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        fallback_msg = "দুঃখিত, বর্তমানে সার্ভার সমস্যার কারণে উত্তর দেওয়া সম্ভব হচ্ছে না।"
        return fallback_msg, category_eng, difficulty
