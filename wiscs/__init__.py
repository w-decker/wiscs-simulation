from .constants import EMPTY_PARAMS
from .utils import *
from .simulate import *
from . import config
from .utils import _validate_params

import sys

def set_params(params: dict = None, return_empty=False):
    """Set data parameters"""

    if params is None and return_empty:
        sys.stdout.write(
            f"Params must be a dictionary of dictionaries with the following keys:\n {EMPTY_PARAMS.keys()}"
        )
        return EMPTY_PARAMS
    elif params is not None and return_empty:
        raise ValueError("If params is provided, return_empty must be False")
    elif _validate_params(params):
        config.p = params
        print("Params set successfully")