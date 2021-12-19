run:
	venv/bin/gunicorn --bind=0.0.0.0:8000 flask_app:app

debug:
	FLASK_ENV=development FLASK_APP=flask_app flask run
