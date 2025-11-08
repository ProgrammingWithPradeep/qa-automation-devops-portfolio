# IoT QA Automation Portfolio

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

Selenium
Run via your IDE (e.g., IntelliJ or Eclipse) with ChromeDriver configured.

API Tests
pip install requests
python api-tests/test-sensors.py

## 📄 Documentation

- `docs/test-strategy.md` — Describes test scope, approach, and tools used
- `ci-cd/GitHub-Actions.yml` — CI pipeline for Playwright tests
- `test-data/sample-sensor-data.csv` — Sample sensor readings for validation
- `README.md` — Project overview, tech stack, and instructions



