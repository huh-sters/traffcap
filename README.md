![Dall-E Generated Logo](https://github.com/huh-sters/traffcap/blob/master/spa/src/assets/traffcap_logo.png?raw=true)

# traffcap

A RequestBin like application using FastAPI.

The goal of this tools is for it to be used in end to end testing where webhooks need testing.

* Provide endpoint management
* Endpoints are in the format `/r/<unique endpoint ID>`
* Allow endpoint prefix to be configurable
* All HTTP verbs are captured
* All headers are recorded
* All content is captured
* Web sockets are captured
* Inbound requests are queued for processing
* A single page application can control the application
* A full API can control all aspects of the application
* A reporting API can be used to monitor the application
* Allow the frontend UI to be disabled
* All request responses are customisable
* Read up on SQLAlchemy ORM with FastAPI: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-database-models
* Allow multiprocessing Managers to talk between Gunicorn managed processes
* Allow Redis/RabbitMQ to talk between Gunicorn managed processes and clusters of servers behind load balancers
* Allow CORS configuration
* Allow multiple database types (SQLite, MySQL, Postres)


# Running This Thing

At the moment, you'll need the following to run it:

* Python 3.11 or greater ([pyenv](https://github.com/pyenv/pyenv#automatic-installer) is a good way to manage versions)
* [PDM installed](https://pdm.fming.dev/latest/#installation)
* Node v12 or greater ([nvm](https://github.com/nvm-sh/nvm#installing-and-updating) is a good way to manage versions)
* NPM (If you installed Node, you should have a version of NPM already)

## Installing Python project dependencies

After cloning the repository to a directory somewhere, change to the repository directory and run the following to install dependencies in a virtual environment:

`pdm install`

Then, once the dependencies are done the server part is ready to rock. But out of the box, there's no UI to configure anything, so you'll need the next step.

## Building the Frontend Single Page Application (SPA)

From the repository directory, change to the `spa` directory and run the following command to build the SPA:

`npm run build`

It should display messages about Quasar building and if all is good you'll see lots of green and another prompt. At this point the SPA is built and ready to use.

## Run the Server and Visit the Site

From the repository root, issue the following command to start the server:

`pdm run server`

You'll get a bunch of messages and the server will be up and running. Now, you can visit:

[The frontend SPA](http://localhost:8000) (Watch the port number here, it may be different to the one you have, but 8000 is probably right, it'll say the port number in the terminal messages)

That's it!

## What Does It Run?

When you invoke `pdm run server`, it starts [Gunicorn](https://gunicorn.org/) with 4 [Uvicorn](https://www.uvicorn.org/) workers.

It then binds everything to `0.0.0.0` on port `8000`

The command it runs is:

`gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000`

You can change the number of Uvicorn workers here if you like. If you don't want to run lots of different processes, you can use Uvicorn directly:

`uvicorn main:app --host 0.0.0.0 --port 8000`

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
                "main:app",
                "--workers",
                "4",
                "--worker-class",
                "uvicorn.workers.UvicornWorker",
                "--bind",
                "0.0.0.0:8000"
            ]
        },
        {
            "name": "Uvicorn worker",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "main:app"
            ],
            "jinja": true
        }
    ]
}
```

Now you can set breakpoints and run this directly from VSCode.

## How Do I Get The Python Interpreter Path For The Virtual Environment?

This project uses PDM for managing dependencies and virtual environments. You can issue this command to list the virtual environment path for the project:

`pdm venv list`

You'll get a list of environments and the Python versions that they are for. The Python interpreter is in the `bin` directory in each environment. So for example, if you see the following:

```
~/python_projects/traffcap> pdm venv list
Virtualenvs created with this project:

*  3.11: /home/chris/.pdm_venv/traffcap-kO3U-3Zd-3.11
```

Then the interpreter for that version of Python 3.11 is:

`/home/chris/.pdm_venv/traffcap-kO3U-3Zd-3.11/bin/python`

If you wanted to, you can add the default Python interpreter in VSCode by adding the following to your projects `settings.json`:

```
{
    "python.defaultInterpreterPath": "/home/chris/.pdm_venv/traffcap-kO3U-3Zd-3.11/bin/python",
    ...
}
```

This will make all terminal sessions in VSCode start in that virtual environment and the debugger will use this version as well.

# Concepts

## Endpoints

These are the URL's that are used by your application to talk to Traffcap. They are in the format of a short prefix followed by a longer identifier, like this:

`/r/123abcdefg890`

So say your server is hosted at a specific address like `https://fipo.co` then the webhook URL would be:

`https://fipo.co/r/123abcdefg890`

Now, by default, the prefix for the URL's is `r`, but this can be changed to something else if you like in the configuration. The part after the prefix is known as the *endpoint code*.

When your application calls this URL by any HTTP verb, like GET or POST, Traffcap will record everything about the interation and then send back a response of some kind.

### Endpoint Code Matching

By default, Traffcap will accept any endpoint code and store the interaction. Doesn't matter how long or short the code is, it'll record the data.

You can tell Traffcap to interact in specific ways by specifying a match to certain endpoint codes.

For example, if you see an endpoint code that starts with `123...` you can respond to the request with a JSON API payload with specific values that your application might need to proceed.

These matches are performed using [Regular Expressions](https://www.regular-expressions.info/) in the endpoint matching section.

You could match an endpoint code exactly, or just parts of the endpoint.
