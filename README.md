# Django Sticky Notes Application

A Django Model–View–Template (MVT) application for creating, viewing, editing, and deleting notes. Each note stores a title, content, and creation timestamp.

## Features

- List notes with newest first; view individual notes
- Create and edit notes using a Django ModelForm
- Delete notes with a POST request, not a GET request
- Responsive HTML templates and CSS styling
- SQLite database and Django migrations

## Local setup

Use a supported Python version for the Django version in `requirements.txt`. From the folder containing `manage.py`:

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. Use the links and forms to create, read, edit, and delete notes. Run tests with `python manage.py test` and configuration checks with `python manage.py check`.

## Configuration

`DJANGO_SECRET_KEY` may be set as an environment variable. The project contains a **development-only** fallback, not suitable for production. `DEBUG=True` is also intended for local development only. Static CSS source files live under `notes/static/`; `collectstatic` copies them to `staticfiles/`. Do not commit `.env`, `venv/`, local databases, or collected static files.

## Submission documents

- `diagrams/use_case.png`, `diagrams/sequence.png`, `diagrams/class.png`
- `sticky_github.txt` with the public GitHub repository link
- Unit tests in `notes/tests.py`

## Architecture

The `Note` model stores note data, `NoteForm` validates inputs, `notes/views.py` handles HTTP requests and CRUD operations, URL routes dispatch requests, and HTML templates display the interface.
