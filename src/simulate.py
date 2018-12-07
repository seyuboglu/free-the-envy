
"""
"""
import logging
import os

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 

from methods.priority import PriorityMethod
from methods.price import MaxMinPriceMethod, MinMaxPriceMethod
from methods.utility import MaxMinUtilityMethod
from methods.demand import MinMaxDemandMethod
from utils import Process


class Simulation(Process):
    
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
    
    def get_starting_priorities(self):
        """
        """
        return np.random.uniform(0, 1, size=self.n)

    def simulate_split(self, method_class, valuations, priorities):
        """
        """
        method = method_class(valuations, priorities, verbosity=0) 
        assignments, prices = method.solve()
        return valuations, priorities, assignments, prices

    def run(self):
        """
        """
        self.fractions = {}
        for method_name in self.methods: 
            assert(method_name in globals())
            method_class = globals()[method_name] 
            fractions = []
            count_no_soln = 0
            for i in range(self.num_samples):
                valuations = self.get_starting_valuations()
                priorities = self.get_starting_priorities()
                try:
                    valuations, priorities, assignments, prices = self.simulate_split(method_class, valuations, priorities)
                except:
                    logging.info("No Solution-")
                    logging.info(valuations)
                    logging.info(priorities)
                    logging.info("-----------------")

                    count_no_soln += 1
                
            frac_no_soln= count_no_soln / self.num_samples
            fractions.append(frac_no_soln)
            self.fractions[method_name] = fractions
        print(self.fractions)
    
    def visualize(self):
        """
        """
        sns.set_style("whitegrid")
        for method_name, fractions in self.fractions.items(): 
            plt.plot(self.noise_scales[::-1], fractions[::-1], label=method_name)
            plt.legend()
            plt.xscale(self.x_scale)

        figures_dir = os.path.join(self.dir, "figures")
        if not os.path.exists(figures_dir):
            os.makedirs(figures_dir)
        
        plt.savefig(os.path.join(figures_dir, "simulation.pdf"))
        

        
                

        

