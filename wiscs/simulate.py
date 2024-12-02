from . import config

import numpy as np
import pandas as pd

def generate(params: dict):
    """Generate data where the difference in distributions is the same across trials."""
    
    total_word = sum(params["word"].values())
    total_image = sum(params["image"].values())

    word = np.random.normal(total_word, params["variance"], 
                            (params["n_participants"], params["n_trials"]))
    image = np.random.normal(total_image, params["variance"], 
                             (params["n_participants"], params["n_trials"]))
    return word, image

class DataGenerator(object):

    def __init__(self):
        self.params = config.p  

    def generate(self, dist_type:str):
        """Generate data"""
        if dist_type == 'same':
            assert self.params["word"]["task"] == self.params["image"]["task"], "Task parameters bust be the same if dist_type == 'same'"
            self.data = generate(self.params)
            return self
        elif dist_type == 'diff':
            assert self.params["word"]["task"] != self.params["image"]["task"], "Task parameters bust be the different if dist_type == 'diff'"
            self.data = generate(self.params)
            return self
        else:
            raise ValueError(f"Invalid theory: {dist_type}")

    def to_pandas(self):
        """Convert data into a pandas DataFrame"""
        
        word, image = self.data
        df = pd.DataFrame({
            "word": word.flatten(),
            "image": image.flatten(),
            "participant": np.repeat(range(self.params["n_participants"]), self.params["n_trials"]),
            "trial": np.tile(range(self.params["n_trials"]), self.params["n_participants"])
        })
        return df