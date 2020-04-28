SHELL = /bin/bash
include .env
.EXPORT_ALL_VARIABLES:
.PHONY: help start stop restart clean
.DEFAULT_GOAL = help


help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

start:  ## Start Postgres server
	docker stack deploy ${STACK_NAME} --compose-file=docker-compose.postgres.yml

stop:  ## Stop API server swarm stack
	docker stack rm ${STACK_NAME}

restart: stop start  ## Kill stack and restart
