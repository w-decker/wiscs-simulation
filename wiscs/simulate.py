from utils import set_params

import numpy as np
from dataclasses import dataclass
import pandas as pd

@dataclass
class Data(object):

    params:dict

    def __post_init__(self):
        self.params = set_params(self.params)   

    def generate(self, theory:str):
        """Generate data"""
        pass
    
    @staticmethod
    def DataFrame(self):
        """Create a DataFrame"""
        pass