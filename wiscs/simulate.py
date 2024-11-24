from .utils import set_params, generate_same, generate_diff, combine_data

import numpy as np
from dataclasses import dataclass
import pandas as pd

@dataclass
class DataGenerator(object):

    params:dict

    def __post_init__(self):
        self.params = set_params(self.params)   

    def generate(self, dist_type:str):
        """Generate data"""
        if dist_type == 'same':
            self.data = generate_same(self.params)
            return self
        elif dist_type == 'diff':
            self.data = generate_diff(self.params)
            return self
        elif dist_type == 'combined':
            self.data = combine_data(self.params)
            return self
        else:
            raise ValueError(f"Invalid theory: {dist_type}")
    
    def to_pandas(self):

        if self.data is None:
            raise ValueError("No data has been generated")
        if len(self.data) == 6:
            df = []
            n_participants = len(self.data[0][0])  # Assuming word, image, word1, image1 are lists of lists with participants' data
            for trial in range(len(self.data[0])):
                for participant in range(n_participants):
                    df.append({"trial": trial, "type": "same", "RT": self.data[0][trial][participant], "modality": "word", "participant": participant})
                    df.append({"trial": trial, "type": "same", "RT": self.data[1][trial][participant], "modality": "image", "participant": participant})
                    df.append({"trial": trial, "type": "diff", "RT": self.data[3][trial][participant], "modality": "word", "participant": participant})
                    df.append({"trial": trial, "type": "diff", "RT": self.data[4][trial][participant], "modality": "image", "participant": participant})
            return pd.DataFrame(df).explode("RT")
        
        elif len(self.data) == 3:
            df = []
            n_participants = len(self.data[0][0])
            for trial in range(len(self.data[0])):
                for participant in range(n_participants):
                    df.append({"trial": trial, "type": "same", "RT": self.data[0][trial][participant], "modality": "word", "participant": participant})
                    df.append({"trial": trial, "type": "same", "RT": self.data[1][trial][participant], "modality": "image", "participant": participant})
            return pd.DataFrame(df).explode("RT")
