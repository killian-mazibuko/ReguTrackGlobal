# Security Policy: ReguTrack Global

ReguTrack Global is committed to maintaining the highest security standards for multi-jurisdictional regulatory intelligence. Given our focus on the **2026 Fiscal Reforms** in the UK, USA, SA, Nigeria, and Kenya, we prioritize data integrity and the prevention of adversarial "jailbreaking" or data leakage.

## Reporting a Security Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you believe you have discovered a security vulnerability—such as an authentication bypass, data leakage between country indices, or a prompt injection that bypasses our grounding filters—please report it via the following channels:

* **Primary:** Email [security@regutrack.global](mailto:security@regutrack.global) (Direct to Engineering Lead)
* **Response Time:** You will receive an initial acknowledgment within **24 hours**.

## Our Security Posture

ReguTrack Global is built on a **Zero-Trust Architecture** to meet 2026 international standards:

1. **Identity & Access:** We utilize **Azure Managed Identities** exclusively. No API keys or connection strings are stored in the application code or environment variables.
2. **Data Residency:** Regulatory data is logically partitioned by country code. UK data (GDPR) and Nigeria data (NDPA 2026) are handled within their respective sovereignty boundaries.
3. **AI Grounding:** To prevent "hallucinations" or misinformation, the system uses a **Strict-Grounding Protocol**. The AI is forbidden from answering questions using its general knowledge if a specific 2026 regulatory source is not found in the index.
4. **Encryption:** All data is encrypted at rest via AES-256 and in transit via TLS 1.3.

## Information to Include in Reports

To help us triage your report quickly, please include:
- **Vulnerability Type:** (e.g., Prompt Injection, RBAC Bypass, SSRF)
- **Affected Component:** (e.g., Ingestion Pipeline, Backend API, Search Index)
- **Country Context:** Does this affect a specific regional index (e.g., Nigeria 2026) or the global system?
- **Steps to Reproduce:** Clear, step-by-step instructions or a proof-of-concept.

## Responsible AI Disclosure

We follow the principle of **Coordinated Vulnerability Disclosure**. We ask that you do not disclose any vulnerability publicly until we have had the opportunity to analyze and mitigate the risk, ensuring the safety of global compliance data.

---
*Last Updated: March 2026*