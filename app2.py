#Still in development, not ready for production use.

import streamlit as st
import google.generativeai as genai
import time
import json
import os
from datetime import datetime
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.llms import GooglePalm

# --- Configure Gemini API ---
genai.configure(api_key="Your Api Key")
model = genai.GenerativeModel("gemini-1.5-flash")

# --- RAG Setup ---
if not os.path.exists("vector_db"):
    raw_docs = TextLoader("rag_docs/gdal_qgis_docs.txt").load()
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = splitter.split_documents(raw_docs)
    vectorstore = FAISS.from_documents(docs, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
    vectorstore.save_local("vector_db")
else:
    vectorstore = FAISS.load_local("vector_db", GoogleGenerativeAIEmbeddings(model="models/embedding-001"), allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever()

st.set_page_config(page_title="GeoAI Chat", page_icon="🗺️", layout="wide")
st.title("🗺️ GeoAI Chat Assistant")
st.markdown("Enter a geospatial query and get step-by-step reasoning using GDAL or WhiteboxTools.")

# --- Create output directory ---
Path("exports").mkdir(parents=True, exist_ok=True)

# --- Session state ---
if "history" not in st.session_state:
    st.session_state.history = []
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d%H%M%S")

# --- Sidebar for inputs and advanced tools ---
st.sidebar.header("⚙️ Inputs & Tools")
input_source = st.sidebar.selectbox("Choose Input Source", [
    "None", "STAC API Link", "OSM Extract", "Upload Shapefile/DEM/CSV"
])

input_metadata = {}
if input_source == "STAC API Link":
    st.sidebar.text_input("STAC API URL", key="stac_url")
    input_metadata["source"] = "STAC"
elif input_source == "OSM Extract":
    st.sidebar.text_input("OSM Extract Link", key="osm_url")
    input_metadata["source"] = "OSM"
elif input_source == "Upload Shapefile/DEM/CSV":
    uploaded_file = st.sidebar.file_uploader("Upload File", type=["shp", "tif", "csv"])
    if uploaded_file:
        input_metadata["filename"] = uploaded_file.name
        input_metadata["format"] = uploaded_file.type

# --- Query box ---
query = st.text_input("Enter your geospatial query", placeholder="e.g., Flood mapping in Mumbai")

# --- Submit and Process ---
if st.button("Send") and query:
    with st.spinner("Generating response with context-aware RAG..."):
        start_time = time.time()

        # RAG snippet
        relevant_docs = retriever.get_relevant_documents(query)
        rag_snippet = "\n\n".join([doc.page_content for doc in relevant_docs[:3]])

        system_prompt = f'''
You are a geospatial assistant. Given a user's geospatial query, break it down into two parts:

1. Chain-of-Thought (CoT) reasoning — Think out loud and describe in full detail:
   - how you break the problem down step-by-step.
   - What the query is asking for
   - What geospatial concepts are involved (e.g., terrain, hydrology, population)
   - What datasets are required
   - Why each dataset is needed
   - What tools can be used to manipulate them
   - How the workflow will be constructed logically from the query
   - Any assumptions or caveats
2. Output block with:
   - WorkFlow: A short summary in plain English.
   - GDAL + WhiteboxTools Workflow: Numbered technical steps using those tools.

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

Use the following documentation as context:
{rag_snippet}

Respond in this format:

**Chain-of-Thought Reasoning:**
[step-by-step breakdown here]

**Output:**
**WorkFlow:** [summary here]
**GDAL + Whitebox Workflow:**
1. Step one
2. Step two
...
'''

        prompt = system_prompt + f"\n**Query:** \"{query}\""

        try:
            response = model.generate_content(prompt, generation_config={
                "temperature": 0.4,
                "max_output_tokens": 2048,
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

            end_time = time.time()
            metrics = {
                "token_estimate": len(full_response.split()),
                "generation_time_sec": round(end_time - start_time, 2),
                "workflow_length": output_part.count("\n")
            }

            entry = {
                "query": query,
                "session_id": st.session_state.session_id,
                "timestamp": datetime.now().isoformat(),
                "input_metadata": input_metadata,
                "cot": cot_part,
                "workflow": output_part,
                "metrics": metrics,
                "docs_used": rag_snippet
            }
            st.session_state.history.append(entry)

            # Save JSON
            with open(f"exports/{st.session_state.session_id}_{len(st.session_state.history)}.json", "w") as f:
                json.dump(entry, f, indent=2)

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.warning("Common causes: CRS mismatch, NoData overlaps, invalid topology.\n\nTry adding a step to fix geometries or reproject your data.")

# --- Display Previous Chats ---
for i, item in enumerate(st.session_state.history[::-1]):
    st.markdown(f"**🧑 You:** {item['query']}")
    tabs = st.tabs(["🧠 COT", "🛠️ Workflows", "📊 Metrics", "📁 JSON", "📚 RAG Snippets"])

    with tabs[0]:
        st.markdown(item["cot"])

    with tabs[1]:
        st.markdown(item["workflow"])

    with tabs[2]:
        st.json(item["metrics"])

    with tabs[3]:
        json_download = json.dumps(item, indent=2)
        st.download_button(
            label="📥 Download Workflow JSON",
            file_name=f"workflow_{item['session_id']}_{i+1}.json",
            mime="application/json",
            data=json_download
        )

    with tabs[4]:
        st.code(item["docs_used"], language="markdown")

st.caption("Built with ❤️ using Streamlit and Gemini API + RAG")
