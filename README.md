# Job Tracker

Personal Project 1 for [boot.dev Backend Track](https://www.boot.dev/)

## Goals

**Job Tracker** is an app to track and manage aspects of your job search:

- Jobs: manage jobs postings (details, status, interviews, contacts, notes)
- Interviews: manage interviews (details, contacts, notes)
- Contacts: manage job/interview specific and global (e.g. recruiters)
- Notes: markdown based notes for jobs, interviews, and contacts

The project includes both a JSON API and a web front end.

## Motivation

Build something that helps solve a current problem...centralizing all aspects of job search.

Build a project that leverages HTMX for the frontend while also providing JSON APIs.

## Stack

**[poetry](https://python-poetry.org/)** - Python packaging and dependency management

**[FastAPI](https://fastapi.tiangolo.com/)** - web framework for building APIs with Python

**[SQLAlchemy](https://www.sqlalchemy.org/)** - database toolkit and ORM for Python

**[SQLite](https://www.sqlite.org/index.html)** - SQL database engine

**[HTMX](https://htmx.org/)** - JavaScript library for interactive web development

**[TailwindCSS](https://tailwindcss.com/)** - utility-first CSS framework

**[Development Containers](https://containers.dev/)** - uses container as full-featured development environment (I'm using VSCode with [remote containers extension](https://code.visualstudio.com/docs/devcontainers/containers))

## Usage

Clone the repo

```sh
$ git clone https://github.com/patrickneise/job-tracker.git
```

Open the folder [in container](https://code.visualstudio.com/docs/devcontainers/containers#_quick-start-open-an-existing-folder-in-a-container).

Start the server:

```sh
$ uvicorn app.main:app
```

or with hot reloading:

```sh
$ uvicorn app.main:app --reload
```

The web app will be available at [http://localhost:8000](http://localhost:8000) and the built in Swagger API documentation will be available at [http://localhost:8000/docs](http://localhost:8000/docs)

For frontend development, to get automatic building of TailwindCSS, in a separate terminal window:

```sh
$ tailwindcss -i app/styles/tw.css -o app/static/css/main.css --watch
```

## Project Status

This is very much a WIP.

All JSON API endpoints are available. Currently working on test coverage and ensuring functionality.

Minimal working frontend (this is a backend track after all...)