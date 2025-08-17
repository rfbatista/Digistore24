run:
	uv run manage.py runserver
test:
	uv run python manage.py test
migrate:
	uv run python manage.py migrate
migrations:
	uv run python manage.py makemigrations
user:
	uv run python manage.py createsuperuser
seed:
	uv run python manage.py seed
