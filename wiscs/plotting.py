from .simulate import DataGenerator
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from .methods import deltas, nearest_square_dims

class Plot(DataGenerator):
    def __init__(self, DG: DataGenerator):
        self.__dict__ = DG.__dict__.copy()
    
    def grid(self, **kwargs):
        """Plot grid of data distributions
        
        Parameters
        ----------
        kwargs: dict
            Keys: 'idx', 'question_idx'
        """

        if kwargs.get('idx') == 'participant':
            rows, cols = nearest_square_dims(self.params["n"]["participant"])
            fig, axs = plt.subplots(rows, cols, figsize=(cols*5, rows*5))

            for ax, i in zip(axs.flatten(), range(self.params["n"]["participant"])):
                ax.hist(self.data[0][i, :, :].ravel(), label='image', alpha=0.5)
                ax.hist(self.data[1][i, :, :].ravel(), label='word', alpha=0.5)
                ax.set_title(f'Participant {i+1}')

                ax.set_xlabel('RT')
                ax.set_ylabel('Frequency')

                ymax = (max(ax.get_ylim())/2).round(0)

                i_mean = self.data[0][i, :, :].ravel().mean()
                w_mean = self.data[1][i, :, :].ravel().mean()

                ax.scatter(i_mean, ymax, color='red', marker='o')
                ax.scatter(w_mean, ymax, color='red', marker='o')

                x_min, x_max = ax.get_xlim()
                xmin_frac = (w_mean - x_min) / (x_max - x_min)
                xmax_frac = (i_mean - x_min) / (x_max - x_min)
                ax.axhline(xmin=xmin_frac, xmax=xmax_frac, y=ymax, color='red', linestyle='--', label=r'$\Delta$ {}'.format(np.abs(i_mean - w_mean).round(2)))
                
                ax.legend()

            plt.show()
        
        elif kwargs.get('idx') == 'question':
            rows, cols = nearest_square_dims(self.params["n"]["question"])
            fig, axs = plt.subplots(rows, cols, figsize=(cols*5, rows*5))

            for ax, i in zip(axs.flatten(), range(self.params["n"]["question"])):
                ax.hist(self.data[0][:, i, :].ravel(), label='image', alpha=0.5)
                ax.hist(self.data[1][:, i, :].ravel(), label='word', alpha=0.5)
                ax.set_title(f'Question {i+1}')

                ax.set_xlabel('RT')
                ax.set_ylabel('Frequency')                

                i_mean = self.data[0][:, i, :].ravel().mean()
                w_mean = self.data[1][:, i, :].ravel().mean()

                ax.scatter(i_mean, 400, color='red', marker='o')
                ax.scatter(w_mean, 400, color='red', marker='o')

                x_min, x_max = ax.get_xlim()
                xmin_frac = (w_mean - x_min) / (x_max - x_min)
                xmax_frac = (i_mean - x_min) / (x_max - x_min)
                ax.axhline(xmin=xmin_frac, xmax=xmax_frac, y=400, color='red', linestyle='--', label=r'$\Delta$ {}'.format(np.abs(i_mean - w_mean).round(2)))
                
                ax.legend()
            plt.show()

        elif kwargs.get('idx') == 'trial':  
            rows, cols = nearest_square_dims(self.params["n"]["trial"])
            fig, axs = plt.subplots(rows, cols, figsize=(cols*5, rows*5))

            q = kwargs.get('question_idx')

            for ax, i in zip(axs.flatten(), range(self.params["n"]["trial"])):
                ax.hist(self.data[0][:, q, i].ravel(), label='image', alpha=0.5)
                ax.hist(self.data[1][:, q, i].ravel(), label='word', alpha=0.5)
                ax.set_title(f'Trial {i+1}')

                ax.set_xlabel('RT')
                ax.set_ylabel('Frequency')

                i_mean = self.data[0][:, q, i].ravel().mean()
                w_mean = self.data[1][:, q, i].ravel().mean()

                ax.scatter(i_mean, 400, color='red', marker='o')
                ax.scatter(w_mean, 400, color='red', marker='o')

                x_min, x_max = ax.get_xlim()
                xmin_frac = (w_mean - x_min) / (x_max - x_min)
                xmax_frac = (i_mean - x_min) / (x_max - x_min)
                ax.axhline(xmin=xmin_frac, xmax=xmax_frac, y=400, color='red', linestyle='--', label=r'$\Delta$ {}'.format(np.abs(i_mean - w_mean).round(2)))
                
                ax.legend()
            plt.show()

def plot_deltas(DG1:DataGenerator, DG2:DataGenerator, idx:str, labels:list[str]) -> None:
    """Plot deltas
    """
    plt.plot(deltas(DG1, idx), marker='o', label=labels[0])
    plt.plot(deltas(DG2, idx), marker='o', label=labels[1])
    plt.title("$\\Delta$ in modality across {} and hypotheses".format(idx.capitalize()))

    plt.xlabel(idx.capitalize())
    plt.ylabel("$\\Delta$")

    plt.legend()

    plt.show()