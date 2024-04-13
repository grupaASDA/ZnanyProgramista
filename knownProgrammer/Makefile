.PHONY: all install migrate loaddata runserver

all: install migrate loaddata runserver

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations accounts communication programmers
	python manage.py migrate

loaddata:
	python manage.py loaddata initial_db.json

runserver:
	python manage.py runserver