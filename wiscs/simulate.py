from . import config

import numpy as np
import pandas as pd

def generate_same(params: dict):
    """Generate data where the difference in distributions is the same across trials."""
    
    total_word = sum(params["word"].values())
    total_image = sum(params["image"].values())

    word = np.random.normal(total_word, params["variance"], 
                            (params["n_participants"], params["n_trials"]))
    image = np.random.normal(total_image, params["variance"], 
                             (params["n_participants"], params["n_trials"]))
    return word, image

def generate_diff(params: dict):
    """Generate data where the difference in distributions is different across trials."""
    
    total_word = sum([params["word"]["perceptual"], params["word"]["conceptual"]])
    total_image = sum([params["image"]["perceptual"], params["image"]["conceptual"]])

    word = np.random.normal(total_word, params["variance"],(params["n_participants"], params["n_trials"]))
    image = np.random.normal(total_image, params["variance"],(params["n_participants"], params["n_trials"]))

    for i in range(params["n_trials"]):
        word[:, i] += np.random.uniform(*params["word"]["task"])
        image[:, i] += np.random.uniform(*params["image"]["task"])

    return word, image

class DataGenerator(object):

    def __init__(self):
        self.params = config.p  

    def generate(self, dist_type:str=None, params=None):
        """Generate data"""
        if params is not None:
            self.params = params
        if dist_type is not None:
            self.params["dist_type"] = dist_type

        if self.params["dist_type"] == 'same':
            assert self.params["word"]["task"] == self.params["image"]["task"], "Task parameters bust be the same if dist_type == 'same'"
            self.data = generate_same(self.params)
            return self
        elif self.params["dist_type"] == 'diff':
            assert isinstance(self.params["word"]["task"], tuple) 
            assert isinstance(self.params["image"]["task"], tuple)
            self.data = generate_diff(self.params)
            return self

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