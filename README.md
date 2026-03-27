# ReguTrack Global: Multi-Jurisdictional Regulatory Intelligence (RAG)

**ReguTrack Global** is an enterprise-grade AI solution designed to automate regulatory gap analysis across five key global corridors: **South Africa, UK, USA, Nigeria, and Kenya**. 

By leveraging the **Retrieval-Augmented Generation (RAG)** pattern, ReguTrack Global provides compliance officers and legal teams with cited, grounded, and real-time intelligence on 2026 fiscal reforms and digital mandates.

---

## 🌍 Global Compliance Scope (2026)

ReguTrack Global is specifically engineered to handle the "2026 Regulatory Wave":
* **Nigeria:** Tax Reform Acts 2026 (4% Development Levy, ₦50M SME CIT exemptions).
* **South Africa:** 2026 VAT Reform (New R2.3M registration thresholds).
* **UK:** Finance Act 2026 and the "Making Tax Digital" (MTD) phase-in.
* **USA:** Tax Cuts and Jobs Act (TCJA) permanent transitions.
* **Kenya:** Finance Act 2026 (Significant Economic Presence tax for digital services).

---

## 🛠 Features

* **Multi-Jurisdictional Chat:** Context-aware switching between global regulatory environments using metadata routing.
* **High-Fidelity Citations:** Every answer is grounded in official gazettes with direct links to the source PDF and page number.
* **Hybrid Vector Search:** Combines keyword matching with **1536-dimension embeddings** (`text-embedding-3-small`) for legal nuance.
* **Semantic Re-ranking:** Uses an L3 ranking layer to prioritize the most relevant 2026 legal provisions.
* **Keyless Security:** Built on **Azure Managed Identities** (Zero-Trust) to ensure data sovereignty and compliance with international privacy laws (GDPR, NDPA).

---

## 🏗 Architecture

ReguTrack Global utilizes a modular cloud architecture to ensure scalability across regional indices.

### System Components:
* **App Service:** Python (FastAPI) backend

Handling Multi-Jurisdictional Data
When adding new regulatory data:

Place PDFs in data/[country_name].

Run the ingestion script with the --tenant flag to ensure proper metadata routing:

Bash
python ./app/backend/prepdocs.py --data ./data/nigeria --index idx-regutrack-global --tenant nigeria