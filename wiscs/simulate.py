from . import config
from .utils import validate_params, parse_params

import numpy as np
import warnings
import numpy.typing as npt
import pandas as pd

def make_tasks(low, high, n) -> npt.ArrayLike:
    """Generate task parameters"""
    return np.random.permutation(np.linspace(low, high, n).round(0))

def generate(params:dict) -> npt.ArrayLike | npt.ArrayLike:
    """Generate data
    
    Returns
    -------
    image, word
    """

    if not np.array_equal(params["image"]["task"], params["word"]["task"]):
        warnings.warn("Tasks parameters are different. Generating data for ALTERNATIVE hypothesis.")

    # noise distributions
    var_item_image = np.random.normal(0, params["var"]["image"], (params["n"]["participant"], params["n"]["question"], params["n"]["trial"]))
    var_item_word = np.random.normal(0, params["var"]["word"], (params["n"]["participant"], params["n"]["question"], params["n"]["trial"]))
    var_question = np.random.normal(0, params["var"]["question"], (params["n"]["participant"], params["n"]["question"], params["n"]["trial"]))
    var_participant = np.random.normal(0, params["var"]["participant"], (params["n"]["participant"], params["n"]["question"], params["n"]["trial"]))

    return \
            (params["image"]["concept"]
           + params["image"]["task"][None, :, None] 
           + var_item_image
           + var_participant
           + var_question), \
            (params["word"]["concept"]
            + params["word"]["task"][None, :, None]
            + var_item_word
            + var_question
            + var_participant)

class DataGenerator(object):
    """Data generator
    
    Methods
    -------
    fit(self, params:dict=None)
        Generate data based on parameters

    to_pandas(self) -> pd.DataFrame
        Convert data to pandas dataframe

    Attributes
    ----------
    data: npt.ArrayLike | npt.ArrayLike
        Generated data (image, word)
    """ 

    def __init__(self):
        self.params = config.p  

    def fit(self, params:dict=None):
        if params is not None:
            validate_params(params)
            self.data = generate(parse_params(params))
        else:
            self.data = generate(self.params)
        return self          
    
    def to_pandas(self) -> pd.DataFrame:
        """Convert data to pandas dataframe"""
        
        df_image = pd.DataFrame({
            'participant': np.repeat(np.arange(self.params["n"]["participant"]), self.params["n"]["question"] * self.params["n"]["trial"]),
            'question': np.tile(np.repeat(np.arange( self.params["n"]["question"]), self.params["n"]["trial"]), self.params["n"]["participant"]),
            'trial': np.tile(np.arange(self.params["n"]["trial"]), self.params["n"]["participant"] * self.params["n"]["question"]),
            'RT': self.data[0].flatten() # image data
        })

        df_word = pd.DataFrame({
            'participant': np.repeat(np.arange(self.params["n"]["participant"]), self.params["n"]["question"] * self.params["n"]["trial"]),
            'question': np.tile(np.repeat(np.arange( self.params["n"]["question"]), self.params["n"]["trial"]), self.params["n"]["participant"]),
            'trial': np.tile(np.arange(self.params["n"]["trial"]), self.params["n"]["participant"] * self.params["n"]["question"]),
            'RT': self.data[1].flatten() # word data
        })

        df_image['modality'] = 'image'
        df_word['modality'] = 'word'
        return pd.concat([df_image, df_word], ignore_index=True)