# AI Pipeline Doctor

<p align="center">
  <img src="https://raw.githubusercontent.com/oozan/ai-pipeline-doctor/main/assets/ai-pipeline-doctor-banner.png" width="100%" />
</p>

**AI Pipeline Doctor** is an intelligent developer tool designed to automatically analyze CI/CD logs, detect the root cause of pipeline failures, and provide actionable suggestions to fix them. It saves developers hours of manual debugging by understanding logs from GitHub Actions, GitLab CI, CircleCI, and generic terminals.

---

## Why This Exists

Modern development teams rely heavily on CI/CD pipelines. When they break, developers waste **massive time** figuring out:

- Which part of the pipeline failed?
- Was it dependency-related?
- Was it a Docker build issue?
- Was it a test failure?
- Was it authentication or permission-related?
- What command actually failed?

CI logs are often long, noisy, and cryptic.  
**AI Pipeline Doctor automates all that pain away.**

---

## What It Does

Given a pipeline log (raw text), AI Pipeline Doctor:

1. Identifies the CI provider  
   ✔ GitHub Actions  
   ✔ GitLab CI  
   ✔ Generic pipelines

2. Extracts the failure point  
   ✔ Failed command  
   ✔ Last error line  
   ✔ Root cause

3. Classifies the error type

   - `dependency_error`
   - `test_failure`
   - `docker_build_error`
   - `auth_error`
   - `unknown`

4. Summarizes the issue  
   Clear human-readable explanation

5. Suggests fixes  
   Practical, specific, immediately usable

6. Provides a confidence score

---

### Quick example

````bash
cd backend
python3 cli_analyze.py --file sample_github.log --provider github


## Example Output

```json
{
  "provider": "github_actions",
  "error_category": "dependency_error",
  "primary_error": "ModuleNotFoundError: No module named 'requests'",
  "failed_command": "pip install -r requirements.txt",
  "summary": "The pipeline failed due to a missing or incompatible dependency.",
  "suggested_fixes": [
    "Add 'requests' to your requirements file and reinstall dependencies.",
    "Ensure the dependency installation step runs before executing your script."
  ],
  "confidence": 0.9
}
````

---

## Project Structure

```
ai-pipeline-doctor/
│
├── backend/
│   ├── app.py                    # FastAPI app
│   ├── core/
│   │   ├── models.py             # Pydantic models
│   │   └── analyzer.py           # Main logic
│   ├── parsers/
│   │   ├── base.py               # Base parser class
│   │   ├── github_actions.py     # GitHub-specific parser
│   │   └── generic.py            # Fallback parser
│   ├── rules/
│   │   └── patterns.py           # Regex rules & suggestions
│   ├── tests/
│   │   ├── test_analyzer.py      # Analyzer tests
│   │   └── fixtures/             # Example log files
│   │       ├── github_dependency_error.log
│   │       ├── github_test_failure.log
│   │       └── github_docker_error.log
│   └── requirements.txt
│
└── README.md
```

---

## Installation

```bash
cd ai-pipeline-doctor/backend
pip install -r requirements.txt
```

---

## Running the API

Start the server:

```bash
uvicorn app:app --reload
```

Open interactive docs:

http://127.0.0.1:8000/docs

---

## CLI Usage

Analyze a log file:

```bash
python cli_analyze.py --file mylog.txt
```

Or pipe output:

```bash
cat mylog.txt | python cli_analyze.py
```

---

## 🧪 Testing

Run unit tests:

```bash
pytest
```

---

## 🔮 Future Enhancements

- AI model to improve classification (transformer-based)
- GitHub App integration to auto-comment on PR failures
- Web UI (Next.js) for drag-and-drop log analysis
- Multi-provider advanced parsers (Jenkins, CircleCI)
- Automatic patch generation (PR-ready fixes)

---

## ❤️ Contributing

PRs are welcome.
Open an issue with:

- log samples
- new error categories
- feature ideas

---

## 📜 License

MIT License

---

## 👑 Author

**Ozan Özayrancı**

- Hugging Face: https://huggingface.co/oozan
- GitHub: https://github.com/oozan

---

AI Pipeline Doctor is built to save developers from CI hell
Let's make debugging painless 🔥
