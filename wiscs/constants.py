import numpy.typing as npt
from typing import Callable, Union

EMPTY_PARAMS = {
    'word.concept': Union[int, float],
    'image.concept': Union[int, float],
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