import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

# -------------------
# MODEL
# -------------------
model = ChatMistralAI(
    model="mistral-small-latest",
    api_key=os.getenv("MISTRAL_API_KEY")
)

# -------------------
# MEMORY
# -------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "output" not in st.session_state:
    st.session_state.output = ""

# -------------------
# UI
# -------------------
st.title("🚀 LinkedIn Post Generator")

st.write("Just enter details and generate a post in seconds.")

topic = st.text_input("Topic")
audience = st.text_input("Audience")

tone = st.selectbox(
    "Tone",
    ["Professional", "Friendly", "Motivational", "Technical"]
)

generate = st.button("Generate Post")

# -------------------
# PROMPT
# -------------------
prompt = PromptTemplate(
    template="""
You are an experienced LinkedIn content writer and personal branding expert.

Write a highly engaging LinkedIn post based on the details below:

Topic: {topic}
Audience: {audience}
Tone: {tone}

### Writing Style Requirements:
- Write like a real person sharing experience, not an AI
- Use a natural, conversational tone
- Start with a strong hook (question, story, or bold statement)
- Keep sentences short and easy to read
- Use simple English, avoid jargon
- Add emotional or personal touch where possible

### Structure:
1. Hook (attention-grabbing first 1–2 lines)
2. Main story or insight (realistic, relatable explanation)
3. Value section (tips, lessons, or insights)
4. Personal takeaway (what I learned or realized)
5. Call to Action (ask a question to audience)

### Rules:
- Do NOT sound generic or robotic
- Avoid phrases like "in today's world", "unlocking potential", "game changer"
- Include one small personal experience or example
- Make it feel like a real LinkedIn user wrote it after learning something
- Add 3 to 5 relevant hashtags at the end


Return ONLY the LinkedIn post.
""",
    input_variables=["topic", "audience", "tone"]
)
# -------------------
# GENERATE
# -------------------
if generate:

    if not topic or not audience:
        st.warning("Please fill all fields")
        st.stop()

    formatted_prompt = prompt.format(
        topic=topic,
        audience=audience,
        tone=tone
    )

    with st.spinner("Writing your post..."):
        result = model.invoke(formatted_prompt)

    post = result.content.strip()

    st.session_state.output = post
    st.session_state.history.append(post)

# -------------------
# OUTPUT
# -------------------
if st.session_state.output:
    st.subheader("Your Post")
    st.text_area("", st.session_state.output, height=300)

    st.download_button(
        "Download Post",
        st.session_state.output,
        file_name="linkedin_post.txt"
    )

# -------------------
# HISTORY (SIMPLE)
# -------------------
if st.session_state.history:
    st.markdown("### Previous Posts")

    for i, h in enumerate(reversed(st.session_state.history[-5:])):
        st.write(f"Post {i+1}")
        st.write(h[:120] + "...")
        st.markdown("---")