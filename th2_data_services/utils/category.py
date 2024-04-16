#  Copyright 2023-2024 Exactpro (Exactpro Systems Limited)
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


class Category:
    def __init__(self, name: str, get_func):
        """Category is category name + categorizer function.

        Args:
            name: Name that you will see as category name. Often it's a column name.
            get_func: A function to get a value for this category from every data value.
        """
        self.name: str = name
        self.get_func = get_func

    def __repr__(self):
        return f"Category<{self.name}>"
