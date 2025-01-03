from collections import defaultdict
import numpy as np
import numpy.typing as npt
from typing import Callable, Union, get_args
import types

EMPTY_PARAMS = {
    'word.concept': Union[int, float],
    'image.concept': Union[int, float],
    'image.*': Union[int, float, Callable[..., npt.ArrayLike]],
    'word.*': Union[int, float, Callable[..., npt.ArrayLike]],
    'word.task': Union[npt.ArrayLike, Callable[..., npt.ArrayLike]],
    'image.task': Union[npt.ArrayLike, Callable[..., npt.ArrayLike]],
    'var.image': Union[int, float],
    'var.word': Union[int, float],
    'var.question': Union[int, float],
    'var.participant': Union[int, float], 
    'n.participant': int,
    'n.question': int,
    'n.trial': int
}

def validate_params(params: dict) -> bool:
    for key, value in params.items():
        if key not in EMPTY_PARAMS:
            # Check for wildcard keys like `image.*`
            if any(key.startswith(prefix.split('.')[0]) and "*" in prefix for prefix in EMPTY_PARAMS):
                expected_type = EMPTY_PARAMS['image.*']
            else:
                raise ValueError(f"Unexpected parameter: {key}")
        else:
            expected_type = EMPTY_PARAMS[key]

        # Validate the type
        if isinstance(expected_type, type):
            if not isinstance(value, expected_type):
                raise TypeError(f"Parameter {key} should be {expected_type}, but got {type(value)}")

        elif (isinstance(expected_type, types.UnionType) or
              (hasattr(expected_type, '__origin__') and expected_type.__origin__ is Union)):
            union_args = get_args(expected_type)
            if not any(isinstance(value, t) for t in union_args):
                raise TypeError(f"Parameter {key} should be one of {union_args}, but got {type(value)}")

        elif expected_type == npt.ArrayLike:
            if not isinstance(value, (list, tuple, np.ndarray)):
                raise TypeError(f"Parameter {key} should be an array-like, but got {type(value)}")

        elif expected_type == Callable[..., npt.ArrayLike]:
            if not callable(value):
                raise TypeError(f"Parameter {key} should be a callable, but got {type(value)}")

        else:
            raise TypeError(f"Unsupported type for parameter {key}: {expected_type}")

    return True

def parse_params(params):
    """
    Parse a dictionary with compound keys into a nested dictionary.

    Parameters
    ----------
    params: dict 
        Dictionary with keys in the format 'category.attribute'.

    Returns
    -------
    dict: Nested dictionary with categories as top-level keys and attributes as subkeys.
    """
    parsed = defaultdict(dict)
    for key, value in params.items():
        category, attribute = key.split('.')
        parsed[category][attribute] = value
    return dict(parsed)

def update_params(params, kwargs) -> dict:
    """
    Update parameters with new values.

    Parameters
    ----------
    params: dict
        Original dictionary of parameters

    kwargs: dict
        Keys and values to be updated

    Returns
    -------
    dict: Updated parameters.
    """
    update = params.copy()
    new = parse_params(kwargs)

    for key, subdict in new.items():
        if key in update and isinstance(update[key], dict) and isinstance(subdict, dict):
            update[key].update(subdict)
        else:
            update[key] = subdict

    return update