#  Copyright 2023 Exactpro (Exactpro Systems Limited)
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
from typing import List, Union


class ResponseFormats:
    def __init__(self):
        """ResponseFormats Constructor."""

    @staticmethod
    def is_valid_response_format(formats: Union[str, List[str]]):
        correct_formats = ["PROTO_PARSED", "JSON_PARSED", "BASE_64"]
        if isinstance(formats, str):
            formats = [formats]
        if not isinstance(formats, list):
            raise Exception("Wrong type. formats should be list or string")
        if "JSON_PARSED" in formats and "PROTO_PARSED" in formats:
            raise Exception("response_formats can't have both both JSON_PARSED and PROTO_PARSED values")
        if not all(format in correct_formats for format in formats):
            raise Exception("Possible values for response_formats are PROTO_PARSED, JSON_PARSED and BASE_64")