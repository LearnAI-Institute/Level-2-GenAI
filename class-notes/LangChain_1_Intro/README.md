# LangChain — Class 1: Why LangChain + ChatModels + PromptTemplates

> The next big step. You've already called an LLM with the raw `groq` library.
> Today you'll meet **LangChain** — a library that makes LLM work **clean, reusable, and powerful**.

> 📍 **Week 6 · Class 1** of the Level Two GenAI Course — start of **Phase 2 (LangChain)**

> **What you should already know:**
> - FastAPI + Groq class (raw LLM calls)
> - Pydantic models, `/docs` testing
> - AI Foundations 1 & 2 (LLMs, tokenization, hallucinations)

---

## Table of Contents

1. [Recap — where you are now](#1-recap)
2. [The pain — what's wrong with raw LLM calls](#2-the-pain)
3. [What is LangChain?](#3-what-is-langchain)
4. [Installation](#4-installation)
5. [Your first ChatModel — `ChatGroq`](#5-your-first-chatmodel)
6. [PromptTemplate — static prompts](#6-prompttemplate--static-prompts)
7. [PromptTemplate — dynamic prompts (with variables)](#7-prompttemplate--dynamic-prompts)
8. [ChatPromptTemplate — for system + user messages](#8-chatprompttemplate)
9. [Before vs After — raw Groq vs LangChain](#9-before-vs-after)
10. [Use it in FastAPI — test in `/docs`](#10-use-it-in-fastapi)
11. [Common mistakes](#11-common-mistakes)
12. [Practice exercises](#12-practice-exercises)
13. [Quick cheat sheet](#13-quick-cheat-sheet)
14. [What's next? — LCEL + Chains](#14-whats-next)

---

## 1. Recap

In the previous class you built this:

```python
from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Tell me a joke."}],
)
print(response.choices[0].message.content)
```

It works. You wrapped it in FastAPI. Tested in `/docs`. Built `/ask`, `/chat`, even saved to DB.

**So why do we need anything else?** Let's see. 👇

---

## 2. The Pain

**Story:** Ahmed builds 5 endpoints — translator, summarizer, joke-teller, code reviewer, email writer. Each one looks like this:

```python
# Translator
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "Translate the user's text to French."},
        {"role": "user", "content": user_text},
    ],
)
result = response.choices[0].message.content

# Summarizer
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "Summarize the user's text in 2 sentences."},
        {"role": "user", "content": user_text},
    ],
)
result = response.choices[0].message.content

# ... 3 more, each one a copy-paste with one change
```

### Problems:

| Problem | Pain level |
|---------|-----------|
| **Repetitive setup** — same `client.chat.completions.create(...)` everywhere | 😩 |
| **Long messages list** to build every time | 😩 |
| **Hard to reuse prompts** — they're stuck inside strings | 😩😩 |
| **Switching models means changing every endpoint** | 😩😩 |
| **No memory built in** — chat history is your problem | 😩😩 |
| **No tools** — LLM can't call functions | 😩😩😩 |
| **No structured outputs** — always strings | 😩😩😩 |

**Raw LLM calls are like raw SQL** — they work, but the boilerplate is painful.

> 💡 **Just like SQLModel saved us from raw SQL, LangChain saves us from raw LLM calls.**

---

## 3. What is LangChain?

> **LangChain** is a Python library that makes building LLM-powered apps clean and powerful.
>
> It gives you **building blocks** — prompts, models, parsers, memory, tools, agents — that you can **plug together**.

### The big ideas:

| LangChain gives you | What it replaces |
|---------------------|------------------|
| **ChatModel** — wrapper around any LLM | Raw `client.chat.completions.create(...)` |
| **PromptTemplate** — reusable prompts | Hard-coded strings |
| **Output Parser** — converts LLM text to JSON/objects | Manual parsing |
| **Memory** — automatic conversation history | DIY in-memory lists |
| **Tools** — let the LLM call functions | Custom routing logic |
| **Agents** — LLM decides what to do | Manual if/else logic |
| **Chains** — link the above with the `|` pipe | Glue code everywhere |

### Why this matters:

You write **less code**. You **swap LLM providers** by changing one line. You build **reusable prompts**. You add **memory** with one import.

> 🎯 **LangChain is the industry standard for production GenAI apps in Python.**

---

## 4. Installation

In your terminal:

```bash
pip install langchain langchain-groq python-dotenv
```

| Package | What it's for |
|---------|---------------|
| `langchain` | The core library |
| `langchain-groq` | Groq integration (uses your existing API key!) |
| `python-dotenv` | You already have this — for `.env` |

**Good news:** You **already have your Groq API key** from the previous class. No new signup. ✨

---

## 5. Your First ChatModel

Instead of using `Groq` client directly, we use **LangChain's `ChatGroq`**:

```python
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

# The LangChain way
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)

# Just ask
response = llm.invoke("Tell me a 1-line joke about Python.")
print(response.content)
```

### Output:

```
Why did the Python developer go broke? Because he used up all his cache!
```

### Compare side-by-side:

**Raw Groq (last class):**

```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Tell me a 1-line joke about Python."}],
)
print(response.choices[0].message.content)
```

**LangChain (today):**

```python
response = llm.invoke("Tell me a 1-line joke about Python.")
print(response.content)
```

### What changed?

| Raw Groq | LangChain |
|----------|-----------|
| Build `messages` list | Pass a string directly |
| `response.choices[0].message.content` | `response.content` |
| Tied to Groq only | Swap to OpenAI, Anthropic, etc. by 1 line |

**Cleaner. Shorter. Provider-agnostic.** 🎉

### Swapping models is easy:

```python
# Change one line — same code works:
# llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=...)
# llm = ChatOpenAI(model="gpt-4", api_key=...)        # if you had OpenAI
# llm = ChatAnthropic(model="claude-3-opus", api_key=...)  # if you had Claude
```

This is the **superpower** of LangChain — your code doesn't care which LLM you use.

---

## 6. PromptTemplate — Static Prompts

A **prompt** is the instruction you send to the LLM. Instead of hardcoding it, you make it a reusable **template**.

```python
from langchain_core.prompts import PromptTemplate

# Define once, use many times
prompt = PromptTemplate.from_template("Tell me a joke about Python.")

# Format it (returns a string)
text = prompt.format()
print(text)
# "Tell me a joke about Python."

# Use it with the LLM
response = llm.invoke(text)
print(response.content)
```

That's it for static. But the real power comes with **variables**.

---

## 7. PromptTemplate — Dynamic Prompts

Add `{variables}` in the template — they get filled in later.

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("Tell me a joke about {topic}.")

# Use the same template for different topics
text1 = prompt.format(topic="Python")
text2 = prompt.format(topic="cats")
text3 = prompt.format(topic="databases")

print(text1)   # "Tell me a joke about Python."
print(text2)   # "Tell me a joke about cats."
print(text3)   # "Tell me a joke about databases."
```

### Multiple variables:

```python
prompt = PromptTemplate.from_template(
    "Translate the following text to {language}: {text}"
)

formatted = prompt.format(language="French", text="Hello, how are you?")
print(formatted)
# "Translate the following text to French: Hello, how are you?"

response = llm.invoke(formatted)
print(response.content)
# "Bonjour, comment allez-vous ?"
```

### Why this is powerful:

- ✅ **Reusable** — define the prompt once, use anywhere
- ✅ **Clean** — no f-string ugliness in your function bodies
- ✅ **Composable** — chain prompts together (next class)
- ✅ **Versionable** — store prompts in YAML/JSON files

---

## 8. ChatPromptTemplate

For chat models, you often want **system + user** messages (like the Groq class). LangChain has `ChatPromptTemplate` for that.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful translator. Translate everything to {language}."),
    ("user", "{text}"),
])

# Format both at once
messages = prompt.format_messages(language="French", text="Hello, how are you?")
print(messages)
# [SystemMessage(content="You are a helpful translator..."),
#  HumanMessage(content="Hello, how are you?")]

# Send to LLM
response = llm.invoke(messages)
print(response.content)
# "Bonjour, comment allez-vous ?"
```

### Compare to raw Groq:

**Raw Groq:**

```python
messages = [
    {"role": "system", "content": f"You are a helpful translator. Translate everything to {language}."},
    {"role": "user", "content": text},
]
```

**LangChain:**

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful translator. Translate everything to {language}."),
    ("user", "{text}"),
])
messages = prompt.format_messages(language=language, text=text)
```

LangChain's version is:
- Reusable (define once, use many times)
- Clearer (system/user roles named explicitly as tuples)
- Easier to test (template separated from data)

---

## 9. Before vs After

Let's see a **real comparison** — a translator app.

### ❌ Raw Groq (the old way):

```python
def translate(text: str, language: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Translate the user's text to {language}."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content
```

### ✅ LangChain (the new way):

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate the user's text to {language}."),
    ("user", "{text}"),
])

def translate(text: str, language: str) -> str:
    messages = prompt.format_messages(language=language, text=text)
    response = llm.invoke(messages)
    return response.content
```

### Differences:

| Aspect | Raw Groq | LangChain |
|--------|----------|-----------|
| Prompt definition | Inside the function | Outside, reusable |
| Provider lock-in | Groq only | Any provider |
| String formatting | f-strings inside messages | Template variables |
| `.content` access | Long path | Short path |

> 🪄 **Next class:** We'll learn **LCEL** — a `|` pipe operator that makes this even shorter. Spoiler: it becomes a 1-liner.

---

## 10. Use It in FastAPI

Let's wire LangChain into a real `/translate` endpoint.

### `main.py`:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

# Setup
load_dotenv()
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)

# Reusable prompt (defined once)
translate_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a professional translator. Translate the user's text to {language}. Return ONLY the translation, nothing else."),
    ("user", "{text}"),
])

app = FastAPI()

class TranslateRequest(BaseModel):
    text: str
    language: str

class TranslateResponse(BaseModel):
    original: str
    translation: str
    language: str

@app.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    messages = translate_prompt.format_messages(
        language=req.language,
        text=req.text,
    )
    response = llm.invoke(messages)
    return TranslateResponse(
        original=req.text,
        translation=response.content,
        language=req.language,
    )
```

### Run it:

```bash
uvicorn main:app --reload
```

### Test in `/docs`:

1. Open `http://localhost:8000/docs`
2. Find **POST `/translate`** → click **"Try it out"**
3. Send this JSON:

```json
{
  "text": "Hello, how are you today?",
  "language": "Urdu"
}
```

4. **Execute**

### Response:

```json
{
  "original": "Hello, how are you today?",
  "translation": "السلام علیکم، آج آپ کیسے ہیں؟",
  "language": "Urdu"
}
```

🎉 **You just built a LangChain-powered FastAPI endpoint!**

Try more languages — French, Spanish, Arabic, Hindi. Same endpoint, same code. Just change `language`.

---

## 11. Common Mistakes

### ❌ Mistake 1: Forgot `load_dotenv()`

```python
llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"))    # ❌ returns None
```

✅ **Correct:**

```python
load_dotenv()
llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"))
```

---

### ❌ Mistake 2: Wrong import

```python
from langchain_groq import Groq    # ❌ wrong class
```

✅ **Correct:**

```python
from langchain_groq import ChatGroq    # ✅
```

---

### ❌ Mistake 3: Forgetting `.content`

```python
response = llm.invoke("Hello")
print(response)    # ❌ prints a giant object
```

✅ **Correct:**

```python
print(response.content)    # ✅ just the text
```

---

### ❌ Mistake 4: Forgetting to `format` the prompt

```python
response = llm.invoke(prompt)    # ❌ sends the template, not a filled string
```

✅ **Correct:**

```python
text = prompt.format(topic="cats")
response = llm.invoke(text)
```

Or for ChatPromptTemplate:

```python
messages = prompt.format_messages(language="French", text="Hello")
response = llm.invoke(messages)
```

---

### ❌ Mistake 5: Mismatched variable names

```python
prompt = ChatPromptTemplate.from_messages([
    ("user", "{question}"),
])
messages = prompt.format_messages(text="Hello")    # ❌ used `text`, not `question`
```

✅ **Correct:**

```python
messages = prompt.format_messages(question="Hello")    # ✅ matches template
```

---

## 12. Practice Exercises

All exercises should be tested in `/docs`. 🎯

### Exercise 1 — Summarizer endpoint
Build POST `/summarize` that takes long text and returns a 2-sentence summary using LangChain + `ChatPromptTemplate`.

### Exercise 2 — Joke generator
Build POST `/joke` that takes a `topic` (string) and returns a joke about it. Use `PromptTemplate.from_template("Tell me a joke about {topic}.")`.

### Exercise 3 — Code reviewer
Build POST `/review-code` that takes Python code and returns suggestions. Use a system prompt that says "You are a senior Python reviewer."

### Exercise 4 — Personality chat
Build POST `/chat-as` that takes `personality` and `question`. The LLM responds **as** that personality. Example:
```json
{"personality": "Shakespeare", "question": "Why is the sky blue?"}
```

### Exercise 5 — Multi-language
Reuse the `translate_prompt` from the lesson. Build a script that translates the SAME English text into 5 different languages in one run (loop the LLM call).

### Exercise 6 — Reusable email writer
Build POST `/write-email` that takes `recipient`, `topic`, and `tone` (formal/casual). Use a single `ChatPromptTemplate` with 3 variables.

### Exercise 7 — Swap models (bonus)
Change the model from `llama-3.3-70b-versatile` to `llama-3.1-8b-instant`. Compare response quality and speed. Notice — only ONE line had to change.

---

## 13. Quick Cheat Sheet

```python
# ---- imports ----
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
import os

# ---- setup ----
load_dotenv()
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
)

# ---- simple call ----
response = llm.invoke("Tell me a joke.")
print(response.content)

# ---- PromptTemplate (single string) ----
prompt = PromptTemplate.from_template("Tell me a joke about {topic}.")
text = prompt.format(topic="cats")
response = llm.invoke(text)

# ---- ChatPromptTemplate (system + user) ----
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a {role}."),
    ("user", "{question}"),
])
messages = prompt.format_messages(role="Python expert", question="What is FastAPI?")
response = llm.invoke(messages)

# ---- get the answer ----
print(response.content)
```

### Quick comparison:

| What you want | Use |
|---------------|-----|
| One string prompt | `PromptTemplate.from_template(...)` |
| System + User messages | `ChatPromptTemplate.from_messages([...])` |
| Fill in variables | `.format(...)` or `.format_messages(...)` |
| Send to LLM | `llm.invoke(...)` |
| Get the text | `response.content` |

---

## 🎯 Summary — What You Learned Today

✅ Why raw LLM calls become painful at scale
✅ LangChain = clean building blocks for LLM apps
✅ Installed `langchain` + `langchain-groq`
✅ `ChatGroq` — LangChain's wrapper for Groq
✅ `PromptTemplate` — reusable single-string prompts
✅ `ChatPromptTemplate` — reusable system + user prompts
✅ Variables in templates → fill in at runtime
✅ Built a `/translate` FastAPI endpoint with LangChain — tested in `/docs`
✅ Code is now provider-agnostic — swap LLMs by changing 1 line

---

## 14. What's Next?

Today you used:

```python
messages = prompt.format_messages(language="French", text="Hello")
response = llm.invoke(messages)
return response.content
```

That's **3 lines** to call an LLM with a prompt. **Tomorrow** you'll learn **LCEL (LangChain Expression Language)** — the magic `|` pipe operator that turns those 3 lines into **1 line**:

```python
chain = prompt | llm | StrOutputParser()
return chain.invoke({"language": "French", "text": "Hello"})
```

You'll meet:
- The `|` pipe operator
- Output parsers (`StrOutputParser`, `JsonOutputParser`)
- Chain composition (combining multiple steps)
- Why every LangChain tutorial uses `|`

---

**Remember:**

```python
# This is the LangChain mantra:
prompt | llm | parser

# Build prompts once. Swap models freely. Parse outputs cleanly.
```

LangChain is just **clean, composable, professional LLM code**. You're now on the path that every real GenAI engineer walks.

**Happy Coding! 🚀**
