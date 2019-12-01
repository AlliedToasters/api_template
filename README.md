# Basic Python Redis Server

Microservice(s) template for python applications. This is a template repository so it is not intended to actually run anything but to be used as a template for building web services.

## uvicorn
This service supports asynchronous calls and is built on [python 3's ASGI server capability](https://buildmedia.readthedocs.org/media/pdf/asgi/latest/asgi.pdf) using [uvicorn](https://www.uvicorn.org/) and built with [fastapi](https://github.com/tiangolo/fastapi). The dockerfile deploys this app on multiple threads with [gunicorn](https://gunicorn.org/).

## Running the service
### In a virtualenv
This provides a faster cycle for development.

Start the fastapi service:
```bash
python3 -m venv venv
venv/bin/pip install -r requirements-dev.txt
venv/bin/uvicorn app.main:app --port 5000 --reload
```
The `--reload` flag will cause changes to the application to update in the server in real-time.
In a separate process, try sending a request:
```
curl "http://localhost:5000/some_path" -X POST -d @example-request.json
```

## Unit Tests
This service uses redis caching. Unit tests can be run without redis but will throw warnings.

To test redis integration, you may start a redis server locally and run on the default port 6379. <br><br>

After setting up the virtualenv in the step above, you can run the unit tests:
```
venv/bin/python -m pytest
```

To run the functional tests, start up a server on port 5000 (as above) and run:
```
BASE_URL='http://localhost:5000' venv/bin/python -m pytest functional_tests
```

## testing with docker
To avoid installing redis locally, run the tests in a docker container. From the root of this repository, run:
```
docker build . -t test_build
docker run --entrypoint "/bin/bash" -it test_build:latest
```
Inside the container, run:
```
redis-server --daemonize yes
python -m pytest
```
<br><br>

## Functional tests with docker
To set up the service as a docker container, build and run the image:

```
docker build . -t test_build
docker run -p 80:80 test_build:latest
```
Then, in another process/terminal, run the functional tests with:
```
BASE_URL='http://localhost' venv/bin/python -m pytest functional_tests
```
