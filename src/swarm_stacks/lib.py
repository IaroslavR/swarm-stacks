"""Common helpers."""

import random
import string
import subprocess
from typing import List

from invoke import UnexpectedExit
from loguru import logger

PROJECT_REQS = ["docker", "weq"]


def check_program(c, prg: str) -> bool:
    """Check program for existence."""
    try:
        c.run(f"hash {prg}", hide=True)
    except UnexpectedExit:
        logger.error(f"No {prg} installed")
        return True
    else:
        logger.success(f"{prg} found")
        return False


def check_reqs(c, reqs: List[str]) -> List[bool]:
    """Check target level pre-requirements."""
    return [check_program(c, e) for e in reqs]


def random_pass(length=20) -> str:
    """Generate a random string of letters and digits."""
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def as_2y_hash(password: str) -> str:
    """Generate 2Y hash for string."""
    r = subprocess.check_output(["htpasswd", "-nbB", "x", password]).decode("utf-8").strip()
    return r.strip("x:")
