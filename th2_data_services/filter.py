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

from th2_grpc_data_provider.data_provider_pb2 import Filter as grpc_Filter, FilterName as grpc_FilterName
import google.protobuf.wrappers_pb2

class Filter:
    def __init__(self, name: str, values: str or (list, tuple), negative: bool = False, conjunct: bool = False):
        self.name = name

        if isinstance(values, (list, tuple)):
            self.values = map(str, values)
        else:
            self.values = [str(values)]

        self.negative = negative
        self.conjunct = conjunct

    def url(self):
        return (
            f"&filters={self.name}"
            + "".join([f"&{self.name}-values={val}" for val in self.values])
            + f"&{self.name}-negative={self.negative}"
        )

    def grpc(self) -> grpc_Filter:
        return grpc_Filter(name=grpc_FilterName(filter_name=self.name),
                           negative=google.protobuf.wrappers_pb2.BoolValue(value=self.negative),
                           values=self.values,
                           conjunct=google.protobuf.wrappers_pb2.BoolValue(value=self.conjunct))
