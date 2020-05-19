"""Portainer stack CLI tool."""
import hashlib
from pathlib import Path
import sys

from invoke import Collection, Program, task
from jinja2 import Environment, FileSystemLoader
from swarm_stacks.lib import as_2y_hash, random_pass, check_program
from loguru import logger
import yaml


STACK_NAME = "portainer"
COMPOSE_FILE = "docker-compose.portainer.yml"
VOLUME_NAME = "portainer"
PUBLIC_NETWORK = "public"


@task
def check_reqs(c):
    """Check pre-requirements for portainer stack builder."""
    check_program(c, "htpasswd")


@task(pre=[check_reqs])
def create(
    c,
    image="portainer/portainer:1.23.2",
    agent_image="portainer/agent:1.5.1",
    port=9000,
    traefik_host="portainer.swarm.home",
    compose_file=COMPOSE_FILE,
    volume_name=VOLUME_NAME,
    public_network=PUBLIC_NETWORK,
):
    """Create compose file for portainer stack."""
    password = random_pass()
    cfg = {
        "image": image,
        "agent_image": agent_image,
        "port": port,
        "password": password,
        "traefik_host": traefik_host,
        "agent_secret": hashlib.md5(str.encode(random_pass())).hexdigest(),
        "password_hash": as_2y_hash(password).replace("$", "$$"),
        "volume_name": volume_name,
        "public_network": public_network,
    }
    env = Environment(
        loader=FileSystemLoader(packet_path / "templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("portainer.jinja2")
    Path(compose_file).write_text(template.render(cfg))
    logger.success(f"{compose_file} created")
    with open("portainer_secrets.yml", "w") as f:
        yaml.dump({"user": "admin", "password": password}, f)
    logger.success("Portainer UI credentials stored to the portainer_secrets.yml file")


@task
def start(c, stack_name=STACK_NAME, compose_file=COMPOSE_FILE):
    """Start docker stack from the generated compose file."""
    c.run(f"docker stack deploy {stack_name} --compose-file={compose_file}")


@task
def stop(c, stack_name=STACK_NAME):
    """Stop docker stack."""
    c.run(f"docker stack rm {stack_name}")


@task
def destroy(c, stack_name=STACK_NAME, volume_name=VOLUME_NAME):
    """Destroy persisted stack resources."""
    c.run(f"docker volume rm {stack_name}_{volume_name}")


logger.remove()
logger.add(
    sink=sys.stderr, colorize=True, format="<level>{message}</level>", level="TRACE",
)
ns = Collection()
ns.add_task(create)
ns.add_task(start)
ns.add_task(stop)
ns.add_task(destroy)
program = Program(namespace=ns, version="0.1.0")
packet_path = Path(sys.modules[__name__].__file__).parent
