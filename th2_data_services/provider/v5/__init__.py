#  Copyright 2022 Exactpro (Exactpro Systems Limited)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from th2_data_services.provider.utils.version_checker import get_package_version

version = get_package_version("th2_grpc_data_provider")

if not version:
    raise SystemError(f"Package th2_grpc_data_provider not found")

if version not in ("0.0.4", "0.1.4"):
    raise SystemError(f"There is unsupported version of th2_grpc_data_provider for v5 provider api ({version})")
