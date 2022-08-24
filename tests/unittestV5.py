import pip
import pytest

PATH_DIFF_VERSION = "tests_unit/tests_diff_version"
PACKAGE_NAME = "th2-grpc-data-provider"

grpc_version_5 = "0.1.6"


def install_package(name: str, version: str) -> int:
    return pip.main(["install", f"{name}=={version}", "--upgrade"])


def run_tests(source_dir: str = ".", ignore_dir=None) -> int:
    args = [source_dir]
    if ignore_dir is not None:
        args.append(f"--ignore={ignore_dir}")
    return pytest.main(args)


if __name__ == "__main__":
    install_package(PACKAGE_NAME, grpc_version_5)
    run_tests(source_dir="./tests_unit", ignore_dir=f"./{PATH_DIFF_VERSION}/tests_v6")
