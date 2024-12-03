from .simulate import DataGenerator
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

class Plot(DataGenerator):
    def __init__(self, DG: DataGenerator):
        self.__dict__ = DG.__dict__.copy()
    
    def imshow(self):
        """Plot heatmap"""
        fig, ax = plt.subplots(1, len(self.data), figsize=(10, 5))
        for i in range(len(self.data)):
            ax[i].imshow(self.data[i], aspect='auto')
            ax[i].set_xlabel("Trial")
            ax[i].set_ylabel("Participant")
            ax[0].set_title("Word")
            ax[1].set_title("Image")
        plt.show()

    def hist(self):
        """Plot histogram"""
        fig, ax = plt.subplots(1, len(self.data), figsize=(10, 5))
        for i in range(len(self.data)):
            ax[i].hist(self.data[i].flatten())
            ax[i].set_xlabel("RT")
            ax[i].set_ylabel("Frequency")
            ax[0].set_title("Word")
            ax[1].set_title("Image")
        plt.show()

    def grid(self):
        """Plot grid of histograms across trials for word and image data"""

        fig, ax = plt.subplots(6, 5, figsize=(20, 15))

        deltas = []

        for idx, axis in enumerate(ax.flatten()):
            axis.hist(self.data[0][:, idx], bins=20, alpha=0.5, label='word')
            axis.hist(self.data[1][:, idx], bins=20, alpha=0.5, label='image')
            axis.set_title(f'Trial {idx}')

            w_mean = np.mean(self.data[0][:, idx])
            i_mean = np.mean(self.data[1][:, idx])
            delta = np.abs(round(w_mean - i_mean, 3))
            deltas.append(delta)

            axis.scatter((w_mean, i_mean), (10, 10), color='red')

            x_min, x_max = axis.get_xlim()
            xmin_frac = (w_mean - x_min) / (x_max - x_min)
            xmax_frac = (i_mean - x_min) / (x_max - x_min)
            axis.axhline(y=10, xmin=xmin_frac, xmax=xmax_frac, color="red", linestyle="--", label=r'$\Delta$ {}'.format(delta))

            axis.legend()

        plt.tight_layout()  
        plt.show()

        self.deltas = np.array(deltas)
        return self
    
def plot_deltas(d1:npt.ArrayLike, d2:npt.ArrayLike, labels:list[str]):
    """Plot deltas
    
    Parameters
    ----------
    d1 : npt.ArrayLike
    
    d2 : npt.ArrayLike

    labels : list[str]
        labels[0] is the label for d1, labels[1] is the label for d2
    """
    plt.plot(d1, marker='o', label=labels[0])
    plt.plot(d2, marker='o', label=labels[1])
    plt.title("$\\Delta$ in modality across trials and hypotheses")

    plt.xlabel("Trial")
    plt.ylabel("$\\Delta$")

    plt.legend()

    plt.show()