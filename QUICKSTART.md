# 🚀 How to Run the Bengali FAQ Chatbot

Complete guide to run both backend and frontend.

## 📋 Prerequisites

- Python 3.8+
- Modern web browser (Chrome, Firefox, Edge)
- Terminal/Command Prompt

---

## 🎯 Quick Start (3 Steps)

### **Step 1: Start the Backend Server**

Open a terminal and run:

```bash
cd "E:\OStad Ai Engeneering\Module 17\assignment\project"

# If not installed yet, install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload
```

**Wait for this message:**
```
INFO:     Vector store initialized successfully!
INFO:     Application startup complete!
```

✅ **Backend is ready at:** http://localhost:8000

---

### **Step 2: Open the Chatbot Frontend**

Simply **double-click** on:
```
E:\OStad Ai Engeneering\Module 17\assignment\project\index.html
```

Or open it in your browser by dragging the file into the browser window.

✅ **Chatbot interface will open!**

---

### **Step 3: Start Chatting!**

Try these sample questions by clicking on them or typing:

- **শিক্ষা:** "প্রাথমিক শিক্ষা কত বছরের হয়?"
- **স্বাস্থ্য:** "দৈনিক কতটুকু পানি পান করা উচিত?"
- **ভ্রমণ:** "সুন্দরবন কেন বিখ্যাত?"
- **প্রযুক্তি:** "এআই (AI) বলতে কী বোঝো?"
- **খেলাধুলা:** "বাংলাদেশের সবচেয়ে জনপ্রিয় খেলা কোনটি?"

---

## 🎨 Chatbot Features

✨ **Beautiful UI**
- Modern gradient design
- Smooth animations
- Responsive layout (works on mobile!)
- Typing indicators
- Message bubbles with metadata

📂 **Category Quick Access**
- Click on category pills (শিক্ষা, স্বাস্থ্য, etc.) for instant sample questions

🔍 **Smart Responses**
- Shows category and difficulty level for each answer
- Displays connection status
- Error handling with user-friendly messages

---

## 🛠️ Troubleshooting

### "সংযোগ বিচ্ছিন্ন - সার্ভার চালু করুন"

**Problem:** Backend server is not running

**Solution:** 
1. Open a terminal
2. Navigate to project folder
3. Run: `uvicorn app.main:app --reload`
4. Refresh the browser

---

### CORS Error in Browser Console

**Problem:** Cross-origin request blocked

**Solution:** Backend already has CORS enabled. Make sure:
1. Backend is running on port 8000
2. You're opening index.html in a browser (not from file:// URL for production)

**Alternative:** Use a simple local server:
```bash
# Using Python's built-in server
python -m http.server 8080

# Then open: http://localhost:8080
```

---

## 📱 Mobile/Tablet View

The chatbot is fully responsive! Open `index.html` on your phone/tablet browser to test the mobile view.

---

## 🎥 Demo Workflow

1. **Backend starts** → Loads AI model and vector store
2. **User opens chatbot** → Sees welcome screen with sample questions
3. **User clicks category** → Auto-fills a sample question
4. **User sends question** → Shows typing indicator
5. **Bot responds** → Displays answer with category badge and difficulty

---

## 📊 What Happens Behind the Scenes

```
User Question
    ↓
Frontend (index.html)
    ↓
POST request to /api/ask
    ↓
Backend (FastAPI)
    ↓
1. Detect Category (LLM)
2. Detect Difficulty (LLM)
3. Vector Search (FAISS)
4. Generate Answer (LLM)
    ↓
JSON Response
    ↓
Frontend displays answer with metadata
```

---

## 🎯 Testing Checklist

- [ ] Backend server starts successfully
- [ ] Open index.html in browser
- [ ] Status shows "সক্রিয় এবং সাহায্যের জন্য প্রস্তুত"
- [ ] Click on a category pill - sends sample question
- [ ] Type a custom question and send
- [ ] Verify answer appears with category badge
- [ ] Check typing indicator shows while waiting
- [ ] Try all 5 categories

---

## 🔗 Useful Links

- **Chatbot UI:** Open `index.html` in browser
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/api/health
- **Categories List:** http://localhost:8000/api/categories

---

## 💡 Pro Tips

1. **Keep the backend terminal open** to see real-time logs
2. **Use category pills** for quick testing
3. **Try out-of-scope questions** to test fallback behavior
4. **Press Enter** to send messages (Shift+Enter for new line)
5. **Check browser console** (F12) for debugging if needed

---

## 🎉 You're All Set!

Your Bengali FAQ chatbot is ready to use! Enjoy testing the AI-powered question answering system! 🚀
