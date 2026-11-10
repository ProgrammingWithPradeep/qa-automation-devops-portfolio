# IoT QA Automation DEVOPS Portfolio

This repository showcases a QA automation framework built for a Smart Home IoT Dashboard demo site. It includes UI, API, and CI/CD testing using modern tools and best practices.

## 👤 Author

**Supradeep Peyyeti**  
Senior Software Engineer ( Automation QA )
🔗 [LinkedIn Profile](https://www.linkedin.com/in/supradeep-peyyeti-7577845)


## 🔗 Demo Site

[Smart Hub IoT Dashboard](https://demo.smart-hub.io/) — used as the target application for automation testing.

---

## 🧰 Tech Stack

### 🧪 Test Automation
- **Playwright (TypeScript)** — UI automation for modern web apps
- **Selenium (Java)** — Cross-browser testing
- **Python + Requests** — REST API validation

### ⚙️ CI/CD Integration
- **GitHub Actions** — Automated test execution on code push
- **Jenkins (optional)** — For enterprise CI/CD pipelines

### 📦 Supporting Tools
- **Node.js & npm** — Dependency management for Playwright
- **ChromeDriver** — WebDriver for Selenium
- **pytest** — Python test runner
- **CSV files** — Sample sensor data for test validation

---

## 📁 Project Structure
iot-qa-automation-portfolio/
│
├── README.md
├── playwright-tests/        # UI tests using Playwright
│   └── test-dashboard.spec.ts
├── selenium-tests/          # UI tests using Selenium
│   └── test-login.java
├── api-tests/               # API tests using Python
│   └── test-sensors.py
├── test-data/               # Sample sensor data
│   └── sample-sensor-data.csv
├── ci-cd/                   # GitHub Actions workflow
│   └── GitHub-Actions.yml
└── docs/                    # Test strategy and documentation
    └── test-strategy.md

---

## 🚀 How to Run Tests

### Playwright
```bash
npm install
npx playwright test
```

### Storefront pytest workflows
Install pytest, then run the workflow tests from the repository root:
```bash
python -m pip install pytest
python -m pytest
```
The pytest fixture starts the standard-library storefront server on an ephemeral local port and shuts it down after the tests. These tests cover page routes, catalog data, sign-in, and checkout behavior without requiring a separately running server.

### Python Playwright end-to-end tests
These tests drive a real Chromium browser through the login, catalog, basket, payment, and order-confirmation workflows. Start the storefront in one terminal:
```bash
python app/server.py
```
In a second terminal, install the browser-test dependencies and Chromium, then run the suite from the repository root:
```bash
python -m pip install -r playwright-python/requirements.txt
python -m playwright install chromium
python -m pytest -c playwright-python/pytest.ini playwright-python/tests -v
```
Each run saves a standalone HTML report to `playwright-python/report.html` and a JUnit XML report to `playwright-python/report.xml` (both files are replaced on the next run). Open the HTML file in a browser to review the results. The app must be reachable at `http://127.0.0.1:8000`. To use another address, set `STOREFRONT_BASE_URL` before running pytest (for example, in PowerShell: `$env:STOREFRONT_BASE_URL = 'http://localhost:8000'`). The existing server-workflow tests remain separate and continue to run with `python -m pytest`.

### GitHub Actions
The `main.yml` workflow runs each suite in a container on GitHub Actions, using runtime-specific images: TypeScript Playwright uses the official Playwright image; pytest and API tests use Python images; Python Playwright uses a Python image with Chromium and its system dependencies installed; Serenity/Selenium uses a Maven and Java image with Chromium and ChromeDriver installed. The Python Playwright job starts the storefront in the same container before running its browser tests. Its CI-only Serenity configuration enables headless Chromium without changing local browser settings.

The existing TypeScript Playwright report upload and commit steps are preserved. Reports from the other suites are uploaded as artifacts and can be downloaded from the workflow run under **Actions → Artifacts**.

### Selenium
Run via your IDE (e.g., IntelliJ or Eclipse) with ChromeDriver configured.

### API Tests
```bash
pip install requests
python api-tests/test-sensors.py
```

## 📄 Documentation

- `docs/test-strategy.md` — Describes test scope, approach, and tools used
- `ci-cd/GitHub-Actions.yml` — CI pipeline for Playwright tests
- `test-data/sample-sensor-data.csv` — Sample sensor readings for validation
- `README.md` — Project overview, tech stack, and instructions
