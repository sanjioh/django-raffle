# django-raffle

## Prerequisites

- Python 3.8

This software has been developed and tested on macOS 10.15.5 Catalina.

## Installation and execution

This guide assumes you have a working setup of Python 3.8.

- clone this repository and `cd` into it

  ```sh
    git clone https://github.com/sanjioh/django-raffle
    cd django-raffle
  ```

- create a Python virtual environment and activate it (assuming Bash as shell)

  ```sh
    python3.8 -m venv .venv
    source .venv/bin/activate
  ```

- install runtime dependencies

  ```sh
    python -m pip install -r requirements.txt
  ```

- open another terminal, move to the repository root directory and run `docker-compose`

  ```sh
    # in another terminal

    cd django-raffle  # this command depends on where you cloned the repository
    docker-compose up
  ```

- go back to the first terminal and setup the database

  ```sh
    # back to the first terminal

    ./manage.py migrate
    ./manage.py populate
  ```

- run the service

  ```sh
    ./manage.py runserver
  ```

## Admin

The Django admin interface is available at `http://127.0.0.1:8000/admin/`.

A superuser is available with the following credentials:

- username: `admin`
- password: `adminadmin`

## Endpoints

- `/api/v1/play?contest={code}`

## Tests

- follow the installation steps outlined above up and including the database setup

- install test dependencies

  ```sh
    python -m pip install -r requirements-test.txt
  ```

- run the test suite
  ```sh
    python -m pytest
  ```
