import streamlit as st
import requests
import os
API_URL = "https://router.huggingface.co/v1/chat/completions"
HF_TOKEN="" # <-- replace with your Hugging Face token
HEADERS = {"Authorization": f"Bearer {os.environ['HF_TOKEN']}"}


PROMPT_TEMPLATES = {
    "formal": "Rewrite the following resume summary in formal business English:\n\n{input}",
    "concise": "Summarize the following resume into 3 sentences:\n\n{input}",
    "impact": "Rewrite the following resume summary to emphasize measurable results:\n\n{input}",
    "story": "Rewrite the following resume summary with storytelling (challenge → action → result):\n\n{input}",
    "neutral": "Paraphrase the following resume summary in simple, clear language:\n\n{input}",
}

def query_hf(prompt, model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai"):
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"
    data = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        return str(data)

st.title("Resume Enhancer (Streamlit + Hugging Face API)")

resume = st.text_area("Paste your resume summary here:", height=200)
style = st.selectbox("Choose style:", list(PROMPT_TEMPLATES.keys()))

if st.button("Enhance"):
    if resume.strip():
        prompt = PROMPT_TEMPLATES[style].format(input=resume)
        result = query_hf(prompt)
        st.subheader("Enhanced Output")

        st.write(result)
