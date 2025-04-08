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

---

# Notes 
- A Flask application is an instance of the Flask class. Everything about the application, such as configuration and URLs, will be registered with this class.
- The application will use a SQLite database to store users and posts. Python comes with built-in support for SQLite in the sqlite3 module.
- A Blueprint @bp.route() is a way to organise a group of related views and other code.
- Templates are files that contain static data as well as placeholders for dynamic data. A template is rendered with specific data to produce a final document. Flask uses the Jinja template library to render templates.
- Flask automatically adds a static view that takes a path relative to the flaskr/static directory and serves it.