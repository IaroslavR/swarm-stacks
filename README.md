# swarm-stacks
Common docker swarm stacks

### Usage
##### For server
1. `make init-env`
1. `make init`
1. `make start`
##### For local deployment
1. `make init-env`
1. `make init-cert`
1. Edit the file `/etc/NetworkManager/NetworkManager.conf`, and add the line `dns=dnsmasq` to the `[main]` section,
1. `sudo rm /etc/resolv.conf ; sudo ln -s /var/run/NetworkManager/resolv.conf /etc/resolv.conf`
1. `echo 'address=/.swarm.home/192.168.43.176' | sudo tee /etc/NetworkManager/dnsmasq.d/swarm.home-wildcard.conf`
1. `sudo systemctl reload NetworkManager`
1. `make init`
1. `make start-local`  
after that, `portainer.swarm.home`, `traefik.swarm.home` and `whoami.swarm.home` will be available from Chrome and Firefox with valid sertificates.

##### References
- [MKCERT: Valid HTTPS certificates for localhost](https://blog.filippo.io/mkcert-valid-https-certificates-for-localhost/)
- [How can I set up local wildcard domain resolution on Ubuntu 18.04?
](https://askubuntu.com/a/1031896/441554)

### Available Stacks
- [Traefik](https://docs.traefik.io/) `docker-compose.traefik.yaml` Lets Encrypt version for the real servers
- [Traefik](https://docs.traefik.io/) `docker-compose.traefik.local.yaml` Self-signed certificate version for the local development stack. See above for the details.
- [Portainer](https://www.portainer.io/) `docker-compose.portainer.yaml`/`docker-compose.portainer.local.yaml` After first login choose `Connect to a Portainer agent`, enter `tasks.agent:9001` as endpoint url and press `Connect`. 
- [whoami](https://github.com/containous/whoami) `docker-compose.whoami.yaml`/`docker-compose.whoami.local.yaml` Tiny Go web-server that prints os information and HTTP request to output for testing

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
    start       Stare server stacks
    start-local  Stare local stacks
    stop        Stop all stacks
    clean-swarm  Delete persistent containers, public network and stop swarm manager
    clean       Stop stacks and prune unused docker objects
    fresh       Start cleanup sequence
    init-certs  Install local CA
    clean-certs  Remove local CA and certs
    certs       generate wildcard certificates for the swarm.home domain
```
