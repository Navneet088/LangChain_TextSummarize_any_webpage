# 🦜 LangChain Web Summarizer

> **Summarize any webpage instantly — powered by Llama 3.1 via Groq**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-🦜-1C3C3C?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-Llama_3.1-FF6B35?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-Web_Scraping-4B8BBE?style=for-the-badge)

---

## 📌 Overview

**LangChain Web Summarizer** is an end-to-end AI web app that takes any website URL and returns a clean, structured **300-word summary**. It scrapes real HTML, strips noise, and passes meaningful content to a **Llama 3.1 model hosted on Groq** — all within a polished Streamlit interface.

No copy-pasting. No tab overload. Just paste a URL and read.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🔐 **Secure API Input** | Password-masked Groq API key field in sidebar with `.env` fallback |
| 🌐 **Smart Web Scraper** | Browser-mimicking headers (Chrome 120 UA), session-based requests, 30s timeout |
| 🧹 **HTML Noise Removal** | Auto-strips `<script>`, `<style>`, `<nav>`, `<footer>`, `<header>`, `<aside>`, `<form>` |
| 🎯 **Smart Content Targeting** | Priority chain: `<article>` → `<main>` → `.content` class → `<body>` fallback |
| ✂️ **Context Window Guard** | Normalises whitespace and caps text at **8,000 characters** |
| 🤖 **AI Summarization** | LangChain `stuff` chain with custom `PromptTemplate` → ~300-word output |
| ✅ **Input Validation** | URL format check, empty field guards, YouTube URL rejection |
| ⚠️ **Rich Error Handling** | Distinct messages for `Timeout`, `ConnectionError`, `HTTPError`, and generic exceptions |
| 🖥️ **Live UI Feedback** | `st.spinner()` during fetch, `st.success()` for output, `st.error()` for failures |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — UI framework
- **LangChain** — chain orchestration + prompt management
- **langchain-groq** — Groq-hosted Llama 3.1 8B Instant
- **requests + BeautifulSoup4** — web scraping pipeline
- **validators** — URL format validation
- **python-dotenv** — `.env` secret management

---

## 🚀 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/langchain-web-summarizer.git
cd langchain-web-summarizer
```

### 2. Install dependencies

```bash
pip install streamlit langchain langchain-groq
pip install requests beautifulsoup4 validators python-dotenv
```

### 3. Add your Groq API key

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Or enter it directly in the sidebar when the app launches.

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📖 How to Use

1. Open the app at `http://localhost:8501`
2. Enter your **Groq API key** in the sidebar (or set via `.env`)
3. Paste any **website URL** into the input field
4. Click **"Summarize Website"**
5. Read your clean AI-generated summary ✅

---

## 🏗️ How It Works

```
URL Input
   │
   ▼
requests.Session (browser headers)
   │
   ▼
BeautifulSoup HTML Parser
   │  strips: script, style, nav, footer, header, aside, form
   ▼
Smart Content Selector
   │  article → main → .content → body
   ▼
Text Cleaner (whitespace normalise + 8k char cap)
   │
   ▼
LangChain Document → stuff chain → PromptTemplate
   │
   ▼
Groq API (Llama 3.1 8B Instant)
   │
   ▼
300-word Summary → Streamlit UI
```

---

## ⚠️ Known Limitations

> - The `stuff` chain silently truncates content beyond 8,000 characters.
>   For long articles, consider switching to `map_reduce` or `refine` chain types.
> - YouTube and JS-heavy SPA pages are **not supported**.
> - Some websites block automated requests **(403)**. This is detected and reported clearly.

---

## 📁 Project Structure

```
langchain-web-summarizer/
│
├── app.py              # Main Streamlit application
├── .env                # API key (not committed to git)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 📦 requirements.txt

```
streamlit
langchain
langchain-groq
langchain-core
langchain-community
requests
beautifulsoup4
validators
python-dotenv
```

---

> Built with ❤️ using **LangChain · Groq · Streamlit**
