DOCKER_COMPOSE = docker compose
SERVICE = app
WORKDIR = --workdir /src

CONTAINER_RUNNING_EXISTS = $(if $(shell docker ps -q --filter "name=tochka-$(SERVICE)"),true,false)

ifeq ($(CONTAINER_RUNNING_EXISTS),true)
	EXEC = $(DOCKER_COMPOSE) exec -T $(SERVICE)
else
	EXEC = $(DOCKER_COMPOSE) run --rm $(SERVICE)
endif

migrate:
	$(DOCKER_COMPOSE) run --rm $(SERVICE) python3 src/manage.py migrate $(if $m, api $m,)

makemigrations:
	$(DOCKER_COMPOSE) run --rm $(WORKDIR) $(SERVICE) python3 src/manage.py makemigrations

createsuperuser:
	$(DOCKER_COMPOSE) exec $(SERVICE) python3 src/manage.py createsuperuser

collectstatic:
	$(DOCKER_COMPOSE) run --rm $(SERVICE) python3 src/manage.py collectstatic --noinput

command:
	$(EXEC) ${c}

shell:
	$(DOCKER_COMPOSE) exec $(SERVICE) sh

debug:
	$(EXEC) debug

piplock:
	$(EXEC) pipenv install

lint:
	$(DOCKER_COMPOSE) run --rm $(WORKDIR) $(SERVICE) isort .
	$(DOCKER_COMPOSE) run --rm $(WORKDIR) $(SERVICE) flake8 --config setup.cfg
	$(DOCKER_COMPOSE) run --rm $(WORKDIR) $(SERVICE) black --config pyproject.toml .

check_lint:
	$(DOCKER_COMPOSE) run --rm $(SERVICE) isort --check --diff .
	$(DOCKER_COMPOSE) run --rm $(SERVICE) flake8 --config setup.cfg
	$(DOCKER_COMPOSE) run --rm $(SERVICE) black --check --config pyproject.toml .

build:
	$(DOCKER_COMPOSE) build

push:
	docker push ${IMAGE_APP}

pull:
	docker pull ${IMAGE_APP}

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

rebuild:
	$(DOCKER_COMPOSE) up --build -d

clean:
	$(DOCKER_COMPOSE) down -v
	$(DOCKER_COMPOSE) rm -f
	docker rmi $$(docker images -q)

test:
	$(DOCKER_COMPOSE) run --rm $(SERVICE) pytest --disable-warnings

gen_fernet_key:
	$(EXEC) python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"