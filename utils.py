import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

def overlap(x:npt.ArrayLike, y:npt.ArrayLike) -> bool:
    """Determine if two distributions overlap"""
    return not(max(x) < min(y) or max(y) < min(x))

def simulate(p_word, 
             p_image, 
             task, 
             sigma:np.float32, 
             n_iter:int, 
             x_word=None, 
             x_image=None) ->npt.ArrayLike | npt.ArrayLike:
    """Generate simulation
    Parameters
    ----------
    p_word: timing parameters for word perceptual processing

    p_image: timing parameters for image perceptual processing
    
    x_word: timing parameters for word -> concept

    x_image: timing parameter for image -> concept

    task: timing parameter for c -> task

    sigma: np.float32
        amount of noise to add to distribution
    
    n_iter: int
        Number of iterations
    """
    noise_w = np.random.normal(0, sigma, n_iter)
    noise_i = np.random.normal(0, sigma, n_iter)
    return np.array(p_word + x_word + task + noise_w), np.array(p_image + x_image + task + noise_i)

def plot(word_dat:npt.ArrayLike, image_dat:npt.ArrayLike):
    """Plot distributions"""

    plt.hist(word_dat, alpha=0.7, label="words")
    plt.hist(image_dat, alpha=0.7, label="images")
    plt.axvline(np.mean(word_dat), color='k', linestyle='--')
    plt.axvline(np.mean(image_dat), color='k', linestyle='--')

    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()

def t(x:npt.ArrayLike, y:npt.ArrayLike, verbose:bool=True) -> np.float32:
    """Calculate t-statistic"""
    t, p = ttest_ind(x, y)
    if verbose:
        print(f't-statistic: {t}, p-value: {p.round(7)}')
    return t, p
    