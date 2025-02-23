# Waste classifier API

## Set up
First we need to clone the repository and start the docker containers.
```bash
git clone https:github.com/bcastillo-2022474/waste-classifier-api.git
```
```bash
docker compose up -d
```

After that we need to install poetry, a dependency manager, and then, install the dependencies.
```bash
pip install poetry
```

```bash
poetry install
```

now we already have the environment set up, now we need to create the database and set up the migrations.
First of all, we are going to get inside the `api` directory in which we have our Django application.
```bash
cd api
```

now, from here, we are going to be able to run django commands, so let's create the database and run the migrations.
```bash
python manage.py migrate
```

Now we are ready to run the server.
```bash
python manage.py runserver
```

We also can run this commands from the root directory of the project, but we need to specify the path to the `manage.py` file.
```bash
python api/manage.py migrate
```

```bash
python api/manage.py runserver
```

## Hexagonal Architecture explanation

The hexagonal architecture is a software architecture that separates the core logic of the application from the external services, this is done by creating ports and adapters, the ports are the interfaces that the core logic uses to interact with the external services, and the adapters are the implementations of those interfaces.

So, just so we get in to the core of the functinoality, we can say our `core` directory is like a library, and we can use it in our API (infra), using the use cases as the interfaces to interact with it.