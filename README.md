# Beat API

A backend service for cataloging music beats and sharing them safely.

## About

I produce beats in FL Studio, and managing them is a mess: files with unhelpful names, BPM kept in my head, and no safe way to share a track without handing over the full file.

Beat API solves that. It stores each beat with its metadata, lets you search by genre, mood and BPM range, and automatically generates a 30-second preview when a file is uploaded — so beats can be shared without giving away the original.

This is a backend project. The API is explored through FastAPI's auto-generated docs page; a minimal HTML page is included as a demo client.

## Features

- Store beats with name, creator, BPM, genre and mood
- Search with combinable filters: genre, mood, BPM range
- Upload audio files (type and size are validated)
- Automatic 30-second preview generated with ffmpeg on upload
- Separate endpoints for the preview and the original file
- Internal fields (file paths on disk) never leave the API
- 13 tests covering all endpoints

## Tech stack

- **Python 3.14**
- **FastAPI** — web framework with automatic interactive docs
- **SQLModel** — ORM over SQLite
- **ffmpeg** — audio trimming, called through `subprocess`
- **pytest** — tests, with an in-memory database
- **Git / GitHub**

## API

| Method | Path | What it does |
|---|---|---|
| GET | `/beats` | All beats; optional `genre`, `mood`, `min_bpm`, `max_bpm` |
| GET | `/beats/count` | Total number of beats |
| GET | `/beats/genres` | All genres, no duplicates |
| GET | `/beats/{id}` | One beat, 404 if missing |
| POST | `/beats` | Create a beat, returns it with its new id |
| DELETE | `/beats/{id}` | Delete a beat |
| POST | `/beats/{id}/upload` | Upload an audio file, preview is generated |
| GET | `/beats/{id}/preview` | 30-second preview |
| GET | `/beats/{id}/download` | Original file |

Interactive docs: `http://127.0.0.1:8000/docs`

## Design notes

**Separate models and schemas.** The database model `Beat` holds `file_path` and `preview_path`, but the response schema `BeatRead` does not. Internal paths never reach the client. The create schema `BeatCreate` has no `id` either, so a client cannot set one — the database assigns it.

**Dependency injection for the database session.** Endpoints receive a session instead of opening one. Tests swap it for an in-memory database with `app.dependency_overrides`, and no endpoint code changes.

**Unique filenames.** Uploaded files are renamed with a UUID, so two beats with the same filename do not overwrite each other. The preview keeps the same name in a different folder, which makes the pair easy to match by eye.

## Running locally

Requires Python 3.11+ and ffmpeg (`brew install ffmpeg` on macOS).

```bash
cd backend
```

First time only — create a virtual environment.

**macOS / Linux**
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

Fill the database with sample beats:

```bash
python -m app.seed
```

Run the server:

```bash
python -m uvicorn app.main:app --reload
```

Then open:
- `http://127.0.0.1:8000/docs` — interactive API docs
- `frontend/index.html` — demo page (open the file in a browser)

## Tests

```bash
cd backend
pytest
```

Tests run against a separate in-memory database, so they never touch real data.

## Project structure

```
backend/
  app/
    main.py        app setup, routers
    models.py      database models
    schemas.py     request/response schemas
    database.py    engine, session dependency
    audio.py       preview generation
    seed.py        sample data
    routers/
      beats.py     all endpoints
  tests/
    conftest.py    test database setup
    test_beats.py  13 tests
  storage/
    originals/     uploaded files
    previews/      generated previews
frontend/
  index.html       demo page
```

## What's next

- **Authentication** — so only the owner can download the original; everyone else gets the preview
- **Deployment** — a live URL instead of localhost
- **Similar beats** — compare audio features with librosa and recommend by sound
- **Migrations** — Alembic, so the schema can change without dropping the database
- **Pagination** — `/beats` currently returns everything at once

## Status

Built October–November 2026 as a sophomore project at ASU, through the SoDA mentorship program.
