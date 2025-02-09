#  Copyright 2022-2025 Exactpro (Exactpro Systems Limited)
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


from abc import ABC


class IEventStruct(ABC):
    """Just to mark Event Struct class.

    Actually, this class doesn't describe the structure, it describes filed names.

    It should look like a class with constants.
    """


class IMessageStruct(ABC):
    """Just to mark Message Struct class.

    Actually, this class doesn't describe the structure, it describes filed names.

    It should look like a class with constants.
    """
