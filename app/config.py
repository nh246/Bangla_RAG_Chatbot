"""
Configuration module for the FastAPI application.
Manages environment variables and application settings.
"""
import os
from typing import List, Tuple, Dict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    github_token: str = os.getenv("GITHUB_TOKEN", "")
    model_name: str = os.getenv("MODEL_NAME", "openai/gpt-4o-mini")
    base_url: str = os.getenv("BASE_URL", "https://models.github.ai/inference")
    
    # Embedding Model
    embedding_model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # API Settings
    api_title: str = "Bengali RAG FAQ Bot API"
    api_version: str = "1.0.0"
    api_description: str = "FastAPI backend for Bengali FAQ bot using RAG technology"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


# FAQ Data Structure
# Structure: (Question, Answer, Metadata Dictionary)
FAQ_DATA: List[Tuple[str, str, Dict[str, str]]] = [
    # শিক্ষা (Education)
    ("বাংলাদেশে প্রাথমিক শিক্ষা কত বছরের?", "বাংলাদেশে প্রাথমিক শিক্ষা ৫ বছরের।", {"category": "education", "difficulty": "easy"}),
    ("উচ্চশিক্ষার জন্য কী প্রয়োজন?", "উচ্চশিক্ষার জন্য এসএসসি এবং এইচএসসি পাস করতে হয়।", {"category": "education", "difficulty": "medium"}),
    ("অনলাইন শিক্ষা কীভাবে কার্যকর করা যায়?", "অনলাইন শিক্ষা ডিজিটাল টুলস এবং ইন্টারেক্টিভ কন্টেন্ট দিয়ে কার্যকর করা যায়।", {"category": "education", "difficulty": "hard"}),
    ("প্রাথমিক বিদ্যালয়ে ভর্তির বয়স কত?", "প্রাথমিক বিদ্যালয়ে ভর্তির বয়স সাধারণত ৬ বছর।", {"category": "education", "difficulty": "easy"}),
    ("শিক্ষায় প্রযুক্তির ভূমিকা কী?", "শিক্ষায় প্রযুক্তির ব্যবহার শিক্ষার্থীদের আগ্রহ এবং শেখার মান বাড়াতে সাহায্য করে।", {"category": "education", "difficulty": "medium"}),

    # স্বাস্থ্য (Health)
    ("সুস্থ থাকার মূল উপায় কী?", "সুস্থ থাকতে প্রতিদিন ব্যায়াম এবং সুষম খাবার খান।", {"category": "health", "difficulty": "easy"}),
    ("ডায়াবেটিস নিয়ন্ত্রণের উপায় কী?", "ডায়াবেটিস নিয়ন্ত্রণে ওজন এবং খাদ্যাভ্যাস নিয়ন্ত্রণ করা জরুরি।", {"category": "health", "difficulty": "medium"}),
    ("মানসিক স্বাস্থ্যের জন্য কী করা উচিত?", "মানসিক স্বাস্থ্যের জন্য মেডিটেশন, পর্যাপ্ত ঘুম এবং যোগ ব্যায়াম করুন।", {"category": "health", "difficulty": "hard"}),
    ("দৈনিক কতটুকু পানি পান করা উচিত?", "প্রতিদিন কমপক্ষে ৮ গ্লাস পানি পান করা উচিত।", {"category": "health", "difficulty": "easy"}),
    ("কোন অভ্যাস স্বাস্থ্যের জন্য ক্ষতিকর?", "ধূমপান এবং মদ্যপান স্বাস্থ্যের জন্য অত্যন্ত ক্ষতিকর।", {"category": "health", "difficulty": "easy"}),

    # ভ্রমণ (Travel)
    ("বাংলাদেশের দীর্ঘতম সমুদ্র সৈকত কোনটি?", "কক্সবাজার বিশ্বের দীর্ঘতম সমুদ্র সৈকত।", {"category": "travel", "difficulty": "easy"}),
    ("বিদেশ ভ্রমণের জন্য কী কী কাগজপত্র প্রয়োজন?", "বিদেশ ভ্রমণের জন্য পাসপোর্ট এবং ভিসা প্রয়োজন।", {"category": "travel", "difficulty": "medium"}),
    ("পরিবেশবান্ধব ভ্রমণ কী?", "পরিবেশবান্ধব ভ্রমণে প্লাস্টিক ব্যবহার কমানো এবং প্রকৃতির প্রতি যত্ন নেওয়া হয়।", {"category": "travel", "difficulty": "hard"}),
    ("সুন্দরবন কেন বিখ্যাত?", "সুন্দরবন রয়েল বেঙ্গল টাইগার বাঘের জন্য বিখ্যাত।", {"category": "travel", "difficulty": "easy"}),
    ("ভ্রমণের সময় কী মেনে চলা উচিত?", "ভ্রমণের সময় স্থানীয় সংস্কৃতি এবং ঐতিহ্যকে সম্মান করুন।", {"category": "travel", "difficulty": "medium"}),

    # প্রযুক্তি (Technology)
    ("কৃত্রিম বুদ্ধিমত্তা বা এআই কী?", "এআই হলো কৃত্রিম বুদ্ধিমত্তা যা মানুষের মতো চিন্তা করতে ও কাজ করতে পারে।", {"category": "technology", "difficulty": "easy"}),
    ("ইন্টারনেট গতি বাড়ানোর উপায় কী?", "ইন্টারনেট গতি বাড়াতে ভালো রাউটার ব্যবহার করুন এবং অপ্রয়োজনীয় ডিভাইস কানেক্ট করা এড়িয়ে চলুন।", {"category": "technology", "difficulty": "medium"}),
    ("ব্লকচেইন প্রযুক্তির সুবিধা কী?", "ব্লকচেইন প্রযুক্তি ডেটা সুরক্ষিত ও বিকেন্দ্রীভূত করে এবং স্বচ্ছতা বাড়ায়।", {"category": "technology", "difficulty": "hard"}),
    ("স্মার্টফোনের সুবিধা কী?", "স্মার্টফোন দিয়ে অনলাইন পেমেন্ট, যোগাযোগ এবং বিভিন্ন কাজ সহজে করা যায়।", {"category": "technology", "difficulty": "easy"}),
    ("ক্লাউড স্টোরেজ কী?", "ক্লাউড স্টোরেজে আপনার ডেটা ইন্টারনেটের মাধ্যমে সুরক্ষিতভাবে ব্যাকআপ থাকে।", {"category": "technology", "difficulty": "medium"}),

    # খেলাধুলা (Sports)
    ("বাংলাদেশের সবচেয়ে জনপ্রিয় খেলা কোনটি?", "ক্রিকেট বাংলাদেশের সবচেয়ে জনপ্রিয় খেলা।", {"category": "sports", "difficulty": "easy"}),
    ("ফুটবল খেলায় কতজন খেলোয়াড় থাকে?", "ফুটবল খেলায় প্রতি দলে ১১ জন খেলোয়াড় থাকে।", {"category": "sports", "difficulty": "medium"}),
    ("আধুনিক অলিম্পিক কখন শুরু হয়?", "আধুনিক অলিম্পিক ১৮৯৬ সালে শুরু হয়।", {"category": "sports", "difficulty": "hard"}),
    ("বাংলাদেশের জাতীয় খেলার নাম কী?", "কাবাডি বাংলাদেশের জাতীয় খেলা।", {"category": "sports", "difficulty": "easy"}),
    ("নিয়মিত খেলাধুলার উপকারিতা কী?", "নিয়মিত খেলাধুলা শারীরিক ও মানসিক স্বাস্থ্য ভালো রাখে এবং ফিটনেস বাড়ায়।", {"category": "sports", "difficulty": "easy"}),
]


# Category Mapping (English to Bengali)
CATEGORY_MAP = {
    "education": "শিক্ষা",
    "health": "স্বাস্থ্য",
    "travel": "ভ্রমণ",
    "technology": "প্রযুক্তি",
    "sports": "খেলাধুলা",
    "general": "সাধারণ"
}
