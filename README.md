# swarm-stacks
Common docker swarm stacks

### Usage
1. `make init-env`
1. `make init`
1. `make start`

### Available Stacks
- [Portainer](https://www.portainer.io/) After first login choose `Connect to a Portainer agent`, enter `tasks.agent:9001` as endpoint url and press `Connect`. 
- [Traefik](https://docs.traefik.io/) an open-source Edge Router
- [whoami](https://github.com/containous/whoami) Tiny Go webserver that prints os information and HTTP request to output for testing
### Available Commands
```
$ make

Usage:
  make <target>

Targets:
  help        Display this help
  init-swarm  Init docker swarm manager node
  init-network  Init public swarm network
  init-env    Fill .env file
  init        Initial swarm setup
  start       Stare all stacks
  stop        Stop all stacks
  clean-swarm  Delete public network and stop swarm
  clean       Stop stacks and prune unused docker objects
  fresh       Start cleanup sequence

```