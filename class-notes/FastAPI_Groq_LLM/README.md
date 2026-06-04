# FastAPI + Groq — Your First GenAI API Endpoint

> Today is special. Until now, your APIs only served **your own data**.
> Today, your API starts **talking to an LLM**. This is the moment everything you've learned starts paying off.

> 📍 **Week 4 · Class 2** — The Milestone Class ⭐

> **What you should already know:**
> - FastAPI Basics (POST endpoints, `/docs`)
> - Pydantic Basics + Part 2 (`BaseModel`, validation, `response_model`)
> - SQLModel Basics (`Session`, CRUD via /docs — optional today, used in bonus section)
> - AI Foundations 1 & 2 (LLMs, tokenization, context window, temperature)

---

## Table of Contents

1. [The big jump — from CRUD to GenAI](#1-the-big-jump)
2. [What is Groq?](#2-what-is-groq)
3. [Step 1 — Get a free Groq API key](#3-step-1--get-a-free-groq-api-key)
4. [Step 2 — Install the libraries](#4-step-2--install)
5. [Step 3 — Set up the `.env` file](#5-step-3--set-up-the-env-file)
6. [Step 4 — First Groq call (plain Python)](#6-step-4--first-groq-call)
7. [Step 5 — Wrap it in a FastAPI endpoint](#7-step-5--wrap-it-in-a-fastapi-endpoint)
8. [Test in `/docs` 🎉](#8-test-in-docs)
9. [Step 6 — Add chat history (in-memory)](#9-step-6--add-chat-history-in-memory)
10. [Step 7 — Bonus: save chats to the database](#10-step-7--bonus-save-chats-to-the-database)
11. [Common mistakes](#11-common-mistakes)
12. [Practice exercises](#12-practice-exercises)
13. [Quick cheat sheet](#13-quick-cheat-sheet)
14. [What's next? — LangChain](#14-whats-next--langchain)

---

## 1. The Big Jump

So far you've built APIs like:

```
POST /students   → save a student in the database
GET /students    → return students from the database
```

The data **came from you**. Your API just stored and served it.

**Today:** the data comes from an **LLM**.

```
POST /ask        → your API → Groq's Llama 3 → answer comes back → return to user
```

You're no longer building a database app — you're building a **GenAI app**. 🚀

---

## 2. What is Groq?

> **Groq** (not Grok 🤡) is a company that runs LLMs at **blazing speed** — about 10x faster than OpenAI in most cases.
>
> Most importantly: **they have a generous free tier**.

| Detail | Value |
|--------|-------|
| Cost | **Free** (with daily rate limits) |
| Models offered | Llama 3.3 70B, Mixtral 8x7B, Gemma, more |
| Speed | Extremely fast (~500 tokens/sec) |
| API style | OpenAI-compatible (easy to switch later) |
| Signup | Just a Google account |

We'll use Groq throughout the rest of the course.

---

## 3. Step 1 — Get a Free Groq API Key

1. Go to **https://console.groq.com/**
2. Click **"Log In"** → sign in with Google
3. Click **"API Keys"** in the left sidebar
4. Click **"Create API Key"**, give it a name like `my-first-genai-app`
5. **Copy the key** — it looks like `gsk_abc123...` (long string)

⚠️ **Important:** You can only see the key **once**. If you lose it, just create a new one.

🛡️ **Never share this key publicly.** Don't commit it to GitHub. We'll use `.env` files to keep it safe.

---

## 4. Step 2 — Install

In your project folder:

```bash
pip install groq python-dotenv fastapi uvicorn
```

| Package | What it's for |
|---------|---------------|
| `groq` | The official Groq Python SDK |
| `python-dotenv` | Loads secrets from a `.env` file |
| `fastapi`, `uvicorn` | You already know these |

---

## 5. Step 3 — Set Up the `.env` File

Create a new file called `.env` (yes, just `.env` — no name before the dot) in your project root:

```
GROQ_API_KEY=gsk_paste_your_real_key_here
```

### Why `.env`?

| Without `.env` | With `.env` |
|----------------|-------------|
| API key hardcoded in your code | API key kept separately |
| Easy to accidentally push to GitHub | `.env` is ignored from Git |
| Anyone reading your code sees your key | Code is safe to share |

### Add to `.gitignore`

If you use git, create or edit `.gitignore`:

```
.env
__pycache__/
*.db
```

This ensures `.env` never goes to GitHub.

---

## 6. Step 4 — First Groq Call (Plain Python)

Before wrapping it in FastAPI, let's confirm Groq works. Create a file `test_groq.py`:

```python
from dotenv import load_dotenv
from groq import Groq
import os

# Load .env into environment
load_dotenv()

# Create a Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Make a chat completion call
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Tell me a 1-line joke about cats."}
    ],
)

print(response.choices[0].message.content)
```

Run it:

```bash
python test_groq.py
```

You should see something like:

```
Why don't cats play poker in the jungle? Too many cheetahs!
```

🎉 **You just made an LLM call from Python!**

### Walking through the code:

| Line | What it does |
|------|--------------|
| `load_dotenv()` | Reads your `.env` file into environment variables |
| `os.getenv("GROQ_API_KEY")` | Grabs the key safely |
| `Groq(api_key=...)` | Creates a client connection to Groq |
| `client.chat.completions.create(...)` | Actually sends the request |
| `messages=[...]` | The conversation. `role` = `"user"` or `"assistant"` or `"system"` |
| `response.choices[0].message.content` | The text the LLM gave back |

---

## 7. Step 5 — Wrap It in a FastAPI Endpoint

Now the magic. Create `main.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os

# Setup
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = FastAPI()

# Input schema (Pydantic — you know this!)
class Question(BaseModel):
    text: str

# Output schema
class Answer(BaseModel):
    question: str
    answer: str

# The endpoint!
@app.post("/ask", response_model=Answer)
def ask_llm(question: Question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": question.text}
        ],
    )
    answer_text = response.choices[0].message.content
    return Answer(question=question.text, answer=answer_text)
```

Run it:

```bash
uvicorn main:app --reload
```

That's it. **20 lines of code = a working GenAI API.** ⚡

---

## 8. Test in `/docs`

Open `http://localhost:8000/docs` — your familiar Swagger UI.

1. Find **POST `/ask`** — click to expand
2. Click **"Try it out"**
3. Enter this JSON body:

```json
{
  "text": "What is FastAPI in one sentence?"
}
```

4. Click **"Execute"**

### Response (200 OK):

```json
{
  "question": "What is FastAPI in one sentence?",
  "answer": "FastAPI is a modern, fast Python web framework for building APIs with automatic documentation and type-based validation."
}
```

🎉 **You just built a GenAI API endpoint.**

### Try more questions:

```json
{"text": "Tell me a joke about programmers."}
```

```json
{"text": "Explain context window in 2 sentences."}
```

```json
{"text": "Suggest 3 names for a coffee shop."}
```

Every question goes to Groq's Llama 3.3 70B model and comes back as a clean JSON response. Pydantic validates everything. `/docs` is auto-generated. **Magic.**

---

## 9. Step 6 — Add Chat History (In-Memory)

The `/ask` endpoint has **no memory**. Each call starts fresh. Let's build a `/chat` endpoint that remembers the conversation.

Add this to `main.py`:

```python
# In-memory chat history (resets when server restarts)
chat_history = []

@app.post("/chat", response_model=Answer)
def chat(question: Question):
    # Add this question to history
    chat_history.append({"role": "user", "content": question.text})

    # Send the WHOLE history to the LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=chat_history,
    )

    answer_text = response.choices[0].message.content

    # Save the LLM's answer in history too
    chat_history.append({"role": "assistant", "content": answer_text})

    return Answer(question=question.text, answer=answer_text)

@app.get("/chat/history")
def get_history():
    return chat_history

@app.delete("/chat/history")
def clear_history():
    chat_history.clear()
    return {"message": "History cleared"}
```

### Test in `/docs`:

**First call:**
```json
{"text": "My favorite color is blue."}
```

→ LLM: *"That's a calming color! Why do you like it?"*

**Second call (no need to repeat info!):**
```json
{"text": "What did I just tell you my favorite color was?"}
```

→ LLM: *"You told me your favorite color is blue."* 🧠

**The LLM remembers** because we send the whole history every time.

### What just happened?

This is the **context window** concept from Class 2 in action!
- Each request includes the entire conversation
- The LLM "sees" all previous messages
- That's why it can refer back

> ⚠️ Watch out: the history grows over time. Eventually it exceeds the context window. **Memory management** is a real problem — LangChain solves it elegantly in later classes.

---

## 10. Step 7 — Bonus: Save Chats to the Database

This is **optional** but powerful. Combine today's class with SQLModel.

### Add to `main.py`:

```python
from sqlmodel import SQLModel, Field, Session, create_engine, select
from datetime import datetime

class ChatLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    question: str
    answer: str
    created_at: datetime = Field(default_factory=datetime.now)

engine = create_engine("sqlite:///chats.db")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/ask-and-save", response_model=Answer)
def ask_and_save(question: Question):
    # Call the LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": question.text}],
    )
    answer_text = response.choices[0].message.content

    # Save to the database
    with Session(engine) as session:
        log = ChatLog(question=question.text, answer=answer_text)
        session.add(log)
        session.commit()

    return Answer(question=question.text, answer=answer_text)

@app.get("/chats")
def list_chats():
    with Session(engine) as session:
        return session.exec(select(ChatLog)).all()
```

Now every question + answer is stored. Restart the server — your history is **still there**. 🎉

This is the moment Pydantic + FastAPI + SQLModel + GenAI **all come together**.

---

## 11. Common Mistakes

### ❌ Mistake 1: API key not loaded

```python
client = Groq(api_key=os.getenv("GROQ_API_KEY"))    # ❌ returns None if .env not loaded
```

✅ **Correct:**

```python
load_dotenv()                                        # ✅ load first
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
```

---

### ❌ Mistake 2: Wrong model name

Groq updates model names periodically. If you see `"model_not_found"`, check the latest list:

👉 https://console.groq.com/docs/models

As of now (2026), use: `llama-3.3-70b-versatile`

---

### ❌ Mistake 3: Committing `.env` to GitHub

If you accidentally push `.env`, your key is **public**. Anyone can use it. Revoke it immediately from Groq console.

✅ **Always** add `.env` to `.gitignore` **before** your first commit.

---

### ❌ Mistake 4: Hitting the free-tier rate limit

Groq's free tier has per-minute and per-day limits. If you spam requests, you'll see:
```
groq.RateLimitError: Rate limit exceeded
```

Just wait a minute and try again. For class projects, the free tier is more than enough.

---

### ❌ Mistake 5: Forgetting Pydantic input model

```python
@app.post("/ask")
def ask_llm(text: str):     # ❌ doesn't work as a POST body
```

✅ **Correct:**

```python
class Question(BaseModel):
    text: str

@app.post("/ask")
def ask_llm(question: Question):
```

---

### ❌ Mistake 6: Trusting the LLM blindly (hallucinations!)

Remember Class 2 — LLMs hallucinate. If your app gives **factual** answers (medical, legal, business), don't just return the LLM's response. **Ground it** with RAG (coming in Phase 3).

---

## 12. Practice Exercises

All exercises should be tested in `/docs`. 🎯

### Exercise 1 — Translator endpoint
Build POST `/translate` that takes `text` and `target_language` and returns the translation.

Hint: use a system message like:
```python
{"role": "system", "content": f"Translate the user's text to {target_language}."}
```

### Exercise 2 — Summarizer
Build POST `/summarize` that takes long text and returns a 2-sentence summary.

### Exercise 3 — Temperature playground
Add a `temperature` field to the `Question` model. Default to `0.7`. Test with `0.0` vs `1.5` — see the difference.

### Exercise 4 — System prompt
Add a `system_prompt` to `/ask` so the user can give the LLM a "personality":
```json
{
  "text": "Tell me about cats.",
  "system_prompt": "You are a 5-year-old child."
}
```

### Exercise 5 — Code reviewer
Build POST `/review-code` that takes Python code and returns suggestions.

### Exercise 6 — Token counter
Use `tiktoken` (from Class 2) to count tokens in the question and add `tokens_used` to the response.

### Exercise 7 — Save to DB
Combine Exercise 1 (translator) with section 10 — save every translation to a `translations` table.

### Exercise 8 — Persistence test
Make 5 calls to `/ask-and-save`. Stop the server. Restart. Call `/chats`. All 5 should still be there.

---

## 13. Quick Cheat Sheet

```python
# ---- imports ----
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from groq import Groq
import os

# ---- setup ----
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = FastAPI()

# ---- schemas ----
class Question(BaseModel):
    text: str

class Answer(BaseModel):
    question: str
    answer: str

# ---- endpoint ----
@app.post("/ask", response_model=Answer)
def ask_llm(question: Question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": question.text}],
        temperature=0.7,    # optional
    )
    return Answer(
        question=question.text,
        answer=response.choices[0].message.content,
    )
```

### Message roles:

| Role | Meaning |
|------|---------|
| `"system"` | Set the LLM's behavior / personality |
| `"user"` | The user's message |
| `"assistant"` | The LLM's previous reply (used for history) |

### Free Groq models (as of 2026):

| Model name | Best for |
|------------|----------|
| `llama-3.3-70b-versatile` | General chat — recommended default |
| `llama-3.1-8b-instant` | Fastest, lower quality |
| `mixtral-8x7b-32768` | Long context (32k tokens) |
| `gemma2-9b-it` | Lightweight alternative |

> 🔄 Models change — always check https://console.groq.com/docs/models for the latest list.

---

## 🎯 Summary — What You Built Today

✅ Got a free Groq API key
✅ Set up `.env` for safe key storage
✅ Made your first LLM call from Python
✅ Wrapped it in a FastAPI POST endpoint
✅ Tested it in `/docs` (just like every API class)
✅ Added chat history with multi-turn memory
✅ (Bonus) Saved chat history to a SQLModel database
✅ Connected everything you've learned: Pydantic + FastAPI + SQLModel + LLMs

**This is a real, working GenAI application.** 🎉

---

## 14. What's Next? — LangChain

You can now call an LLM and wrap it in an API. But:

- ❓ How do you handle **complex prompts** without messy string formatting?
- ❓ How do you give an LLM **tools** (like a search engine, a calculator)?
- ❓ How do you build **agents** that can decide what to do?
- ❓ How do you chain multiple LLM calls together?

**LangChain** solves all of these.

### Coming up in Phase 2:

| Class | Topic |
|-------|-------|
| Week 6 | LangChain intro: ChatModels, PromptTemplates |
| Week 6 | LCEL — the pipe operator (`prompt | llm | parser`) |
| Week 7 | Output parsers — structured JSON outputs |
| Week 7 | Memory — proper conversation history |
| Week 8 | Tools — let the LLM call functions |
| Week 9 | Agents — autonomous LLM reasoning |
| Week 11-12 | **Mini Project: AI Chatbot** with memory + tools |

---

**Remember:**

```python
# This is the entire core of a GenAI API:
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": user_question}],
)
print(response.choices[0].message.content)
```

Three lines. One LLM. Infinite possibilities.

Wrap it in FastAPI → you have a GenAI app.
Wrap it in LangChain → you have a *powerful* GenAI app.
Add RAG → you have a *trustworthy* GenAI app.

**You are now officially a GenAI engineer.** 🚀

**Happy Coding!**
