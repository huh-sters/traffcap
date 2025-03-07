![build workflow](https://github.com/huh-sters/traffcap/actions/workflows/build.yml/badge.svg)
![licence](https://img.shields.io/github/license/huh-sters/traffcap.svg)
![uv-managed](https://img.shields.io/badge/uv-managed-blueviolet)

![Logo](https://github.com/huh-sters/traffcap/blob/master/src/traffcap/spa/src/assets/traffcap_logo.png?raw=true)

# What Is Currently Working?

* Request capturing. It records all requests with any method to an endpoint
* Supports SQLite and MySQL
* Basic GUI which display the inbound requests in realtime using websockets
* API to fetch all inbound requests in a big list
* Settings for configuring server URLs and protocols
* IPC between inbound requests and websockets on a single container works

**As it stands, it performs enough to be able to integrate with a CI/CD stack with little work:**

* An end-to-end test can send traffic to `/r/random-endpoint` and it will record the data
* Calling `/traffic` will return all the traffic sent including headers and the body

This can at least be used to verify the data sent to a webhook

# traffcap

A RequestBin like application using FastAPI.

The goal of this tools is for it to be used in end to end testing where webhooks need testing.

* Provide endpoint rule matching management
* Endpoints are in the format `/r/<unique endpoint ID>` (done)
* Allow endpoint prefix to be configurable (done)
* All HTTP methods are captured (done)
* All headers are recorded (done)
* All content is captured (done)
* Web sockets are captured
* A single page application can control the application (working)
* A full API can control all aspects of the application
* A reporting API can be used to monitor the application
* Allow the frontend UI to be disabled
* All request responses are customisable
* Allow multiprocessing Managers to talk between Gunicorn managed processes (done)
* Allow Redis/RabbitMQ to talk between Gunicorn managed processes and clusters of servers behind load balancers
* Allow CORS configuration
* Allow multiple database types (SQLite (done), MySQL (done), Postres, MSSQL, Oracle)
* Provide a websocket connection

# Running

## Docker

This application is available as an image [here](https://hub.docker.com/r/centurix/traffcap)

To use with `docker-compose.yaml`

```
---
version: "2.1"
services:
  radarr:
    image: centurix/traffcap:latest
    container_name: traffcap
    ports:
      - 9696:9696
    restart: unless-stopped
```

## From PyPi

This is available from PyPi as a package. You can install the package with:

`pip install traffcap`

And once it has installed, you can run:

`traffcap`

And a basic server will start. Typing `traffcap --help` will list the available options.

## From source

At the moment, you'll need the following to run it:

* Python 3.9 or greater ([pyenv](https://github.com/pyenv/pyenv#automatic-installer) is a good way to manage versions)
* [uv installed](https://github.com/astral-sh/uv)
* Node v12 or greater ([nvm](https://github.com/nvm-sh/nvm#installing-and-updating) is a good way to manage versions)
* NPM (If you installed Node, you should have a version of NPM already)

## Installing Python project dependencies

After cloning the repository to a directory somewhere, change to the repository directory and run the following to install dependencies in a virtual environment:

`uv sync`

Then, once the dependencies are done the server part is ready to rock. But out of the box, there's no UI to configure anything, so you'll need the next step.

## Building the Frontend Single Page Application (SPA)

From the repository directory, change to the `spa` directory and run the following command to build the SPA:

`npm run build`

It should display messages about Quasar building and if all is good you'll see lots of green and another prompt. At this point the SPA is built and ready to use.

## Run the Server and Visit the Site

From the repository root, issue the following command to start the server:

`uv run ./server`

You'll get a bunch of messages and the server will be up and running. Now, you can visit:

[The frontend SPA](http://localhost:9669) (Watch the port number here, it may be different to the one you have, but 9669 is probably right, it'll say the port number in the terminal messages)

That's it!

## What Does It Run?

When you invoke `uv run ./server`, it starts [Gunicorn](https://gunicorn.org/) with 4 [Uvicorn](https://www.uvicorn.org/) workers.

It then binds everything to `0.0.0.0` on port `9669`

The command it runs is:

`gunicorn server:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:9669`

You can change the number of Uvicorn workers here if you like. If you don't want to run lots of different processes, you can use Uvicorn directly:

`uvicorn server:app --host 0.0.0.0 --port 9669`

This will run a single Uvicorn worker bound to the same network interface and port number.

## How Do I Setup VSCode To Debug This Stuff?

You can setup a launch configuration with the following:

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Gunicorn with Uvicorn workers",
            "type": "python",
            "request": "launch",
            "module": "gunicorn",
            "args": [
                "server:app",
                "--workers",
                "4",
                "--worker-class",
                "uvicorn.workers.UvicornWorker",
                "--bind",
                "0.0.0.0:9669"
            ]
        },
        {
            "name": "Uvicorn worker",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "server:app"
            ],
            "jinja": true
        }
    ]
}
```

Now you can set breakpoints and run this directly from VSCode.

## How Do I Get The Python Interpreter Path For The Virtual Environment?

This project uses [uv] for managing dependencies and virtual environments. You can create virtual environments with the following command:

`uv venv .venv`

You'll get details of the environment just created. The Python interpreter is in the `bin` directory in the environment. You see the following:

```
~/python_projects/traffcap> uv venv .venv
Using CPython 3.13.2
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
```

Then the interpreter for that version of Python 3.9 is:

`.venv/bin/python`

If you wanted to, you can add the default Python interpreter in VSCode by adding the following to your projects `settings.json`:

```
{
    "python.defaultInterpreterPath": ".venv/bin/python",
    ...
}
```

This will make all terminal sessions in VSCode start in that virtual environment and the debugger will use this version as well.

### Why Python 3.9?

As of the writing of this document, 3.9 will be the minimum supported version with the End of Life scheduled to be in June 2023. At which point, this repository will be upgrade to support the next in line for EOL, Python 3.10

We support the minimum non-EOL Python to provide compatibility with your environment. Integrations can be difficult at the best of times, especially
when your organisation can only accept specific versions of applications and tools. We will work on the assumption that organisations *should* at least
adhere to the minimum non-EOL version of Python.

### Contributing

The codebase aims to comply to PEP8, with the only exception on line lengths being a maximum of 119 characters. This is reflected in the `ruff` configuration within the `pyproject.toml` file.

# Concepts

### Endpoint Codes

These are codes used in the URL's that are used by your application to talk to Traffcap. They are in the format of a short prefix followed by a longer endpoint code, like this:

`/r/123abcdefg890`

In this case, the endpoint code is `123abcdefg890`.

So say your server is hosted at a specific address like `https://fipo.co` then the webhook URL would be:

`https://fipo.co/r/123abcdefg890`

By default, the prefix for the URL's is `r`, but this can be changed to something else if you like in the configuration.

When your application calls this URL by any HTTP verb, like GET or POST, Traffcap will record everything about the interation and then send back a response of some kind.

### Endpoint Code Matching Rules

By default, Traffcap will accept any endpoint code and store the interaction. Doesn't matter how long or short the code is, it'll record the data.

You can tell Traffcap to interact in specific ways by specifying a matching rule to certain endpoint codes.

For example, if you see an endpoint code that starts with `123...` you can respond to the request with a JSON API payload with specific values that your application might need to proceed.

These matches are performed using [Regular Expressions](https://www.regular-expressions.info/) in the endpoint matching section.

You could match an endpoint code exactly, or just parts of the endpoint.

### Responses

By default, Traffcap will send back JSON data as a response to an inbound request. However, it can respond in the following content types:

* JSON (Default)
* XML
* HTML
* CSV/TSV

Need to chose a templating language that will work across all content types listed.

### Open Choice in Database Storage

This application should provide the ability to choose which database you want to use. This list of supported databases is controlled by SQLAlchemy and Alembic. Currently, the DBAPI setting is embedded in the alembic.ini file and also in the Repository class. This must be easily changable.

TODO: Create installation targets for specific database storage

* traffcap[mysql]
* traffcap[sqlite]
* traffcap[mssql]

etc.

### Open Choice in Message Brokers

There is a certain level of messaging that happens between threads, processes and containers (where this application is scaled horizontally). In its simplest form, the application running as a single instance will more likely utilise the multi-processing library (like if gunicorn is used with uvicorn workers). But the application will also use a message broker if required to provide horizontal scaling. Message brokers to support are:

* RabbitMQ
* Redis
* AmazonMQ
* IBM MQ

Is there a framework like SQLAlchemy for message brokers?

### Creating New Alembic Revisions

During development, it is fine to create feature branch revisions using the IDs generated by Alembic. Prior to a tagged release, these migrations are to be grouped together into a revision ID that matches the git tag. This application will be using the Alembic auto generation of migrations:

1. Using the release code, remove the revisions generated by Alembic
2. Empty the database
3. Migrate up using `alembic upgrade head`
4. Run the following command replacing the revision ID with the next release number and add a meaningful description

`alembic revision --autogenerate --rev-id 0.0.1 -m 'Baseline schema'`

OR

`uv run ./baseline_schema`

### ORM Usage and Being Database Agnostic

One of the aims of this project is to be as database agnostic as it could possibly be. Out of the box the project is using SQLAlchemy to bring a certain level of abstraction to Python. Adding specific dialects of SQL into this project would be a last resort.

### Environment Variables

Base configuration of Traffcap is achieved through environment variables:

#### TRAFFCAP_REQUESTS_PREFIX

This is the inbound request path prefix. Defaults to "r"

#### TRAFFCAP_DB_DRIVER

This is the database driver to use. Defaults to "sqlite".

Acceptable values are:

* sqlite
* mysql
* mssql
* postrgresql
* oracle

#### TRAFFCAP_DB_USER

The username used to connect to the database. Not used for SQLite.

#### TRAFFCAP_DB_PASSWORD

The password used to connect to the database. Not used for SQLite.

#### TRAFFCAP_DB_HOST

The hostname for the database server. Not used for SQLite.

#### TRAFFCAP_DB_NAME

The database name. For SQLite, this is the filename. Defaults to 'traffcap.db'.
