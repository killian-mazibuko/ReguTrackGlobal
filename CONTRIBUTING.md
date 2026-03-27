# Contributing to ReguTrack Global

Thank you for your interest in contributing to ReguTrack Global! As we scale our 2026 regulatory intelligence across the UK, USA, South Africa, Nigeria, and Kenya, we welcome contributions that improve our RAG accuracy, security, and multi-jurisdictional logic.

---

## 🚦 Quick Links

- [Submitting a Pull Request (PR)](#submitting-a-pull-request-pr)
- [Development Environment Setup](#setting-up-the-development-environment)
- [Testing (Unit & E2E)](#testing)
- [Adding New Regional Indices](#adding-new-regional-indices)

---

## 🤝 Contributor Guidelines

### Submitting a Pull Request (PR)
1. **Fork the Repo:** Create a new feature branch for your changes.
2. **Standardize:** Ensure your code follows the [Code Style](#code-style) guidelines (Ruff/Black).
3. **Verify:** Run the test suite to ensure no regressions in the RAG retrieval logic.
4. **Document:** If you are adding a new country or regulation, update the `README.md` and `ARCHITECTURE.md`.
5. **Describe:** In your PR, explain how your change impacts the 2026 compliance landscape for the targeted region.

---

## 💻 Setting Up the Development Environment

1. **Python Dependencies:**
   ```shell
   python -m pip install -r requirements-dev.txt
   pre-commit install