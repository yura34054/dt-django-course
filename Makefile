include .env

make all: docker_build docker_down docker_up docker_migrate

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

command:
	python src/manage.py ${c}

shell:
	python src/manage.py shell

debug:
	python src/manage.py debug

piplock:
	pipenv install
	sudo chown -R ${USER} Pipfile.lock

piplock_dev:
	pipenv install --dev
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
	docker build -t ${IMAGE_NGINX} ./nginx

docker_push:
	docker push ${IMAGE_APP}
	docker push ${IMAGE_NGINX}

docker_pull:
	docker pull ${IMAGE_APP}
	docker pull ${IMAGE_NGINX}

docker_up:
	docker-compose up -d

docker_migrate:
	docker exec ${CONTAINER_NAME} python manage.py migrate

docker_down:
	docker-compose down