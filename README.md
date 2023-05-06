[Dall-E Generated Logo](https://github.com/huh-sters/traffcap/blob/master/spa/src/assets/traffcap_logo.png?raw=true)

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


