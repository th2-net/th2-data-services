import os
import re
import subprocess
import sys
from typing import List


def get_version_by_pip(package_name: str):  # noqa: D103
    pip_run = subprocess.run([sys.executable, "-m", "pip", "show", package_name], capture_output=True)
    if pip_run.returncode != 0:
        return None

    output = pip_run.stdout.decode()
    matches = re.findall(r"Version: (.*)", output)
    return matches[0]


def get_package_version(package_name: str):  # noqa: D103
    version = get_version_by_pip(package_name).strip()
    # TODO: get version in case of conda
    return version


def verify_grpc_version(valid: List[str]):  # noqa: D103
    if os.environ.get("TH2_DS_SKIP_GRPC_VERIFY", "0") == "1":
        return
    version = get_package_version("th2_grpc_data_provider")

    if not version:
        raise SystemError(f"Package th2_grpc_data_provider not found")

    if version not in valid:
        raise SystemError(f"There is unsupported version of th2_grpc_data_provider for v5 provider api ({version})")
