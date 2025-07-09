import streamlit as st
import time
import os
from groq import Groq

# --- Configure Groq Client ---
client = Groq(
    base_url="https://api.groq.com",
    api_key="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", # Or replace with your key: "your-groq-api-key"
)

# Custom CSS for Space/ISRO Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;700&display=swap');

/* Main container styling */
.main {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e0e0e0;
    min-height: 100vh;
    position: relative;
    overflow: hidden;
}

/* Animated starfield background */
.main::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: 
        radial-gradient(2px 2px at 20px 30px, #eee, transparent),
        radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
        radial-gradient(1px 1px at 90px 40px, #fff, transparent),
        radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
        radial-gradient(2px 2px at 160px 30px, #ddd, transparent);
    background-repeat: repeat;
    background-size: 200px 100px;
    animation: sparkle 20s linear infinite;
    z-index: -1;
    opacity: 0.6;
}

@keyframes sparkle {
    from { transform: translateY(0px); }
    to { transform: translateY(-100px); }
}

/* Header styling */
.header-container {
    background: linear-gradient(90deg, #0f3460 0%, #533483 50%, #e94560 100%);
    padding: 20px;
    margin: -1rem -1rem 2rem -1rem;
    border-bottom: 3px solid #00d4ff;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
    position: relative;
    overflow: hidden;
}

.header-container::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    animation: scan 3s linear infinite;
}

@keyframes scan {
    0% { left: -100%; }
    100% { left: 100%; }
}

.isro-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.5rem;
    font-weight: 900;
    text-align: center;
    color: #00d4ff;
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.8);
    margin-bottom: 10px;
    letter-spacing: 3px;
}

.subtitle {
    font-family: 'Exo 2', sans-serif;
    font-size: 1.2rem;
    text-align: center;
    color: #ff6b35;
    text-shadow: 0 0 10px rgba(255, 107, 53, 0.6);
    margin-bottom: 5px;
}

.mission-badge {
    text-align: center;
    font-family: 'Orbitron', monospace;
    font-size: 0.9rem;
    color: #ffd700;
    text-shadow: 0 0 10px rgba(255, 215, 0, 0.8);
    letter-spacing: 2px;
}

/* Input styling */
.stTextInput > div > div > input {
    background: rgba(15, 52, 96, 0.3) !important;
    border: 2px solid #00d4ff !important;
    color: #e0e0e0 !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 1.1rem !important;
    padding: 15px !important;
    border-radius: 10px !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    box-shadow: 0 0 25px rgba(0, 212, 255, 0.8) !important;
    border-color: #ff6b35 !important;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(45deg, #00d4ff, #0f3460) !important;
    border: none !important;
    color: white !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 12px 30px !important;
    border-radius: 25px !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.5) !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.5s;
}

.stButton > button:hover::before {
    left: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 30px rgba(0, 212, 255, 0.8) !important;
}

/* Chat message styling */
.chat-message {
    background: rgba(15, 52, 96, 0.2);
    border: 1px solid #00d4ff;
    border-radius: 15px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}

.chat-message::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #00d4ff, #ff6b35);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.user-message {
    font-family: 'Exo 2', sans-serif;
    font-size: 1.2rem;
    color: #00d4ff;
    font-weight: 700;
    text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
    margin-bottom: 10px;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: rgba(15, 52, 96, 0.1);
    border-radius: 10px;
    padding: 5px;
}

.stTabs [data-baseweb="tab"] {
    background: rgba(15, 52, 96, 0.3) !important;
    color: #00d4ff !important;
    border: 1px solid #00d4ff !important;
    border-radius: 8px !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(0, 212, 255, 0.2) !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(45deg, #00d4ff, #0f3460) !important;
    color: white !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.5) !important;
}

/* Response content styling */
.response-content {
    background: rgba(15, 52, 96, 0.1);
    border-radius: 10px;
    padding: 20px;
    margin: 10px 0;
    border: 1px solid rgba(0, 212, 255, 0.3);
    font-family: 'Exo 2', sans-serif;
    line-height: 1.6;
    color: #e0e0e0;
}

