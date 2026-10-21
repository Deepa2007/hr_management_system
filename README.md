# HR Management System

A beginner-friendly HR REST API built with Python and FastAPI, with a GitHub Actions CI pipeline.

## Features

- Health endpoint
- Create, list, retrieve, update, and delete employees
- Input validation for email and positive salary
- Duplicate email protection
- Automated tests with pytest
- Ruff linting and Black formatting checks
- GitHub Actions CI on pushes and pull requests

> This learning version uses in-memory storage. Data is reset when the app restarts.

## Requirements

- Python 3.11 or newer
- Git
- A GitHub account for running the CI workflow

## Run locally (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API docs.

## Run checks locally

```powershell
ruff check .
black --check .
pytest -v
```

If Black reports that formatting is needed, run `black .`, then rerun all checks.

## API endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/employees` | Create an employee |
| GET | `/employees` | List employees |
| GET | `/employees/{employee_id}` | Get one employee |
| PUT | `/employees/{employee_id}` | Replace employee details |
| DELETE | `/employees/{employee_id}` | Delete an employee |

Example JSON body:

```json
{
  "name": "Asha Rao",
  "email": "asha@example.com",
  "department": "Engineering",
  "salary": 65000
}
```

## Push to GitHub

Create an empty repository on GitHub named `hr-management-system` (do not initialize it with a README if you already have this project locally). Then run:

```powershell
git init
git add .
git commit -m "Build HR management API and CI pipeline"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/hr-management-system.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. If Git is already initialized or a remote already exists, do not repeat those commands blindly; inspect with `git status` and `git remote -v`.

## How the CI pipeline works

1. A push to `main`/`master` or a pull request targeting those branches triggers the workflow.
2. GitHub checks out the repository.
3. It installs Python 3.12 and project dependencies.
4. Ruff checks for common code issues and import problems.
5. Black verifies that files follow the configured formatting.
6. Pytest runs the automated tests.
7. The workflow passes only when every step succeeds.

No deployment secrets are needed for this CI-only workflow.
