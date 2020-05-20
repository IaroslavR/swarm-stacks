"""Postgres stack CLI tool."""
from pathlib import Path
import sys

from invoke import Collection, Program, task
from jinja2 import Environment, FileSystemLoader
from swarm_stacks.lib import random_pass
from loguru import logger
import yaml


STACK_NAME = "postgres"
VOLUME_NAME = "postgres"
PUBLIC_NETWORK = "public"
IMAGE = "postgres:12.3-alpine"
PORT = 5432
USER = "root"
DB = "postgres"


@task
def create(
    c,
    image=IMAGE,
    port=PORT,
    user=USER,
    db=DB,
    stack_name=STACK_NAME,
    volume_name=VOLUME_NAME,
    public_network=PUBLIC_NETWORK,
):
    """Create compose file for portainer stack."""
    compose_file = f"docker-compose.{stack_name}-postgres.yml"
    secrets_file = f"secrets.{stack_name}-postgres.yml"
    password = random_pass()
    cfg = {
        "image": image,
        "port": port,
        "password": password,
        "user": user,
        "db": db,
        "volume_name": volume_name,
        "public_network": public_network,
    }
    env = Environment(
        loader=FileSystemLoader(packet_path / "templates"), trim_blocks=True, lstrip_blocks=True
    )
    template = env.get_template("postgres.jinja2")
    Path(compose_file).write_text(template.render(cfg))
    logger.success(f"{compose_file} created")
    with open(secrets_file, "w") as f:
        yaml.dump({"user": user, "password": password}, f)
    logger.success(f"Postgres user credentials stored to the {secrets_file} file")


@task
def start(c, stack_name=STACK_NAME):
    """Start docker stack from the generated compose file."""
    compose_file = f"docker-compose.{stack_name}-postgres.yml"
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
