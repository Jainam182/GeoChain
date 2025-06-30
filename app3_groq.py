

import streamlit as st
import time
import os
from openai import OpenAI

# --- Configure Groq Client ---
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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", # Or replace with your key: "your-groq-api-key"
)
response = client.chat.completions.create(
    model="deepseek-r1-distill-llama-70b",  # or another Groq-supported model
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, what can you do?"}
    ],
    temperature=0.4
)

st.set_page_config(page_title="GeoAI Chat", page_icon="🗺️", layout="wide")

st.title("🗺️ GeoAI Chat Assistant")
st.markdown("Enter a geospatial query and get step-by-step reasoning using GDAL or WhiteboxTools.")

if "history" not in st.session_state:
    st.session_state.history = []

query = st.text_input("Enter your geospatial query", placeholder="e.g., Flood mapping in Mumbai")

if st.button("Send") and query:
    with st.spinner("Generating response..."):
        system_prompt = '''
You are a highly skilled geospatial analyst. When given a geospatial query, think aloud in a casual and detailed way, as if you're explaining it to yourself or a colleague.

Start by saying something like "Alright, I need to figure out how to..." and then continue step-by-step. Your tone should be natural, reflective, and logical — not robotic or bullet-point-like.

Break it down into:

1. **Chain-of-Thought Reasoning** — a stream-of-consciousness where you:
   - Clarify the query and any assumptions (e.g., is the location a neighborhood, ward, or loosely defined place?)
   - Consider whether the spatial boundary is predefined or needs to be approximated using wards, zones, OSM features, or manual merging
   - Identify required datasets: vector boundaries (e.g., shapefiles, GeoJSON), tabular data (CSV), raster (if needed)
   - Mention trusted sources (e.g., Census 2011, OSM, Bhuvan, Bhoonidhi, municipal portals)
   - Describe how to match tabular data with spatial boundaries (e.g., via ward codes or joinable attributes)
   - Specify use of **projected coordinate systems** for geometry-based computations (e.g., UTM Zone 43N — EPSG:32643)
   - Emphasize **geometry validation** before processing (e.g., using `ogr2ogr -makevalid`) to prevent CLI crashes
   - Clearly state **area unit conversions** (e.g., divide m² by 1,000,000 to get km²)
   - Explain fallback logic for boundaries that aren’t clean (e.g., clip, dissolve, or draw manually)
   - Evaluate toolchain:
     - **GDAL** for CRS reprojection, format conversion, SQL joins
     - **WhiteboxTools** for area (`PolygonArea`) and attribute calculations (`AttributeCalculator`)
     - Use exact CLI syntax for WhiteboxTools, e.g.:
       ```bash
       whitebox_tools -r="PolygonArea" --input="input.geojson" --output="output.geojson"
       whitebox_tools -r="AttributeCalculator" --input="input.gpkg" --output="output.gpkg" --attribute="pop_density" --expression="population / (area / 1000000)"
       ```
   - Clarify: **WhiteboxTools cannot join CSV to spatial layers**. Instead, use:
     - `ogr2ogr` with SQL (requires GeoPackage/SQLite format)
     - or pre-merge using Python (e.g., GeoPandas)
   - Plan to export as **GeoJSON** or **TopoJSON** for web visualization (e.g., Leaflet, Mapbox, MapLibre)
   - Avoid rasterization unless working with interpolated or continuous surfaces (e.g., rainfall, elevation)
   - Keep the tone exploratory, detailed, and human — as if you're walking through a real task live with a teammate

2. **Output** section:
   - **WorkFlow:** A plain English summary of the steps — from raw data to visual layer
   - **GDAL + Whitebox Workflow:** A detailed, CLI-accurate sequence including:
     - Data acquisition (e.g., ward boundaries, census CSV)
     - CRS reprojection (`ogr2ogr -t_srs EPSG:32643`)
     - Geometry validation (`ogr2ogr -makevalid`)
     - Polygon dissolve (if needed)
     - Area calculation via `PolygonArea`
     - CSV/spatial join using:
       - `ogr2ogr -sql` inside a GeoPackage, or
       - GeoPandas merge if automating in Python
     - Density calculation using `AttributeCalculator` with the correct expression
     - Export to `GeoJSON` or `MBTiles` for frontend rendering

Make sure to:
- Use accurate geospatial terminology (e.g., dissolve, reproject, attribute join, spatial clip)
- Validate geometry before spatial computation
- Join population attributes *outside* WhiteboxTools
- Export results in UI-ready formats like `.geojson` or `.gpkg`
- Avoid fake commands (e.g., `wb_dissolve`) — only use real CLI syntax
- Explain edge cases and fallback logic (e.g., when boundaries are missing or ambiguous)

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
[Detailed, natural explanation of what you're trying to do, how you plan to do it, what data/tools you’ll use, and any challenges you anticipate.]

**Output:**
**WorkFlow:** [Plain English summary of the full process]
**GDAL + Whitebox Workflow:**
1. Step one
2. Step two
...

Never skip reasoning. Always work through each task aloud like you're solving it in real time. Use production-grade syntax and commands that can run in scripts without modification.
'''

        prompt = system_prompt + f"\n**Query:** \"{query}\""

        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f'**Query:** "{query}"'}
                ],
                temperature=0.4,
                max_tokens=4096,
                top_p=1,
                stop=None
            )

            full_response = response.choices[0].message.content.strip()

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

st.caption("Built with ❤️ using Streamlit and Groq Cloud API")
