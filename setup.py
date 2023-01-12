#   Copyright 2020-2020 Exactpro (Exactpro Systems Limited)
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json
from typing import Dict, List

from setuptools import setup, find_packages

with open("package_info.json", "r") as file:
    package_info = json.load(file)

package_name = package_info["package_name"].replace("-", "_")
package_version = package_info["package_version"]

with open("README.md", "r") as file:
    long_description = file.read()

with open("requirements.txt", "r") as file:
    requirements = [line.strip() for line in file.readlines() if not line.startswith("#") and line != "\n"]

CORE_EXTRAS_DEPENDENCIES: Dict[str, List[str]] = {
    "rdp": [
        "th2-data-services-rdp",
    ],
    "rdp5": [
        "th2-data-services-rdp>=5,<6",
    ],
    "rdp6": [
        "th2-data-services-rdp>=6,<7",
    ],
    "lwdp": [
        "th2-data-services-lwdp",
    ],
    "lwdp1": [
        "th2-data-services-lwdp>=1,<2",
    ],
    "lwdp2": [
        "th2-data-services-lwdp>=2,<3",
    ],
}

setup(
    name=package_name,
    version=package_version,
    description=package_name,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="TH2-devs",
    author_email="th2-devs@exactprosystems.com",
    url="https://github.com/th2-net/th2-data-services",
    license="Apache License 2.0",
    python_requires=">=3.7",
    install_requires=requirements,
    packages=find_packages(include=["th2_data_services*"]),
    extras_require=CORE_EXTRAS_DEPENDENCIES,
    include_package_data=True,
)
