# 1) Executive Summary
## Problem: What problem are you solving, and for whom?
Whever you have some questions or whenever you feel boring, you can chat with this model. This is for everyone.
## Solution: One paragraph, non–technical overview of your project.
A Docker-packaged web chatbot that runs the 1.1B-parameter TinyLlama model entirely on consumer CPU hardware, which includes both echo testing mode and full LLM chat capabilities.

# 2) System Overview
## Course Concept(s): Name the specific module concept/tool you used. 
using Docker (which runs Linux containers)
navigating filesystems, running commands in terminals
organizing code in repositories in github
understand commit/push workflows
built a complete Docker containerized application
managing environment variables and configuration
understand dependency management (requirements.txt)
working with build pipelines
## Architecture Diagram: Include a PNG in /assets and embed it here.
<img width="2552" height="1308" alt="image" src="https://github.com/user-attachments/assets/7d38d1ce-0783-443a-863d-7b6f8792438a" />

## Data/Models/Services: List sources, sizes, formats, and licenses.
TinyLlama/TinyLlama-1.1B-Chat-v1.0 (2.2GB, Apache 2.0 License)
HuggingFace Transformers 4.35.0
Flask 2.3.2
Docker with Python 3.11-slim base

# 3) How to Run (Local)
## Choose Docker or Apptainer and provide a single command:
Docker
## build
docker build -t myapp:latest .
## run
docker run --rm -p 8080:8080 --env-file .env myapp:latest
## health check (if applicable)
curl http://localhost:8080/health
## apptainer build
apptainer build project.sif project.def
## run (bind your repo if needed)
apptainer run --env-file .env project.sif
## health check (if applicable)
curl http://localhost:8080/health

# 4) Design Decisions
## Why this concept? Alternatives considered and why not chosen.
Because I feel like AI which could communicate with people is really interesting and I want to do something related.
## Tradeoffs: Performance, cost, complexity, maintainability.
Have to find some small chat models which could be ran by our laptops since most of the well-done chat models are huge.
## Security/Privacy: Secrets mgmt, input validation, PII handling.
All model files cached locally and restricted to localhost by default (0.0.0.0:8080)
## Ops: Logs/metrics, scaling considerations, known limitations.
Requires ~4GB RAM during inference and no chat history storage.

# 5) Results & Evaluation
## Screenshots or sample outputs (place assets in /assets).
<img width="2552" height="1308" alt="image" src="https://github.com/user-attachments/assets/f69b5049-9947-44e9-8e0c-e90ddfbedf28" />
## Validation/tests performed and outcomes.
Could say hi and answered back, also answered some fun questions too.

# 6) What’s Next
## Planned improvements, refactors, and stretch features.
Maybe try to find another larger model that could do more things for us.

# 7) Links (Required)
GitHub Repo: https://github.com/AndyXie0411/Final-Project
Public Cloud App (optional): http://localhost:8080/
