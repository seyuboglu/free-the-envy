"""
Implements same algorithm described in http://procaccia.info/papers/rent.pdf.
"""

import numpy as np
import cvxopt
from cvxopt import matrix
from cvxopt.solvers import lp

from methods.lp_method import LPMethod


class MinMaxDemandMethod(LPMethod):
    """
    Implementation of the fairness splitting algorithm. 
    Example usage:
        valuations = get_valuations()
        method = FairnessMethod(valuations)
        self.assignemnts, self.prices = method.solve()
    """

    def __init__(self, valuations, verbosity=1):
        """
        Intializes the method. 
        args:
            valuations      (ndarray)   2D matrix of shape (n, n) where position (i, j)
                            gives the valuation of agent i for room j. 
            verbosity       (int)       0=no output, 1=step output, 2=solver output
        """
        super().__init__(valuations, verbosity)
        
    def solve_prices(self):
        """
        Assigns prices to the already assigned rooms by maximizing the minimum 
        utility of the agents. See http://procaccia.info/papers/rent.pdf for details on this
        optimization problem.  
        returns:
            self.prices         (ndarray)   1D array of prices. self.price[i]
                                is the price for room i. 
        """
        # objective function, minimum is stored at last index [-1]
        c = np.zeros((self.n + 1, 1))
        c[-1, 0] = 1

        # inqueality constraints
        all_G = []
        all_h = []

        # ensure minimumn is actually minimum
        for agent_id in range(self.n):
            assigned_room = self.assignments[agent_id]

            g = np.zeros(self.n + 1)
            g[-1] = -1
            g[assigned_room] = 1
            
            h = np.mean(self.valuations[:, assigned_room])

            all_G.append(g)
            all_h.append(h)
        
        # ensure envy-freeness 
        for agent_id in range(self.n):
            assigned_room = self.assignments[agent_id]
            for other_room in range(self.n):
                if other_room == assigned_room:
                    continue
                g = np.zeros(self.n + 1)
                g[assigned_room] = 1.0
                g[other_room] = -1.0

                h = (self.valuations[agent_id, assigned_room] - 
                     self.valuations[agent_id, other_room])
                
                all_G.append(g)
                all_h.append(h)
        G = np.stack(all_G, axis=0)
        h = np.stack(all_h, axis=0)

        # ensure prices sum to 1
        A = np.ones((1, self.n + 1))
        A[0, -1] = 0 
        b = np.ones((1, 1))

        # solve program
        solution = lp(matrix(c, tc='d'), matrix(G, tc='d'), 
                      matrix(h, tc='d'), matrix(A, tc='d'), 
                      matrix(b, tc='d'), solver='glpk')
        self.prices = np.array(solution['x']).squeeze()[:self.n]

        return self.prices