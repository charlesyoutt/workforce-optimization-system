"""
File: main.py
Description: Runs the workforce optimization system.
"""

import numpy as np
import pandas as pd
import random as rnd
import evo
import assignment_optimizer
from profiler import Profiler

def run_optimizer():
    # Load data
    tas_df, sections_df, availability = assignment_optimizer.load_data()

    # Create evolutionary framework
    E = evo.Evo()

    # Register agents
    E.add_agent("flip", assignment_optimizer.random_flip_agent)
    E.add_agent("fix_over", assignment_optimizer.fix_overallocation_agent)
    E.add_agent("fill_under", assignment_optimizer.fill_undersupport_agent)
    E.add_agent("prefer", assignment_optimizer.prefer_agent)

    # Register objective functions
    E.add_objective("overallocation", assignment_optimizer.overallocation)
    E.add_objective("conflicts", assignment_optimizer.conflicts)
    E.add_objective("undersupport", assignment_optimizer.undersupport)
    E.add_objective("unavailable", assignment_optimizer.unavailable)
    E.add_objective("unpreferred", assignment_optimizer.unpreferred)

    # Add initial solution
    init_sol = assignment_optimizer.generate_random_solution(tas_df, sections_df, availability)
    E.add_solution(init_sol)

    # Evolve with time limit (5 min)
    E.time_evolve(time_sec=300, dom=100)

    # Save final summary
    E.summarize("workforce")

    # Print profiling report
    Profiler.report()

if __name__ == "__main__":
    run_optimizer()
