import sys
from constants import EMPTY_PARAMS
import numpy as np
import pandas as pd

def set_params(params:dict=None, help=False):
    """Set data parameters"""

    if params is None and help:
        _ = sys.stdout.write("Params must be a dictionary of dictionaries with the following keys:\n")
        return EMPTY_PARAMS
    
    elif _validate_params(params):
            return params
    
def _validate_params(params:dict):
    """Validate data parameters"""
    
    if not isinstance(params, dict):
        raise ValueError("Params must be a dictionary")
    
    if not all([isinstance(params[key], dict) for key in params.keys()]):
        raise ValueError("Params must be a dictionary of dictionaries")
    
    if not all([key in ["word", "image", "variance", "n_participants", "n_trials"] for key in params.keys()]):
        raise ValueError("Params must contain 'word' and 'image' keys")
    
    if not all([key in ["perceptual", "conceptual", "task"] for key in params["word"].keys()]):
        raise ValueError("Params['word'] must contain 'perceptual', 'conceptual', and 'task' keys")
    
    if not all([key in ["perceptual", "conceptual", "task"] for key in params["image"].keys()]):
        raise ValueError("Params['image'] must contain 'perceptual', 'conceptual', and 'task' keys")
    
    return True

def _generate_diff_trial_means(params, trial):
    """
    Generate random means for word and image distributions with varying differences.
    """
    # Baseline means from params
    total_word = sum(params["word"].values())
    total_image = sum(params["image"].values())
    
    # Add random perturbation to ensure variability
    word_mean_base = total_word / (total_word + total_image)
    image_mean_base = total_image / (total_word + total_image)
    
    # Random trial-specific difference (can be positive or negative)
    trial_diff = np.random.uniform(-0.5, 0.5)  # Difference changes for every trial
    
    # Adjust means
    word_mean = word_mean_base + np.random.uniform(-0.1, 0.1)  # Add slight noise to the base
    image_mean = word_mean + trial_diff  # Ensure the difference
    
    # Keep means bounded in [0, 1]
    word_mean = max(0, min(1, word_mean))
    image_mean = max(0, min(1, image_mean))
    
    return word_mean, image_mean, trial_diff

def generate_same(params: dict):
    """Generate data where the difference in distributions is the same across trials."""
    # Normalize the params to compute relative means
    total_word = sum(params["word"].values())
    total_image = sum(params["image"].values())

    # Scale to a [0, 1] range for mean values
    word_mean = total_word / (total_word + total_image)
    image_mean = total_image / (total_word + total_image)

    # Generate data for trials
    word = [np.random.normal(word_mean, params["variance"], params["n_participants"]) for _ in range(params["n_trials"])]
    image = [np.random.normal(image_mean, params["variance"], params["n_participants"]) for _ in range(params["n_trials"])]

    return word, image

def generate_diff(params: dict):
    """Generate data where the difference in distributions varies across trials."""
    word = []
    image = []

    for trial in range(params["n_trials"]):
        # Generate trial-specific means
        word_mean, image_mean, _ = _generate_diff_trial_means(params, trial)

        # Generate distributions
        word.append(np.random.normal(word_mean, params["variance"], params["n_participants"]))
        image.append(np.random.normal(image_mean, params["variance"], params["n_participants"]))

    return word, image

def combine_data(params: dict):
    """Combine data from generate_same and generate_diff into a single DataFrame."""
    # Generate data
    word_same, image_same = generate_same(params)
    word_diff, image_diff = generate_diff(params)

    data = []

    # Add 'same' distribution data
    for trial in range(params["n_trials"]):
        for participant in range(params["n_participants"]):
            data.append({
                "data": word_same[trial][participant],
                "participant": participant + 1,
                "condition": "word",
                "distribution_type": "same"
            })
            data.append({
                "data": image_same[trial][participant],
                "participant": participant + 1,
                "condition": "image",
                "distribution_type": "same"
            })

    # Add 'diff' distribution data
    for trial in range(params["n_trials"]):
        for participant in range(params["n_participants"]):
            data.append({
                "data": word_diff[trial][participant],
                "participant": participant + 1,
                "condition": "word",
                "distribution_type": "diff"
            })
            data.append({
                "data": image_diff[trial][participant],
                "participant": participant + 1,
                "condition": "image",
                "distribution_type": "diff"
            })

    # Convert to DataFrame
    return pd.DataFrame(data)
