*WARNING: This tutorial was written in 2010 and is outdated - cannot support Flask-migration nor Flask-SQLalchemy*

# Flask Tutorial
https://flask.palletsprojects.com/en/stable/tutorial/

## Answers
https://github.com/pallets/flask/tree/main/examples/tutorial

## How to install
```
pip install -e .
```

## Initialise database
```
flask --app flaskr init-db
```

## How to run app
```
flask --app flaskr run --debug
```
or 
```
flask run
```

## Link for app
http://127.0.0.1:5000/auth/login/

## Run unit tests, assess coverage, and generate report
```
pytest -v
coverage run -m pytest
coverage html
```

## Deployment
```
# Build and Install
pip install build
python -m build --wheel
pip install flaskr-1.0.0-py3-none-any.whl

# Configure secret key
python -c 'import secrets; print(secrets.token_hex())'

# Run with a production server
pip install waitress
waitress-serve --call 'flaskr:create_app'
```

## Database migration
```
export FLASK_APP=flaskr
flask db init      # Initializes the migrations folder
flask db migrate   # Generates the migration script
flask db upgrade   # Applies the migration to the database
```

---

# Notes 
- A Flask application is an instance of the Flask class. Everything about the application, such as configuration and URLs, will be registered with this class.
- The application will use a SQLite database to store users and posts. Python comes with built-in support for SQLite in the sqlite3 module.
- A Blueprint @bp.route() is a way to organise a group of related views and other code.
- Templates are files that contain static data as well as placeholders for dynamic data. A template is rendered with specific data to produce a final document. Flask uses the Jinja template library to render templates.
- Flask automatically adds a static view that takes a path relative to the flaskr/static directory and serves it.
- The application context keeps track of the application-level data during a request, CLI command, or other activity. Rather than passing the application around to each function, the current_app and g proxies are accessed instead.
- The g name stands for “global”, but that is referring to the data being global within a context. The data on g is lost after the context ends, and it is not an appropriate place to store data between requests. Use the session or a database to store data across requests.
- To migrate database have a look at Flask-Migrate https://flask-migrate.readthedocs.io/en/latest/