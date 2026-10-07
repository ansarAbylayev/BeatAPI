# Beat API

A backend API for managing and sharing music beats.

### Setup

```bash
cd backend
```

If running the project for the first time, create a virtual environment:

**Mac/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Run

```bash
python -m uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

### Tech Stack

Python · FastAPI · SQLite · FFmpeg

