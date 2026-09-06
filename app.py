import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

st.title("🤖 AI Chatbot")

# ---------- Load Groq API key ----------
try:
    secret_key = (
        st.secrets.get("groq_API")
        or st.secrets.get("groq_api")
        or st.secrets.get("GROQ_API")
    )
except Exception:
    secret_key = None

groq_api_key = st.session_state.get("groq_api_key") or secret_key

if not groq_api_key:
    st.warning("Groq API key not found. Paste a valid key below (not saved to disk).")
    input_key = st.text_input("Enter Groq API key", type="password", key="input_groq")
    if input_key:
        st.session_state["groq_api_key"] = input_key
        st.rerun()
    st.stop()

# ---------- Model selection ----------
# llama-3.1-8b-instant / llama-3.3-70b-versatile are deprecated on Groq.
# Recommended replacements: openai/gpt-oss-20b, openai/gpt-oss-120b, qwen/qwen3.6-27b
if "model_name" not in st.session_state:
    st.session_state["model_name"] = "openai/gpt-oss-20b"

with st.sidebar:
    model_input = st.text_input(
        "Model name", value=st.session_state["model_name"], key="model_input"
    )
    st.session_state["model_name"] = model_input


@st.cache_resource
def get_llm(api_key: str, model: str):
    return ChatGroq(model=model, temperature=0.7, api_key=api_key)


llm = get_llm(groq_api_key, st.session_state["model_name"])

# ---------- Chat history ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def to_lc_messages(history):
    out = []
    for m in history:
        if m["role"] == "user":
            out.append(HumanMessage(content=m["content"]))
        else:
            out.append(AIMessage(content=m["content"]))
    return out


# ---------- User input ----------
user_input = st.chat_input("Type your message...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = llm.invoke(to_lc_messages(st.session_state.messages))
        ai_content = getattr(response, "content", None) or str(response)
    except Exception as e:
        err_text = str(e)
        st.error(f"Error while contacting LLM: {err_text}")

        if "invalid_api_key" in err_text.lower() or "401" in err_text:
            input_key = st.text_input(
                "Invalid API key — enter a new Groq API key",
                type="password",
                key="input_groq_retry",
            )
            if input_key:
                st.session_state["groq_api_key"] = input_key
                st.rerun()

        elif (
            "model_not_found" in err_text.lower()
            or "does not exist" in err_text.lower()
            or "404" in err_text
        ):
            st.warning("Model not found or inaccessible. Try: openai/gpt-oss-20b")
            new_model = st.text_input(
                "Model name (retry)",
                value=st.session_state.get("model_name", ""),
                key="input_model_retry",
            )
            if new_model and new_model != st.session_state.get("model_name"):
                st.session_state["model_name"] = new_model
                st.rerun()

        ai_content = f"⚠️ {err_text}"

    with st.chat_message("assistant"):
        st.write(ai_content)

    st.session_state.messages.append({"role": "assistant", "content": ai_content})
