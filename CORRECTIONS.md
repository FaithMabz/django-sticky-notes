# Part 2 corrections

- Added invalid create/update, empty POST, missing update/delete, empty list, ordering and rendered-content tests.
- Added short test docstrings.
- Fixed form binding on empty POST requests.
- Added model-level newest-first ordering and migration 0002.
- Standardized template indentation and action button styling; added POST-only delete confirmation to list/detail pages.
- Removed unused MAILERS setting and corrected README submission documents.
- Removed generated Python caches and local SQLite database from submission ZIP.

## Before resubmission

1. Install dependencies with `python -m pip install -r requirements.txt`.
2. Run `python manage.py migrate`, `python manage.py test`, `python manage.py check` and `python manage.py runserver`.
3. Manually check create, view, edit, delete, invalid forms, empty list, and confirmation cancellation.
4. Visually inspect all three diagrams against the assignment and Part 1 feedback when available.
5. Confirm `sticky_github.txt` points to the public repository containing this submitted code.

Tests were not executed in the preparation environment because Django was unavailable.