/* Spinner styling */
.stSpinner {
    border: 4px solid rgba(0, 212, 255, 0.3);
    border-top: 4px solid #00d4ff;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* HUD-style elements */
.hud-element {
    position: relative;
    border: 2px solid #00d4ff;
    background: rgba(15, 52, 96, 0.1);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    backdrop-filter: blur(5px);
}

.hud-element::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, #00d4ff, #ff6b35, #00d4ff);
    border-radius: 10px;
    z-index: -1;
    opacity: 0.3;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { opacity: 0.3; }
    to { opacity: 0.6; }
}

/* Footer styling */
.footer {
    text-align: center;
    font-family: 'Orbitron', monospace;
    color: #ff6b35;
    text-shadow: 0 0 10px rgba(255, 107, 53, 0.6);
    margin-top: 40px;
    padding: 20px;
    border-top: 1px solid rgba(0, 212, 255, 0.3);
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(15, 52, 96, 0.1);
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #00d4ff, #ff6b35);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #ff6b35, #00d4ff);
}

/* Loading animation */
.loading-text {
    font-family: 'Orbitron', monospace;
    color: #00d4ff;
    text-align: center;
    font-size: 1.2rem;
    animation: blink 1s infinite;
}

@keyframes blink {
    0%, 50% { opacity: 1; }
    51%, 100% { opacity: 0.3; }
}

/* Hide Streamlit default elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Configure page
st.set_page_config(
    page_title="ISRO GeoChain",
    page_icon="🛰️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Header with ISRO branding
st.markdown("""
<div class="header-container">
    <div class="isro-title">🛰️ ISRO GEOCHAIN</div>
    <div class="subtitle">Advanced Geospatial Analysis System</div>
    <div class="mission-badge">● MISSION STATUS: ACTIVE ●</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hud-element">
    <p style="color: #00d4ff; font-family: 'Exo 2', sans-serif; font-size: 1.1rem; text-align: center; margin: 0;">
        🌍 Enter geospatial queries or analysis parameters for real-time processing via satellite data networks
    </p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Input section
col1, col2 = st.columns([4, 1])

with col1:
    query = st.text_input(
        "",
        placeholder="🔍 Enter your Query (e.g., Flood mapping in Mumbai, Urban heat analysis Delhi...)",
        key="query_input"
    )

with col2:
    send_button = st.button("🚀 EXECUTE", key="send_button")

# Process query
if send_button and query:
    with st.spinner(""):
        st.markdown("""
        <div class="loading-text">
            🛰️ SATELLITE UPLINK ESTABLISHED<br>
            📡 PROCESSING GEOSPATIAL DATA<br>
            🔄 ANALYZING TERRAIN PATTERNS...
        </div>
        """, unsafe_allow_html=True)
        
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
   - Explain fallback logic for boundaries that aren't clean (e.g., clip, dissolve, or draw manually)
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
[Detailed, natural explanation of what you're trying to do, how you plan to do it, what data/tools you'll use, and any challenges you anticipate.]

**Output:**
**WorkFlow:** [Plain English summary of the full process]
**GDAL + Whitebox Workflow:**
1. Step one
2. Step two
...

Never skip reasoning. Always work through each task aloud like you're solving it in real time. Use production-grade syntax and commands that can run in scripts without modification.
'''

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
            st.error(f"🚨 MISSION CONTROL ERROR: {e}")

# Custom typing effect function
def stream_markdown(content):
    placeholder = st.empty()
    message = ""
    for char in content:
        message += char
        placeholder.markdown(f'<div class="response-content">{message}</div>', unsafe_allow_html=True)
        time.sleep(0.001)

# Display chat history
for i, (user_q, cot, output) in enumerate(st.session_state.history[::-1]):
    st.markdown(f"""
    <div class="chat-message">
        <div class="user-message">🧑‍🚀 MISSION COMMANDER: {user_q}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs with sci-fi styling
    tab1, tab2 = st.tabs(["🧠 ANALYSIS CORE", "🛠️ MISSION PROTOCOLS"])
    
    with tab1:
        st.markdown(f'<div class="response-content">{cot}</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown(f'<div class="response-content">{output}</div>', unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(0, 212, 255, 0.3); margin: 30px 0;'>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    🛰️ ISRO GEOCHAIN  v1.0 | Powered by Advanced Satellite Networks 🌌<br>
    <small>Built with ❤️ for Earth Observation & Space Technology</small>
</div>
""", unsafe_allow_html=True)