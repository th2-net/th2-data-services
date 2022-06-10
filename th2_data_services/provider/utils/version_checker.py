import re
import subprocess
import sys


def get_version_by_pip(package_name):
    pip_run = subprocess.run([sys.executable, "-m", "pip", "show", package_name], capture_output=True)
    if pip_run.returncode != 0:
        return None

    output = pip_run.stdout.decode()
    matches = re.findall(r"Version: (.*)", output)
    return matches[0]


def get_package_version(package_name):
    version = get_version_by_pip(package_name)
    # TODO: get version in case of conda
    return version
