import streamlit as st
import google.generativeai as genai
import time

# --- Configure Gemini API ---
genai.configure(api_key="AIzaSyBmjggCiCz04mByKiadG4I4h2xICqLdtuM")
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="GeoAI Chat", page_icon="🗺️", layout="wide")

st.title("🗺️ GeoAI Chat Assistant")
st.markdown("Enter a geospatial query and get step-by-step reasoning using GDAL or WhiteboxTools.")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Enter your geospatial query", placeholder="e.g., Flood mapping in Mumbai")

if st.button("Send") and query:
    with st.spinner("Generating response..."):
        system_prompt = '''You are a highly detailed and expert geospatial assistant. Given a user's geospatial query, break it down into two parts:

1. **Chain-of-Thought (CoT) Reasoning** — Think out loud and describe in full detail:
   - What the query is asking for
   - What geospatial concepts are involved (e.g., terrain, hydrology, population)
   - What datasets are required
   - Why each dataset is needed
   - What tools can be used to manipulate them
   - How the workflow will be constructed logically from the query
   - Any assumptions or caveats

2. **Output Block** with:
   - **WorkFlow:** A short, high-level summary of how the analysis will be done
   - **GDAL + WhiteboxTools Workflow:** Numbered technical steps using those tools, ready to be executed or implemented

Supported tasks:
- Flood mapping
- Elevation filtering
- Buffer analysis
- Population density
- Land use change
- Urban heat mapping
- Air quality analysis
- Road/traffic congestion
- Rainfall trends
- Watershed/contour mapping
- Proximity to hospitals/schools
- Slum vulnerability
- Forest cover loss
- Disaster risk zones

Respond in this format:

**Chain-of-Thought Reasoning:**
[Detailed multi-paragraph breakdown of every step: what, why, how, and with what data/tools. Be thorough.]

**Output:**
**WorkFlow:** [Plain English summary of the workflow]
**GDAL + Whitebox Workflow:**
1. Step one
2. Step two
...

Be extremely thorough and structured in your breakdown.
'''

        prompt = system_prompt + f"\n**Query:** \"{query}\""

        try:
            response = model.generate_content(prompt, generation_config={
                "temperature": 0.4,
                "max_output_tokens": 4096,
                "top_p": 1,
                "top_k": 40
            })
            full_response = response.text.strip()

            # Split into CoT and Output parts
            cot_part = ""
            output_part = ""
            if "**Output:**" in full_response:
                parts = full_response.split("**Output:**", 1)
                cot_part = parts[0].replace("**Chain-of-Thought Reasoning:**", "").strip()
                output_part = parts[1].strip()
            else:
                cot_part = full_response.strip()

            st.session_state.history.append((query, cot_part, output_part))

        except Exception as e:
            st.error(f"Error: {e}")

# Display chat history with proper formatting and typing effect
def stream_markdown(content):
    placeholder = st.empty()
    message = ""
    for char in content:
        message += char
        placeholder.markdown(message)
        time.sleep(0.001)

for user_q, cot, output in st.session_state.history[::-1]:
    st.markdown(f"**🧑 You:** {user_q}")
    tabs = st.tabs(["🧠 COT", "🛠️ Workflows"])

    with tabs[0]:
        stream_markdown(cot)
    with tabs[1]:
        stream_markdown(output)

st.caption("Built with ❤️ using Streamlit and Gemini API")