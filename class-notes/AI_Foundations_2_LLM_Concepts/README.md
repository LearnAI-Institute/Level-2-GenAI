# AI Foundations — Class 2: How LLMs Actually Work

> A simple guide to the inner life of a Large Language Model.
> Six core concepts. No math. One reference table. Lots of intuition.

> 📍 **Week 1 · Class 2** of the Level Two GenAI Course

> **What you should already know:**
> - Class 1: The AI Hierarchy (AI → ML → DL → Transformers → LLMs → GenAI)

---

## Table of Contents

1. [Recap from Class 1](#1-recap-from-class-1)
2. [What happens when you talk to ChatGPT?](#2-what-happens-when-you-talk-to-chatgpt)
3. [Tokenization — how the LLM "reads"](#3-tokenization)
4. [Context Window — the LLM's memory limit](#4-context-window)
5. [Attention — the secret sauce](#5-attention)
6. [Temperature — the creativity dial](#6-temperature)
7. [Hallucinations — when LLMs make stuff up](#7-hallucinations)
8. [Grounding — the cure (preview of RAG)](#8-grounding)
9. [The Full Reference Table](#9-the-full-reference-table)
10. [Quick concept check](#10-quick-concept-check)
11. [What's next](#11-whats-next)

---

## 1. Recap from Class 1

In Class 1, we built the AI hierarchy:

```
AI → ML → Deep Learning → Transformers → LLMs → GenAI
```

We landed on this fact:
> **LLMs (Large Language Models) are the primary tool of this course.**

But we never opened the hood. How does ChatGPT actually work?

That's today's class. 🛠️

---

## 2. What Happens When You Talk to ChatGPT?

You type:

> *"Tell me a joke about cats."*

And ChatGPT replies:

> *"Why did the cat sit on the computer? Because it wanted to keep an eye on the mouse!"*

Under the hood, **six things happen** between your text going in and the joke coming out:

1. Your sentence is broken into **tokens**
2. Tokens are checked against the **context window** (size limit)
3. The model uses **attention** to figure out which words matter most
4. **Temperature** controls how creative the response will be
5. The model generates an answer — sometimes it might **hallucinate**
6. **Grounding** (if used) keeps the answer connected to real facts

Each one of those bolded words is a class concept. Let's open them one by one.

---

## 3. Tokenization

> **A token is a small piece of text — usually a word, part of a word, or a punctuation mark.**

Before an LLM can process your text, it breaks it into tokens. **Tokens are the unit the LLM thinks in** — not letters, not words.

### Example:

The sentence:

```
"I love pizza."
```

might become these tokens:

```
["I", " love", " pizza", "."]
```

That's 4 tokens.

### Now look at this:

```
"Tokenization"
```

This single English word might split into multiple tokens:

```
["Token", "ization"]
```

That's 2 tokens for **one** word.

### Why does tokenization matter?

| Why it matters | What this means for you |
|----------------|-------------------------|
| **APIs charge per token** | More tokens = more cost |
| **LLMs have a token limit** | You can't send unlimited text |
| **Shorter prompts cost less** | Be concise where possible |
| **Different languages have different ratios** | Urdu/Hindi often = more tokens than English for the same meaning |

### Try it yourself (optional demo):

```python
# pip install tiktoken
import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4")
tokens = encoder.encode("Tokenization is the first step.")
print(tokens)              # list of token IDs (numbers)
print(len(tokens))         # how many tokens
```

> 💡 Try your own name. Try a Hindi sentence. Compare token counts. You'll be surprised.

---

## 4. Context Window

> **The context window is the maximum amount of text (in tokens) an LLM can "see" at one time.**

Think of it like a small whiteboard. The LLM can only read what's on the board right now. Anything older than the board gets erased.

### Real numbers (today's models):

| Model | Context Window |
|-------|----------------|
| GPT-3.5 | ~4,000 — 16,000 tokens |
| GPT-4 | ~8,000 — 128,000 tokens |
| Claude Sonnet | ~200,000 tokens |
| Llama 3 (Groq) | ~8,000 tokens |

### Why this matters:

You **cannot fit a whole book** in a context window. Books have ~80,000+ tokens.

If you want an LLM to answer questions about a book, you need a trick — **send only the relevant part**.

> 🎯 **That trick is called RAG (Retrieval Augmented Generation).** We will build RAG systems in Phase 3 of this course.
>
> RAG exists *because* of the context window limit. Now you know why!

### Visual:

```
Your entire knowledge base ─────────────────► [millions of tokens]
                                                  ❌ won't fit

Context window of LLM     ──► [8,000 tokens]
                              ✅ this is all it can see at once
```

---

## 5. Attention

> **Attention is the mechanism that lets the LLM decide which words matter most when generating each new word.**

That sounds abstract. Try this example.

### Fill in the blank:

> *"The cat sat on the ___."*

Most likely answer: **mat**, **chair**, **floor**, etc.

How does the LLM decide? It looks at **all previous words** and asks:
- Which words help me predict what's next?
- *"cat"* and *"sat on"* are the most important.
- *"The"* is less important.

The model assigns **higher attention weight** to *"cat"* and *"sat on"* than to *"The"*. That's attention.

### Why it's a big deal:

Before Transformers (the architecture using attention), older models processed words **one at a time** like reading a book strictly left-to-right. They forgot context easily.

Transformers can **look at every word at once** and **decide what's important**. That's why modern LLMs feel so good at understanding context.

> ⚙️ **In short:** Attention = how the LLM "focuses" on the right words. It's the reason ChatGPT understands "she" refers to the woman mentioned 3 sentences ago.

---

## 6. Temperature

> **Temperature is a setting (between 0 and ~2) that controls how random or creative the LLM's output is.**

| Temperature | Behavior | Use case |
|-------------|----------|----------|
| `0.0` | Most predictable, almost robotic | Math, code, factual lookup |
| `0.3` — `0.5` | Mostly predictable, slightly varied | Customer support, summaries |
| `0.7` — `1.0` | Creative, varied | Stories, brainstorming, jokes |
| `1.5+` | Wild, sometimes nonsense | Experimentation only |

### Example: Ask "Tell me a 1-line joke about cats."

**Temperature 0:** "Why don't cats play poker in the jungle? Too many cheetahs."
*Always the same. Boring but reliable.*

**Temperature 0.8:** Could be any of:
- "Why do cats hate water? Because they read all the bad reviews."
- "Cats don't make calls. They make miss-calls."
- "I told my cat a joke about dogs. He didn't laugh — he was offended."

*Creative, fresh each time.*

### When you build apps:

| Building... | Set temperature to... |
|-------------|----------------------|
| A code assistant | `0` — be deterministic |
| A factual Q&A bot | `0.2` — mostly factual |
| A general chatbot | `0.7` — natural feel |
| A creative writer | `1.0` — let it flow |

We'll use temperature in our FastAPI + Groq class.

---

## 7. Hallucinations

> **A hallucination is when an LLM confidently generates incorrect or fabricated information.**

### Famous examples:

- ChatGPT once **invented fake legal cases** for a lawyer — citing case names that didn't exist. The lawyer used them in court. Disaster. 😬
- Asked about a small town, an LLM will sometimes invent a mayor's name that was never real.
- Asked about a recent event, the LLM may give a confident answer even if its training data doesn't include it.

### Why does this happen?

LLMs don't **know** facts. They are **prediction machines** — they predict the most likely next word based on patterns in their training data.

If your question has no pattern they trained on, they **still produce text** — they just guess. And the guess sounds confident because LLMs are trained to sound confident.

### The danger:

> **Hallucinations look exactly like real answers.** You can't tell the difference by reading.

That's the scary part. Confident + wrong = trust killer.

### What can we do?

We **ground** the LLM in real data. (Next section.)

---

## 8. Grounding

> **Grounding means connecting an LLM's response to verified, external data — so it stops guessing and starts citing.**

### Without grounding:

> Q: *"What is our company's refund policy?"*
> LLM: *"You can return items within 30 days for a full refund."* ← MADE UP

### With grounding:

> Q: *"What is our company's refund policy?"*
> System: *(retrieves real policy document)* → feeds it to LLM → LLM says:
> *"According to your company's policy on page 3: items can be returned within 14 days for refund and 30 days for store credit."* ← REAL

### How is this done?

A technique called **Retrieval Augmented Generation (RAG)**:

1. Find the relevant document/piece of text (retrieval)
2. Stuff it into the LLM's context window
3. Ask the LLM to answer **based on that text**

**RAG = LLM + a trusted source of truth.**

We will build full RAG pipelines in Phase 3 of this course. For now, just remember:

> **Hallucination is the disease. Grounding is the cure. RAG is the medicine.** 💊

---

## 9. The Full Reference Table

| Concept | Simple explanation | Why it matters for building apps |
|---------|-------------------|----------------------------------|
| **Tokenization** | Text is broken into small pieces called tokens before the LLM processes it | Explains why LLMs have a context limit — tokens cost money and space |
| **Context window** | Maximum amount of text (tokens) an LLM can see at one time | Why RAG exists — you cannot fit a whole book in the context window |
| **Embeddings** | Numbers that represent the meaning of text in vector space — similar meanings are close together | The entire foundation of RAG — semantic search uses embeddings |
| **Attention mechanism** | How the model decides which words are most important when generating a response | Why LLMs understand relationships across long text (not just nearby words) |
| **Temperature** | A setting that controls how random or deterministic the output is | Low = predictable answers, high = more creative but less accurate |
| **Hallucination** | When an LLM confidently generates incorrect or fabricated information | Why we build RAG — to ground responses in real, retrieved facts |
| **Grounding** | Connecting LLM output to verified external data sources | Core purpose of RAG — grounded generation is accurate generation |

> 📝 **Embeddings** is the seventh concept in this table — we'll dedicate a full class to it later (when we start RAG). For now, just remember: embeddings are how an LLM converts "meaning" into numbers.

---

## 10. Quick Concept Check

Answer in your own words:

1. **What is a token?** Roughly how many tokens is the sentence *"Hello, world!"*?

2. Why can't you feed an entire 300-page book into ChatGPT in one shot?

3. In the sentence *"The cat chased the dog because it was hungry"* — what does *"it"* refer to? Which mechanism helps the LLM figure that out?

4. If you're building a **factual Q&A bot**, should you use temperature `0.1` or `1.0`? Why?

5. If an LLM tells you something with 100% confidence — should you trust it? Explain in 1 sentence.

6. What does RAG stand for, and what problem does it solve?

---

## 11. What's Next?

You now understand **the inside of an LLM**. The next questions are:

> *"How do I make an LLM do useful things in my application?"*
> *"How do I call one from Python?"*
> *"How do I connect it to FastAPI?"*

That's where we head next:

| Class | Topic |
|-------|-------|
| **Week 1 · Class 3** (future) | **Embeddings deep dive** — meaning as numbers |
| **Week 2 → Week 3** | FastAPI, Pydantic, SQLModel — backend foundation |
| **Week 4** | **FastAPI + Groq** — your API starts talking to an LLM ⭐ |
| **Week 6+** | LangChain — building real GenAI applications |
| **Week 13+** | RAG, embeddings, vector databases — solving hallucinations for real |

Every concept from today will come back. Tokenization will matter when you count API costs. Context window will matter when you build chatbots. Hallucinations will matter when users trust your app. Grounding will matter when you build RAG.

---

**Remember:**

```
LLMs = pattern machines + confidence.
Hallucination is the price of confidence.
Grounding is how we earn the trust back.
```

**See you in the next class!** 🚀
