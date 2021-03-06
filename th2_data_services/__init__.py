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

from .data import Data
from .filter import Filter
import logging
from logging import NullHandler

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())

# INTERACTIVE_MODE - is a global variable that tells the library not to delete
# the Data cache file if data iteration is interrupted.
INTERACTIVE_MODE = False  # Script mode by default.


def add_stderr_logger(level=logging.DEBUG):
    """Helper for quickly adding a StreamHandler to the logger.

    Useful for debugging.

    Returns the handler after adding it.
    """
    # This method needs to be in this __init__.py to get the __name__ correct
    # even if the lib is vendored within another package.
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s : %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.debug("Added a stderr logging handler to logger: %s", __name__)
    return handler


def add_file_logger(filename="dslib.log", mode="w", level=logging.DEBUG):
    """Helper for quickly adding a StreamHandler to the logger.

    Useful for debugging.

    Returns the handler after adding it.
    """
    # This method needs to be in this __init__.py to get the __name__ correct
    # even if the lib is vendored within another package.
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler(filename, mode=mode)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s : %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.debug("Added a file logging handler to logger: %s", __name__)
    return handler
