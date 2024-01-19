SHELL := /bin/bash

test: 
	pytest --cov . --cov-report term-missing

run:
	python manage.py migrate
	python manage.py runserver 0.0.0.0:80


migrate:
	python manage.py makemigrations
	python manage.py migrate

