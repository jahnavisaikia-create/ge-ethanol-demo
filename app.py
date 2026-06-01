# Task Prompt: AI-Powered Ethanol Plant Tracker (Demo Build)

## 1. Project Overview & Objective
The goal is to build a functional prototype/demo of a global Ethanol Plant Metric Tracker. The initial focus is on **Brazil**, tracking plants that were active, planned, or under construction between **2003 and 2026**. 

The system must automate data extraction using AI from public sources, pass the data through a validation layer, and present it in an analyst dashboard for Human-in-the-Loop (HITL) verification. The final output must seamlessly map to a structured, 33-data-point client spreadsheet template.

---

## 2. Core Architecture & Feature Requirements

### Feature 1: AI Data Extraction Engine (Public Sources)
- **Capability:** Build a scraping/ingestion layer that targets public data sources (news, regulatory filings, industry reports) regarding Brazilian ethanol plants.
- **AI Task:** Use an LLM/NER (Named Entity Recognition) pipeline to parse unstructured text and extract specific plant metrics.
- **Temporal Filter:** Restrict/flag data to the 2003–2026 window.

### Feature 2: Human-in-the-Loop (HITL) Analyst Dashboard
- **UI/UX:** A clean, scannable dashboard for data analysts.
- **Functionality:** - Display AI-extracted plant data side-by-side with the source URL/text for quick verification.
  - Allow analysts to **approve, edit, or reject** the automated AI outputs.
  - Highlight status changes (e.g., "Planned" to "Under Construction") and capacity updates visually.

### Feature 3: Export & Mapping Engine
- **Requirement:** Map verified data strictly to the client-provided spreadsheet template consisting of **33 specific data points**.
- **Action:** A "Download/Export to Template" button that generates the finalized spreadsheet.

---

## 3. Tech Stack Suggestions (For Speed & Scalability)
* **Frontend/Dashboard:** Streamlit or Pillar/Gradio (for rapid Python-based UI prototyping) or React (if building a full UI).
* **AI/LLM Layer:** Gemini API (e.g., Gemini 1.5 Pro) utilizing **Structured Outputs (JSON Mode)** to ensure data maps perfectly to the 33 required schema attributes.
* **Backend & Data:** Python (Pandas/OpenPyXL for spreadsheet manipulation), FastAPI (optional, for routing).

---

## 4. Specific Instructions for the Demo Build

### Step 1: Mock Data & Schema Setup
- Create a mock template mimicking the client's **33 data points** (including: Plant Name, Location/Region, Status [Active/Planned/Under Construction], Capacity, Operational Year, Source URL).
- Generate a sample dataset of 3–5 Brazilian ethanol plants with messy/unstructured text to test the AI's extraction capabilities.

### Step 2: Develop the Streamlit/UI Prototype
- **Screen 1: Ingestion Feed** – Show raw text/news articles on the left, and the AI’s extracted 33 data points in an editable form on the right.
- **Screen 2: Master Inventory** – A tabular view tracking historical changes from 2003 to 2026, specifically flagging plant status changes and capacity updates (critical for long-term operational planning).

### Step 3: Implement the Export Feature
- Ensure that clicking "Export" populates the exact columns required by the client template without breaking any formatting.

---

## 5. Deliverables
1. **Source Code:** Fully documented GitHub repository.
2. **Live Demo UI:** A working Streamlit/Web dashboard showcasing the end-to-end flow (Raw Text -> AI Extraction -> Analyst Edit -> Spreadsheet Export).
3. **Sample Output:** A completed client template spreadsheet containing the verified demo data.
