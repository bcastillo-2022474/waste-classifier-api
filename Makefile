default: dev

test:
	python -m coverage run -m unittest discover core/tests
	python -m coverage report

dev:
	dotenv -f .env run -- python api/manage.py runserver 8000

migrate:
	dotenv -f .env run -- python api/manage.py migrate

makemigrations:
	dotenv -f .env run -- python api/manage.py makemigrations

createsuperuser:
	dotenv -f .env run -- python api/manage.py createsuperuser

venv:
	.venv/Scripts/Activate.ps1
