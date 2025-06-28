
# 🔍 Geospatial Workflow Automation with LLMs (Bharatiya Antariksh Hackathon - PS-4)

This project is developed for **Problem Statement 4 (PS-4)** of the **Bharatiya Antariksh Hackathon 2025**, with a focus on automating complex geospatial analysis tasks using Chain-of-Thought (CoT) reasoning powered by LLMs and GIS toolchains like **GDAL** and **WhiteboxTools**.

---

## 🧠 Problem Statement - PS-4 (Verbatim)

### Designing a Chain-of-Thought-Based LLM System for Solving Complex Spatial Analysis Tasks Through Intelligent Geoprocessing Orchestration

Geospatial challenges such as flood risk assessment, site suitability analysis, or land cover monitoring often demand sophisticated workflows involving various GIS tools and data sources. Traditionally, constructing these workflows requires expert knowledge and manual processes. This challenge invites participants to build a system that uses reasoning capabilities of Large Language Models (LLMs) to automatically plan and execute geospatial workflows—step-by-step—much like a human expert.

### 📌 Objective:
- Develop a reasoning-enabled framework combining LLMs and geoprocessing APIs to auto-generate multi-step geospatial workflows from natural language queries.
- Enable integration of heterogeneous spatial datasets and libraries for tool/resource selection.
- Build an interface translating user queries into sequential geoprocessing tasks with transparent Chain-of-Thought reasoning.
- Demonstrate with benchmark tasks like flood mapping and site selection including input/output, metrics, and visualizations.

---

## 🚀 How to Run This Project

### 1. Prerequisites
Make sure you have the following installed:
- Python 3.10+
- `gdal`
- `whitebox` Python wrapper (`pip install whitebox`)
- `streamlit` (for UI)
- A valid API key for Gemini or Groq (stored as environment variables or inside the script)

---

### 2. Files Description

| File     | Description |
|----------|-------------|
| `app.py` | Uses **Gemini AI** to generate Chain-of-Thought workflows + GIS pipelines. Tested and works well for most PS-4 cases. |
| `app2.py` | Reserved for **future expansion** — may include advanced RAG support or elevation surface analysis. |
| `app3.py` | Uses **Groq API** with LLaMA/Mistral and currently provides ~90–95% accurate responses for PS-4-type queries. Highly optimized for performance and logic clarity. |

---

### 3. Running the Application

You can launch any of the apps using:

```bash
streamlit run app.py
````

or

```bash
streamlit run app3.py
```

Make sure to add your API keys in the appropriate sections (Gemini, Groq).

---

## 🔧 Tools & Tech Stack

* 🗺️ GDAL (geospatial file manipulation)
* 🧰 WhiteboxTools (geospatial analysis)
* 🤖 Gemini AI / Groq (LLM backend)
* 📦 Streamlit (web UI for input/output)
* 🐍 Python 3.10+

---

## 📁 Directory Structure

```plaintext
├── app.py                 # Gemini-based AI workflow generator
├── app2.py                # In-development module
├── app3.py                # Groq-based workflow logic (95% accuracy)
├── LICENSE                # MIT License
├── README.md              # You're reading it!
├── data/                  # Example datasets (boundaries, CSVs)
└── workflows/             # Auto-generated workflows or logs
```

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🤝 Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 👥 Team
---
Jainam Jagani,
Sujal Israni,
Kashish Jain,
Anvee Shetye,


