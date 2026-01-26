"""
File: assignment_optimizer.py
Description: Contains the core logic for the workforce assignment problem,
             including constraints, scoring rules, and operators used to
             improve schedules.
"""

import numpy as np
import pandas as pd
import random as rnd
from profiler import profile

# load the data
tas_df = pd.read_csv("data/tas.csv")
sections_df = pd.read_csv("data/sections.csv")

# get data from the dataframes
max_assigned = tas_df["max_assigned"].values
availability = tas_df.iloc[:, 3:].values
min_ta = sections_df["min_ta"].values
daytimes = sections_df["daytime"].values

# make the objective functions
@profile
def overallocation(schedule):
    total_assigned = schedule.sum(axis=1)
    over_assigned = np.maximum(0, total_assigned - max_assigned)
    return over_assigned.sum()

@profile
def conflicts(schedule):
    time_to_sections = {}
    for sec_idx, time in enumerate(daytimes):
        time_to_sections.setdefault(time, []).append(sec_idx)

    conflict_count = 0
    for ta_idx in range(schedule.shape[0]):
        ta_row = schedule[ta_idx]
        for time, overlapping_secs in time_to_sections.items():
            if ta_row[overlapping_secs].sum() > 1:

                conflict_count += 1
                break

    return conflict_count

@profile
def undersupport(schedule):
    ta_count_per_section = schedule.sum(axis=0)
    missing_tas = np.maximum(0, min_ta - ta_count_per_section)
    return missing_tas.sum()

@profile
def unavailable(schedule):
    return np.sum((availability == 'U') & (schedule == 1))

@profile
def unpreferred(schedule):
    return np.sum((availability == 'W') & (schedule == 1))

# make the agent functions
@profile
def random_flip_agent(solutions):
    schedule = solutions[0].copy()
    ta = rnd.randint(0, schedule.shape[0] - 1)
    sec = rnd.randint(0, schedule.shape[1] - 1)
    schedule[ta, sec] = 1 - schedule[ta, sec]

    return schedule

@profile
def fix_overallocation_agent(solutions):
    schedule = solutions[0].copy()
    for ta in range(schedule.shape[0]):
        assigned_sections = np.where(schedule[ta] == 1)[0]
        if len(assigned_sections) > max_assigned[ta]:

            to_remove = rnd.sample(list(assigned_sections), len(assigned_sections) - max_assigned[ta])
            schedule[ta, to_remove] = 0

    return schedule

@profile
def fill_undersupport_agent(solutions):
    schedule = solutions[0].copy()
    current_section_support = schedule.sum(axis=0)

    for sec in np.where(current_section_support < min_ta)[0]:
        needed = min_ta[sec] - current_section_support[sec]
        eligible_tas = []

        for ta in range(schedule.shape[0]):
            if (availability[ta, sec] in ('W', 'P') and schedule[ta, sec] == 0 and schedule[ta].sum() < max_assigned[ta]):
                eligible_tas.append(ta)

        if len(eligible_tas) >= needed:
            selected = rnd.sample(eligible_tas, needed)
            for ta in selected:
                schedule[ta, sec] = 1
    return schedule

@profile
def prefer_agent(solutions):
    schedule = solutions[0].copy()
    for ta in range(schedule.shape[0]):
        for sec in range(schedule.shape[1]):
            if schedule[ta, sec] == 1 and availability[ta, sec] == 'W':
                better_sec = np.where((availability[ta] == 'P') & (schedule[ta] == 0))[0]
                if len(better_sec):

                    new_sec = rnd.choice(better_sec)
                    schedule[ta, sec] = 0
                    schedule[ta, new_sec] = 1
                    break

    return schedule

# function to load the data
def load_data():
    return tas_df, sections_df, availability

# function to make the initial random solution
def generate_random_solution(tas_df, sections_df, availability):
    num_tas, num_sections = availability.shape
    schedule = np.zeros((num_tas, num_sections), dtype=int)

    for ta in range(num_tas):
        available_sections = np.where(availability[ta] != 'U')[0]
        limit = min(max_assigned[ta], len(available_sections))
        if limit > 0:
            selected_sections = rnd.sample(list(available_sections), limit)
            schedule[ta, selected_sections] = 1

    return schedule
