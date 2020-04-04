# swarm-stacks
Common docker swarm stacks

### Stacks
- - [Portainer](https://www.portainer.io/) Can be started this way: `docker stack deploy portainer --compose-file=docker-compose.portainer.yaml` UI port will be forwarded to the `http://localhost:9000`. 
    After initial password setup choose `Connect to a Portainer agent`, enter `tasks.agent:9001` as endpoint url and press `Connect`. 
