"""
Defines a class for managing a rent splitting problem
"""

import os

import numpy as np
from cvxopt import solvers
import pandas as pd

from methods.price import MaxMinPriceMethod, MinMaxPriceMethod
from methods.utility import MaxMinUtilityMethod
from methods.demand import MinMaxDemandMethod
from methods.priority import PriorityMethod
from utils import Process

class SplitCli(Process):
    """
    Holds one instance of a rent splitting problem parameterized
    by a dict describing the problem.
    Example:
    {
        "n": 3,
        "total_rent": 1000,
        "method":

        "agent_to_valuations": {
            "Sabri": [200, 300, 500],
            "Kye": [150, 250, 600],
            "KiJung": [300, 300, 400]
        }
    }
    """

    def __init__(self, dir):
        """
        Initializes splitting instance.
        args:
        params  (dict)  of form described above.
        """
        super().__init__(dir)
        self.solved = {}
        self.preprocess_valuations()
        self.results = {}

    def output_results(self):
        """
        Outputs solutions of the rent splitting problem.
        TODO: work for any number of solution calls.
        """
        assert(self.solved)
        result = list(self.results.values())[0]
        assignments = result["assignments"]
        data = [{"agent": agent,
                 "room": assignments[i],
                 "valuation": self.valuations[i, assignments[i]] * self.total_rent,
                 #"utility": ((self.valuations[i, assignments[i]] -
                 #            prices[assignments[i]]) *
                 #            self.total_rent),
                 "all_valuations": self.valuations[i, :] * self.total_rent}
                 for i, agent in enumerate(self.agents)]
        columns = ["agent", "room", "valuation", "all_valuations"]
        for method, result in self.results.items():
            assignments = result["assignments"]
            prices = result["prices"]
            for i, agent in enumerate(self.agents):
                data[i][f"price_{method}"] = prices[assignments[i]] * self.total_rent
            columns.append(f"price_{method}")
        df = pd.DataFrame(data, columns=columns)
        print(df)
        df.to_csv(os.path.join(self.dir, "results.csv"))

    def run(self):
        """
        """
        for method in self.methods:
            assert(method in globals())
            method_class = globals()[method]
            self.solve(method_name=method, method_class=method_class)
            self.output_results()

    def preprocess_valuations(self):
        """
        Preprocesses valuations by converting to ndarray and normalizing
        so valuations sum to 1.
        """
        # ensure correct length
        assert(len(self.agent_to_valuations) == self.n)
        for agent, v in self.agent_to_valuations.items():
            assert(np.sum(v) == self.total_rent)
            assert(len(v) == self.n)

        valuations = []
        self.priorities = np.full(len(self.agent_to_valuations), 0.5)
        agents = []
        for i, (agent, curr_valuations) in enumerate(self.agent_to_valuations.items()):
            # scale between 0 and 1
            valuations.append(np.array(curr_valuations) / self.total_rent)
            agents.append(agent)
            if hasattr(self, "agent_to_priority"):
                self.priorities[i] = self.agent_to_priority[agent]

        self.valuations = np.stack(valuations, axis=0)
        self.agents = agents

        return self.agents, self.valuations

    def solve(self,
              method_name="MaxMinUtilityMethod",
              method_class=MaxMinUtilityMethod):
        """
        Solves the splitting instance with the specified method.
        args:
            method_class    (class) a class of Method type.
        TODO: implement base method class
        """
        if method_name == "PriorityMethod":
            method = method_class(self.valuations, self.priorities)
        else:
            method = method_class(self.valuations)
        assignments, prices = method.solve()
        self.results[method_name] = {"assignments": assignments,
                                     "prices": prices}
        self.solved[method_name] = True


class Split():
    """
    Holds one instance of a rent splitting problem parameterized
    by a dict describing the problem.
    Example:
    {
        "n": 3,
        "total_rent": 1000,
        "method":

        "agent_to_valuations": {
            "Sabri": [200, 300, 500],
            "Kye": [150, 250, 600],
            "KiJung": [300, 300, 400]
        }
    }
    """

    def __init__(self, params):
        """
        Initializes splitting instance.
        args:
        params  (dict)  of form described above.
        """
        self.__dict__.update(params)
        self.solved = False
        self.preprocess_valuations()

    def get_results(self):
        """
        """
        assert(self.solved)
        data = {agent:
                {"room": int(self.assignments[i]),
                 "price": self.prices[self.assignments[i]] * self.total_rent,
                 "valuation": self.valuations[i, self.assignments[i]] * self.total_rent,
                 "utility": ((self.valuations[i, self.assignments[i]] -
                              self.prices[self.assignments[i]]) *
                              self.total_rent)}
                for i, agent in enumerate(self.agents)}
        return data

    def output_results(self):
        """
        Outputs solutions of the rent splitting problem.
        TODO: work for any number of solution calls.
        """
        assert(self.solved)
        data = [{agent: {
                 "room": self.assignments[i],
                 "price": self.prices[self.assignments[i]] * self.total_rent,
                 "valuation": self.valuations[i, self.assignments[i]] * self.total_rent,
                 "utility": ((self.valuations[i, self.assignments[i]] -
                              self.prices[self.assignments[i]]) *
                             self.total_rent)}}
                for i, agent in enumerate(self.agents)]

        df = pd.DataFrame(data, columns=["agent", "room",
                                          "price", "valuation",
                                          "utility"])
        print(df)

    def run(self):
        """
        """
        assert(self.method in globals())

        method_class = globals()[self.method]
        self.solve(method_class=method_class)
        self.output_results()

    def preprocess_valuations(self):
        """
        Preprocesses valuations by converting to ndarray and normalizing
        so valuations sum to 1.
        """
        # ensure correct length
        assert(len(self.agent_to_valuations) == self.n)
        for agent, v in self.agent_to_valuations.items():
            assert(np.sum(v) == self.total_rent)
            assert(len(v) == self.n)

        valuations = []
        agents = []
        for agent, curr_valuations in self.agent_to_valuations.items():
            # scale between 0 and 1
            valuations.append(np.array(curr_valuations) / self.total_rent)
            agents.append(agent)

        self.valuations = np.stack(valuations, axis=0)
        self.agents = agents

        return self.agents, self.valuations

    def solve(self, method_class=MaxMinUtilityMethod):
        """
        Solves the splitting instance with the specified method.
        args:
            method_class    (class) a class of Method type.
        TODO: implement base method class
        """
        method = method_class(self.valuations)
        self.assignments, self.prices = method.solve()
        self.solved = True
