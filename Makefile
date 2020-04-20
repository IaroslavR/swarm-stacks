.PHONY: help init start stop clean
.DEFAULT_GOAL = help

include .env
.EXPORT_ALL_VARIABLES:

help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

init-swarm:  ## Init docker swarm manager node
	- docker swarm init --advertise-addr ${SWARM_ADVERTISE_ADDR}

init-network:  ## Init public swarm network
	- docker network create -d overlay public

init-env:  ## Fill .env file
	touch .htpasswd
	python init.py

init: init-swarm init-network ## Initial swarm setup

start-portainer:
	docker stack deploy portainer --compose-file=docker-compose.portainer.yaml

start: start-portainer ## Stare server stacks
	docker stack deploy traefik --compose-file=docker-compose.traefik.yaml
	docker stack deploy whoami --compose-file=docker-compose.whoami.yaml

start-local:  ## Stare local stacks
	docker stack deploy portainer --compose-file=docker-compose.portainer.local.yaml
	docker stack deploy traefik --compose-file=docker-compose.traefik.local.yaml
	docker stack deploy whoami --compose-file=docker-compose.whoami.local.yaml

stop:  ## Stop all stacks
	docker stack rm portainer
	docker stack rm traefik
	docker stack rm whoami

clean-swarm:  ## Delete persistent containers, public network and stop swarm manager
	- docker swarm leave --force
	- docker network rm public traefik_traefik-socket portainer_portainer
	- docker volume rm portainer_portainer traefik_traefik-certificates

clean: stop  ## Stop stacks and prune unused docker objects
	docker system prune

fresh:  clean init-network  ## Start cleanup sequence

init-certs:  ## Install local CA
	mkcert -install

clean-certs: ## Remove local CA and certs
	mkcert -unistall
	rm ./traefik/*.pem

certs:  ## generate wildcard certificates for the swarm.home domain
	cd traefik && mkcert *.swarm.home

