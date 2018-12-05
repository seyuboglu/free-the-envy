"""
Implements same algorithm described in http://procaccia.info/papers/rent.pdf.
"""

import numpy as np
import cvxopt
from cvxopt import matrix
from cvxopt.solvers import lp
from cvxopt.glpk import ilp

from methods.lp_method import LPMethod


class PriorityMethod(LPMethod):
    """
    Implementation of the fairness splitting algorithm. 
    Example usage:
        valuations = get_valuations()
        method = FairnessMethod(valuations)
        self.assignemnts, self.prices = method.solve()
    """

    def __init__(self, valuations, priorities, verbosity=2):
        """
        Intializes the method. 
        args:
            valuations      (ndarray)   2D matrix of shape (n, n) where position (i, j)
                            gives the valuation of agent i for room j. 
            verbosity       (int)       0=no output, 1=step output, 2=solver output
        """
        super().__init__(valuations, verbosity)
        self.priorities = priorities
    
    def solve_assignments(self):
        """
        Assigns rooms to agents by solving a binary linear program that
        maximizes welfare. Uses the glpk binary lienar program solver. 
        See http://procaccia.info/papers/rent.pdf for details on this
        optimization problem.  
        returns:
            self.assignments    (ndarray)   1D array of assignments. 
                                self.assignments[i] is the assignment for 
                                agent with agent id i. 
        """
        # 
        scaled_valuations = self.valuations * 2 * self.priorities.reshape(-1, 1)

        # build valuations vector 
        c = -1 * scaled_valuations.flatten()

        # empty G and h, no inequality constraints
        G = np.zeros((1, self.n**2))
        h = np.zeros((1))

        # build A and b, enforces unique room-agent matching
        A = np.zeros((2 * self.n, self.n**2))
        b = np.ones((2 * self.n))
        for i in range(self.n):
            # exactly one room per agent
            A[i, i * self.n + np.arange(self.n)] = 1.0 
            # exactyly one agent per room
            A[self.n + i, (self.n) * np.arange(self.n) + i] = 1.0

        B = set(range(self.n**2))
        status, x = ilp(c=matrix(c, tc='d'), G=matrix(G, tc='d'), 
                        h=matrix(h, tc='d'), A=matrix(A, tc='d'), 
                        b=matrix(b, tc='d'), B=B)

        # get assignments
        x = np.argmax(np.array(x).reshape(self.n, self.n), axis=1)
        self.assignments = x 

        return self.assignments
        
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
            
            h = np.dot(self.valuations[:, assigned_room], 2 * self.priorities) / len(self.valuations)

            all_G.append(g)
            all_h.append(h)
        
        # ensure envy-freeness 
        for agent_id in range(self.n):
            assigned_room = self.assignments[agent_id]
            for other_room in range(self.n):
                if other_room == assigned_room:
                    continue
                g = np.zeros(self.n + 1)
                g[assigned_room] = 2.0 * (1 - self.priorities[agent_id])
                g[other_room] = -2.0 * (1 - self.priorities[agent_id])

                threshold = 0.1
                h = 2.0 * (self.priorities[agent_id] * self.valuations[agent_id, assigned_room] - 
                           self.priorities[agent_id] * self.valuations[agent_id, other_room] + 
                           threshold)
                #h = (self.valuations[agent_id, assigned_room] - 
                #     self.valuations[agent_id, other_room])
                
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