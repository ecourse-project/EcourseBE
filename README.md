# ECourse

## Prerequisites

-   Python 3.10.4
-   Postgres 14
-   venv (virtual environment)

## Setup

-   Create venv in backend directory:
    -   "python -m venv venv"
-   Activate venv:
    -   cd venv/scripts
    -   activate
-   Install library:
    -   "pip install -r requirements.txt"
-   Edit database information in
    -   "backend/ecourse/ecourse/settings/"
    -   Change "NAME" and "PASSWORD" in "DATABASES" variable
-   Migrate:
    -   "python manage.py migrate"
-   Runserver:

    -   In "ecourse" directory, run "python manage.py runserver {port}"

-   Create venv in backend directory:
    -   "python -m venv venv"
-   Activate venv:
    -   cd venv/scripts
    -   activate
-   Install library:
    -   "pip install -r requirements.txt"
-   Edit database information in
    -   "backend/ecourse/ecourse/settings/"
    -   Change "NAME" and "PASSWORD" in "DATABASES" variable
-   Migrate:
    -   "python manage.py migrate"
-   Runserver:
    -   "python manage.py runserver {port}"
