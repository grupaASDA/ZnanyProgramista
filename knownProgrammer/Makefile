.PHONY: all install migrate load_data runserver

all: install migrate load_data runserver

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations accounts communication programmers
	python manage.py migrate

load_data:
	python manage.py loaddata initial_db.json

runserver:
	python manage.py runserver