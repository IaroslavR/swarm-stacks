SHELL = /bin/bash
include .env
.EXPORT_ALL_VARIABLES:
.PHONY: help start stop clean
.DEFAULT_GOAL = help

STACK_NAME = tapway-v4
API_PORT = 5000
CONDA_ENV_NAME = tapway-config-api
export POSTGRES_URI=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

ecr-login:
# https://stackoverflow.com/a/45938500/4249707
# https://arslan.io/2019/07/03/how-to-write-idempotent-bash-scripts/
	rm -f ${HOME}/.docker/config.json
	$(shell aws ecr get-login --region ${REGION} --no-include-email)

update-env-file:  ## Copy actual conda env to the environment.yml
	conda env export > environment.yml

update-conda-env:  ## Update project environment from the environment.yml
	conda env update --name ${CONDA_ENV_NAME} --file environment.yml --prune

update-packages:  ## Update environment packages to latest versions
	update_env.sh

build: update-env-file  ## Build docker image
	docker-compose build

push: ecr-login  ## Push image to the registry
# workaround for error creating overlay mount
# https://github.com/docker/for-linux/issues/711#issuecomment-525374910
	docker push ${ECR_REGISTRY_URL}:${TAG}

start-api:  ## Start API server
	docker stack deploy ${STACK_NAME} --compose-file=docker-compose.yml

start-postgres:  ## Start Postgres server
	docker stack deploy ${STACK_NAME} --compose-file=docker-compose.postgres.yml


start:  start-api  start-postgres ## Start API server swarm stack

stop:  ## Stop API server swarm stack
	docker stack rm ${STACK_NAME}

restart: stop start  ## Kill stack and restart

test:  ## Run tests. pre-commit hooks errors will be ignored
	pre-commit run -a
	py.test -c tests/

init:  ## Install and init project pre-requirements
	docker swarm init
	docker network create -d overlay public
	pre-commit install --install-hooks
	conda update -q conda
	conda config --add channels conda-forge
	conda env create --name ${CONDA_ENV_NAME} -f environment.yml

check-clean:
	@echo -n "Are you sure? ALL pre-requirements listed in the init target will be deleted [y/N] " && read ans && [ $${ans:-N} = y ]

clean:  check-clean  ## Remove ALL pre-requirements from init target. Use careful
	docker swarm leave --force
	docker network rm public
	pre-commit uninstall
	conda remove --channel conda-forge
	conda remove --name tapway-config-api --all

gen-migration:  ## Generate RDS migration file. RDS server must be started
	cd models && \
	alembic revision --autogenerate

run-migration:  ## Run RDS migration file. RDS server must be started
	cd models && \
	alembic upgrade head

monkeytype:  ## Generate monkeytype stubs from tests https://github.com/Instagram/MonkeyType
	py.test --monkeytype-output=./monkeytype.sqlite3
	monkeytype list-modules

test-typehints:  ## Test for type hinting
	 py.test --mypy