import hashlib
import random
import string

import subprocess


def random_pass(length=20):
    """Generate a random string of letters and digits """
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def as_apr1_hash(password):
    return subprocess.check_output(["openssl", "passwd", "-apr1", password]).decode("utf-8").strip()


def as_2y_hash(password):
    r = subprocess.check_output(["htpasswd", "-nbB", "x", password]).decode("utf-8").strip()
    return r.strip("x:")


def htpasswd(user, password):
    return "{}:{}".format(user, as_apr1_hash(password))


env = {
    "PORTAINER_PORT": input(
        "Enter portainer published port. "
        "For activate this future uncomment ports in the docker-compose.portainer.yaml "
        "[54492]: "
    ),
    "SWARM_ADVERTISE_ADDR": input(
        "Enter advertise address. "
        "See https://docs.docker.com/engine/reference/commandline/swarm_init/#--advertise-addr "
    ),
    "TRAEFIK_HOST_NAME": input("Enter host name for traefik. [example.com]: "),
    "TRAEFIK_LE_EMAIL": input("Enter email for Let's Encrypt. [mail@example.com]: "),
}
if not env["PORTAINER_PORT"]:
    env["PORTAINER_PORT"] = "54492"
portainer_p = random_pass()
env["PORTAINER_PASSWORD"] = as_2y_hash(portainer_p).replace("$", "$$")
print("Portainer credentials: \nadmin\n{}".format(portainer_p))
print("Portainer password hash will be saved to the .env file")
env["PORTAINER_AGENT_SECRET"] = hashlib.md5(str.encode(random_pass())).hexdigest()
print("Portainer agent secret will be saved to the .env file")
traefik_user = input("Enter user name for traefik BasicAuth. [admin]: ")
if not traefik_user:
    traefik_user = "admin"
traefik_p = random_pass()
with open(".htpasswd", "w") as f:
    f.write(htpasswd(traefik_user, traefik_p))
print("Traefik credentials: \n{}\n{}".format(traefik_user, traefik_p))
print("Traefik credentials saved to the .htpasswd")

if not env["TRAEFIK_HOST_NAME"]:
    env["TRAEFIK_HOST_NAME"] = "example.com"
print("Host name will be saved to the .env file")

if not env["TRAEFIK_LE_EMAIL"]:
    env["TRAEFIK_LE_EMAIL"] = "mail@example.com"
print("Email for Let's Encrypt will be saved to the .env file")
with open(".env", "w") as f:
    f.write("\n".join(["{}={}".format(k, v) for k, v in env.items()]))
print("Done. Save generated credentials to your password manager")
