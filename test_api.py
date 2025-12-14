"""
Test script for Bengali RAG FAQ Bot API
Run this after starting the server with: uvicorn app.main:app --reload
"""
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

print("=" * 60)
print("🤖 Bengali RAG FAQ Bot - API Test Suite")
print("=" * 60)
print()

# Test 1: Health Check
print("📍 Test 1: Health Check")
print("-" * 60)
try:
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("✅ Health check passed!\n")
except Exception as e:
    print(f"❌ Error: {e}")
    print("Make sure the server is running: uvicorn app.main:app --reload\n")
    exit(1)

# Test 2: List Categories
print("📍 Test 2: List Categories")
print("-" * 60)
response = requests.get(f"{BASE_URL}/api/categories")
print(json.dumps(response.json(), indent=2, ensure_ascii=False))
print()

# Test 3: Ask Questions
test_questions = [
    ("প্রাথমিক শিক্ষা কত বছরের হয়?", "Education"),
    ("সুস্থ থাকার মূল উপায় কী?", "Health"),
    ("কক্সবাজারের বিশেষত্ব কী?", "Travel"),
    ("এআই (AI) বলতে কী বোঝো?", "Technology"),
    ("বাংলাদেশের সবচেয়ে জনপ্রিয় খেলা কোনটি?", "Sports"),
    ("চাঁদে যেতে কত সময় লাগে?", "Out of scope - should return fallback"),
]

for i, (question, expected_category) in enumerate(test_questions, 3):
    print(f"📍 Test {i}: {expected_category}")
    print("-" * 60)
    print(f"প্রশ্ন: {question}")
    
    response = requests.post(
        f"{BASE_URL}/api/ask",
        json={"question": question}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"উত্তর: {result['answer']}")
        print(f"বিভাগ: {result['category_bangla']} ({result['category']})")
        print(f"কঠিনতা: {result['difficulty']}")
        print("✅ Question answered successfully!")
    else:
        print(f"❌ Error: Status {response.status_code}")
        print(response.text)
    
    print()

print("=" * 60)
print("🎉 All tests completed!")
print("=" * 60)
print()
print("💡 Next steps:")
print("1. Open http://localhost:8000/docs for interactive API testing")
print("2. Try your own questions!")
print("3. Check server logs for detailed processing information")
