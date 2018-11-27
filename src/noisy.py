
"""
"""
import os

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

from methods.fairness import UtilityFairnessMethod, PriceFairnessMethod
from utils import Process


class NoisySimulation(Process):
    
    def __init__(self, dir):
        super().__init__(dir)
    
    def get_starting_valuations(self):
        """
        """
        uniform = np.ones(self.n) / self.n
        mean = self.perturb_valuations(uniform, self.mean_scale)
        valuations = np.stack([self.perturb_valuations(mean, self.initial_scale) 
                               for i in range(self.n)], axis=0).squeeze()
        return valuations
    
    def is_envy_free(self, valuations, assignments, prices, epsilon=1e-5):
        """
        """
        for agent_id in range(self.n):
            assigned_room = assignments[agent_id]
            agent_valuations = valuations[agent_id, :].squeeze()
            for other_room in range(self.n):
                if assigned_room == other_room:
                    continue
                assigned_diff = agent_valuations[assigned_room] - prices[assigned_room]
                other_diff = agent_valuations[other_room] - prices[other_room]
                if assigned_diff + epsilon < other_diff:
                    return False
        return True 
    
    def perturb_valuations(self, valuations, scale=10):
        """
        Perturbs a valuations vector, with a dirichlet distribution with alpha equal to 
        args:
            valuations (ndarray)
            scale   (int) the scale for the dirichlet distribution. The larger it is the lower 
                        the variance.
        """
        valuations = valuations.reshape(-1, self.n)
        perturbed_valuations = np.zeros_like(valuations)
        for i in range(valuations.shape[0]):
            perturbed_valuations[i, :] = np.random.dirichlet(valuations[i, :] * scale)
        return perturbed_valuations

    def simulate_split(self, method_class, noise_scale):
        """
        """
        valuations = self.get_starting_valuations()
        noisy_valuations = self.perturb_valuations(valuations, noise_scale)
        method = method_class(noisy_valuations, verbosity=0) 
        assignments, prices = method.solve()
        return valuations, assignments, prices

    def run(self):
        """
        """
        self.noise_scales = np.logspace(self.scale_range[0], 
                                        self.scale_range[1], 
                                        num=self.scale_samples)
        self.fractions = {}
        for method_name in self.methods: 
            assert(method_name in globals())
            method_class = globals()[method_name] 
            fractions = []
            for noise_scale in self.noise_scales:
                count_ef = 0
                for i in range(self.num_samples):
                    valuations, assignments, prices = self.simulate_split(method_class,
                                                                          noise_scale)
                    if self.is_envy_free(valuations, assignments, prices):
                        count_ef += 1
                frac_envy_free = count_ef / self.num_samples
                fractions.append(frac_envy_free)
            self.fractions[method_name] = fractions

        self.visualize()
    
    def visualize(self):
        """
        """
        for method_name, fractions in self.fractions.items(): 
            plt.plot(self.noise_scales, fractions, label=method_name)
            plt.legend()

        figures_dir = os.path.join(self.dir, "figures")
        if not os.path.exists(figures_dir):
            os.makedirs(figures_dir)
        
        plt.savefig(os.path.join(figures_dir, "simulation.pdf"))
        

        
                

        

