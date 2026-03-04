import validators
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_core.documents import Document
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="LangChain: Summarize Text From Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From Website")
st.subheader("Summarize any webpage instantly")

with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

url = st.text_input("Enter Website URL", placeholder="https://example.com/article")

prompt_template = """
Provide a summary of the following content in 300 words:
Content: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])


def load_website(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0",
    }
    session = requests.Session()
    response = session.get(url, headers=headers, timeout=30, allow_redirects=True)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
        tag.decompose()

    main_content = (
        soup.find("article") or
        soup.find("main") or
        soup.find(class_=lambda c: c and "content" in c.lower()) or
        soup.find("body")
    )
    text = main_content.get_text(separator=" ", strip=True) if main_content else soup.get_text()
    text = " ".join(text.split())
    return [Document(page_content=text[:8000])]


if st.button("Summarize Website"):
    if not groq_api_key.strip():
        st.error("Please provide your Groq API key.")
    elif not url.strip():
        st.error("Please enter a website URL.")
    elif not validators.url(url):
        st.error("Please enter a valid URL (e.g. https://example.com).")
    elif "youtube.com" in url or "youtu.be" in url:
        st.error("YouTube URLs are not supported. Please enter a website URL.")
    else:
        try:
            with st.spinner("Fetching and summarizing..."):
                llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)
                data = load_website(url)
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.invoke({"input_documents": data})
                st.success(output_summary["output_text"])

        except requests.exceptions.Timeout:
            st.error("⏱️ The website took too long to respond. Try a different URL.")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Could not connect to the website. Check the URL or your internet.")
        except requests.exceptions.HTTPError as e:
            st.error(f"🚫 Website blocked the request (HTTP {e.response.status_code}). Try another URL.")
        except Exception as e:
            st.exception(f"Exception: {e}")
