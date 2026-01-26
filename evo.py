"""
File: evo.py
Description: A simple evolutionary optimization engine that searches for
             better solutions across multiple competing objectives.
"""


import random as rnd
import copy
from functools import reduce
import time
import pandas as pd

class Evo:

    def __init__(self):
        """framework constructor"""
        self.pop = {}
        self.fitness = {}
        self.agents = {}

    def add_objective(self, name, f):
        """ Register a new objective for evaluating solutions """
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        """ Register an agent take works on k input solutions """
        self.agents[name] = (op, k)

    def get_random_solutions(self, k=1):
        """ Picks k random solutions from the population
        and returns them as a list of deep-copies """
        if len(self.pop) == 0:
            return []
        else:
            solutions = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(solutions)) for _ in range(k)]


    def add_solution(self, sol):
        """ Adds the solution to the current population.
        Added solutions are evaluated wrt each registered objective. """

        # Create the evaluation key
        # key:  ( (objname1, objvalue1), (objname2, objvalue2), ...... )
        
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])

        # Add to the dictionary
        self.pop[eval] = sol


    def run_agent(self, name):
        """ Invoking a named agent against the current population """
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)


    @staticmethod
    def _dominates(p, q):
        """ p = evaluation of solution: ((obj1, score1), (obj2, score2), ... )"""
        pscores = [score for _,score in p]
        qscores = [score for _,score in q]
        score_diffs = list(map(lambda x,y: y-x, pscores, qscores))
        min_diff = min(score_diffs)
        max_diff = max(score_diffs)
        return min_diff >= 0.0 and max_diff > 0.0

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Evo._dominates(p,q)}

    def remove_dominated(self):
        """ Remove solutions from the pop that are dominated (worse) compared
        to other existing solutions. This is what provides selective pressure
        driving the population towards the pareto optimal tradeoff curve. """
        nds = reduce(Evo._reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k:self.pop[k] for k in nds}


    def evolve(self, n=1, dom=100, status=1000):
        """ Run the framework (start evolving solutions)
        n = # of random agent invocations (# of generations) """

        agent_names = list(self.agents.keys())
        for i in range(n):
            pick = rnd.choice(agent_names)  # pick an agent to run
            self.run_agent(pick)
            if i % dom == 0:
                self.remove_dominated()
            if i % status == 0:
                self.remove_dominated()
                print("Iteration: ", i)
                print("Population size: ", len(self.pop))
                print(self)

        self.remove_dominated()


    def __str__(self):
        """ Output the solutions in the population """
        rslt = ""
        for eval,sol in self.pop.items():
            rslt += str(dict(eval))+":\t"+str(sol)+"\n"
        return rslt

    def time_evolve(self, time_sec=300, dom=100):
        """
        Run the functions for a fixed amount of seconds.

        Params:
        time_sec (int): Maximum number of seconds to run the evolution loop.
        dom (int): How often to remove dominated solutions
        """

        agents = list(self.agents.keys())
        start_time = time.time()

        i = 0
        while time.time() - start_time < time_sec:
            # pick a random agent to evolve the pop
            pick = rnd.choice(agents)
            self.run_agent(pick)

            # remove the dominated solutions every dom interval
            if i % dom == 0:
                self.remove_dominated()

            i += 1

        self.remove_dominated()

    def summarize(self, name):
        """
        Save the results of the non-dominated population to a CSV file.

        Params:
        name (str): The name of your team.
        """

        # make list of rows where each row contains the name followed by the evaluation score
        rows = []
        for eval in self.pop.keys():
            row = [name]
            row += [score for _, score in eval]
            rows.append(row)

        # make a df and export it to a csv
        df = pd.DataFrame(rows, columns=[
            "name", "overallocation", "conflicts", "undersupport", "unavailable", "unpreferred"
        ])
        df.to_csv(f"{name}_summary.csv", index=False)




