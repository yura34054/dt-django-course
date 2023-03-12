make all: docker_build docker_up docker_migrate

migrate:
	python src/manage.py migrate $(if $m, api $m,)

makemigrations:
	python src/manage.py makemigrations
	sudo chown -R ${USER} src/app/migrations/

createsuperuser:
	python src/manage.py createsuperuser

collectstatic:
	python src/manage.py collectstatic --no-input

dev:
	python src/manage.py runserver localhost:8000

bot:
	python src/manage.py run_bot

command:
	python src/manage.py ${c}

shell:
	python src/manage.py shell

debug:
	python src/manage.py debug

piplock:
	pipenv install
	sudo chown -R ${USER} Pipfile.lock

lint:
	isort .
	flake8 --config setup.cfg
	black --config pyproject.toml .

check_lint:
	isort --check --diff .
	flake8 --config setup.cfg
	black --check --config pyproject.toml .

docker_build:
	docker build -t ${IMAGE_APP} .

docker_push:
	docker push ${IMAGE_APP}

docker_pull:
	docker pull ${IMAGE_APP}

docker_up:
	docker-compose up -d

docker_migrate:
	docker exec -it dt-django-homework-web-1 python manage.py migrate

docker_down:
	docker-compose down
