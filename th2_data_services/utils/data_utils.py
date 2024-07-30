#  Copyright 2024 Exactpro (Exactpro Systems Limited)
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

import os
from pathlib import Path
from typing import List, Union

from th2_data_services.data import Data


def read_all_pickle_files_from_the_folder(
    path: Union[str, Path], return_list=False
) -> Union[Data, List[Data]]:
    """Reads all Pickle files from the folder.

    Args:
        path: Directory path.
        return_list: Returns list of Data objects if True.

    Returns:
        Single data object or a list of Data objects.
    """
    datas = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if not filename.endswith(".pickle"):
                continue
            file_path = os.path.join(dirpath, filename)
            datas.append(Data.from_cache_file(file_path))

    if return_list:
        return datas

    if len(datas) == 1:
        return datas[0]
    else:
        d = Data(datas)
        d.update_metadata({"source_file": [dx.metadata.get("source_file") for dx in datas]})
        return d
