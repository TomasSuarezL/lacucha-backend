# La Cucha App - Backend

## Stack

- Python
- Flask
- Flask-RESTx
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow

## Project Organization

The project organization is based on [this post](http://alanpryorjr.com/2019-05-20-flask-api-example/) but with some simplifcations. This organization allows high scalability and mantainability on large projects. For this project, we modified this structure so it's less complex while keeping most of the beneifts. We think this is right balance for this API.

Simplifying, the structure consists of dividing the code into "logic units" of one or more entities (usually a main business entity with its "support" - i.e: Bloques and EjerciciosXBloque are grouped in the same "unit"). For each unit, we split the code into:

- Model: where we define the entity class. This is the columns of the entity using Flask-SQLAlchemy, constructor and class methods.
- Service: where we define all the possible operations on the entity.
- Controller: where we put the API routes that we are going to expose, related to the logic unit.
- Schema: object for serialization and desearlization defined using Marshmallow.
- Tests: finally we create a test file where we will write the tests associated with the logic unit. The tests focus on the service, and non-trivial controller methods (mostly integration tests).

On the `__init__` file of each unit subfolder we expose a method for registering the routes. The registration happens on the `routes.py` file in the root. We then call the route registering method (`register_routes`) exposed in `routes.py` to register all routes (this leverages FLASK-RESTx) on the app factory method.

There are a couple of differences between this approach and the original. We did't include the Interface definitions for each unit and we use a single test file for the entire unit (instead of creating a file for each of the divisions).

## DB Model

## Migrations

We use Flask-migrate to handle migrations. We can execute migratios throught `manage.py` in the root folder. To generate the migration, we can run:

`python manage.py db migrate`

This will detect difference between models and the database and generate a migration script. To apply changes to the Database, we can run:

`pyhton manage.py db upgrade`

Additionally, this file exposes a `seed` method that can be used to populate some tables with default initial data (such as Ejercicios).

## Deploy

Heroku - hooked to Github repo (master branch).

## Development

Clone github repo. On the root folder, install dependencies using:

```
pip install -r requirements.txt
```

Create a `.env` file with Databases URLs:

```python
DATABASE_URL="postgresql://postgres_user:postgres_password@prod_server:5432/lacucha"
TEST_DATABASE_URL="postgresql://postgres_user:postgres_password@127.0.0.1:5432/lacucha_tests"
```

Additionally, we need to supply valid Firebase Credentiasl to get a Token for testing protected routes.

```python
TEST_USER_EMAIL="email"
TEST_USER_PASSWORD="password"
```

To run the tests, on the root folder:

```
pytest
```
