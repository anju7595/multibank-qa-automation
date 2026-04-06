MultiBank Group - QA Automation Framework
A high-performance, scalable E2E automation suite built with Python and Playwright. This framework implements a Page Object Model (POM) and Data-Driven Testing (DDT) to validate the MultiBank Group platform across multiple browser engines and regional locales.

🏗️ Architectural Overview
This project is designed with modularity and maintainability as core principles:

Page Object Model (POM): Separation of UI locators from test logic to minimize maintenance overhead.

Data-Driven Design: Test cases (Navigation, Content) are driven by external JSON configurations, allowing for suite expansion without code changes.

Resilient Interaction Layer: Custom handlers for dynamic UI elements, including cookie banners, localized redirects, and cross-domain tab handling ($MBG Token site).

CI/CD Ready: Integrated with GitHub Actions for automated regression on every push.

🛠️ Tech Stack
Language: Python 3.11+

Framework: Pytest

Automation: Playwright (Sync API)

Reporting: Pytest-HTML & Automated Screenshots

CI/CD: GitHub Actions

📂 Project Structure
Plaintext
multibank-qa-automation/
├── .github/workflows/   # CI/CD Pipeline (GitHub Actions)
├── data/                # JSON Test Data (DDT)
├── pages/               # Page Object Classes (Locators & Actions)
├── tests/               # Functional Test Suites
├── utils/               # Config Constants & Data Loaders
├── reports/             # Test execution results & screenshots
├── conftest.py          # Global fixtures & Failure hooks
├── pytest.ini           # Framework configuration
└── requirements.txt     # Dependency management
⚙️ Quick Start
1. Prerequisites
Ensure you have Python 3.11+ installed. It is recommended to use a virtual environment.

2. Installation
Bash
# Clone the repository
git clone https://github.com/anju7595/multibank-qa-automation.git
cd multibank-qa-automation

# Setup Virtual Environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install Dependencies
pip install -r requirements.txt

# Install Playwright Browsers
playwright install
3. Execution
Bash
# Run all tests (Headless)
pytest

# Run a specific suite in Headed mode
pytest tests/test_navigation.py --headed

# Run in parallel across 4 CPU cores
pytest -n 4
📊 Reporting & Debugging
HTML Reports: Generated after every run at reports/report.html.

Failure Screenshots: On any test failure, a screenshot is automatically captured and saved to the reports/ directory for rapid debugging.

Artifacts: In the GitHub Actions tab, the full HTML report is uploaded as a downloadable artifact for every cloud execution.

Author: Anju George – Senior QA Automation Engineer