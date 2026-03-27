# 🤖 Instructions for Coding Agents: ReguTrack Global

This file contains the "Source of Truth" for AI agents and developers working on the ReguTrack Global platform. It covers the 2026 multi-jurisdictional architecture, ingestion workflows, and standardized patterns for adding new regulatory logic.

## 🏗 Overall Code Layout

* **`app/`**: Core application logic.
    * **`app/backend/`**: Python (Quart) backend.
        * **`approaches/`**: The RAG engine. `chatreadretrieveread.py` is the primary logic for multi-turn chat and query rewriting.
        * **`prompts/`**: Jinja2 templates for system messages. These must maintain "Strict-Grounding" for 2026 legal data.
        * **`prepdocslib/`**: The ingestion library. Includes specialized parsers for 2026 tax tables and legal PDFs.
        * **`app.py`**: Main entry point and API route definitions.
    * **`app/frontend/`**: React/TypeScript frontend (Vite).
        * **`src/api/`**: Client-side API definitions and models.
        * **`src/locales/`**: Internationalization (i18n) files for global regional support.
* **`infra/`**: Bicep templates for Azure resource provisioning (Keyless/RBAC focused).
* **`data/`**: Regulatory source PDFs organized by country (e.g., `/data/nigeria`, `/data/uk`).
* **`tests/`**: Pytest suite including E2E (Playwright), integration, and unit tests.

---

## 🌍 Adding New Jurisdictional Data

When adding new 2026 regulatory documents:
1.  Place PDFs in the country-specific subfolder: `data/[country_name]`.
2.  Run the ingestion script with the `--tenant` metadata flag to ensure correct routing in the UI: