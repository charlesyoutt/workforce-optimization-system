### Workforce Optimization System

## Overview
I built this project to solve a realistic scheduling problem: assigning people to tasks while dealing with constraints like availability, coverage requirements, workload limits, and preferences. Instead of hard-coding rules, the system evaluates trade-offs and searches for better assignments over time.

The focus of this project is the system design and optimization logic, not producing one fixed output.

## What This Does
Given a set of workers and tasks, the system:
- Ensures required coverage is met
- Avoids assigning people when they’re unavailable
- Prevents workload overloads
- Tries to respect preferences when possible

Schedules are scored across multiple objectives, and the optimizer iteratively improves them rather than optimizing a single metric.

## How It’s Built
The project is organized into a few core components:

- assignment_optimizer.py — defines constraints, scoring functions, and how schedules are modified
- evo.py — a lightweight evolutionary optimization engine used to improve solutions
- main.py — runs the optimization end-to-end
- profiler.py — tracks performance during optimization

Supporting folders include input data, unit tests with small synthetic datasets, and past performance evaluation.

## Technical Concepts
This project touches a mix of system design and data-driven concepts, including:
- Multi-objective optimization
- Constraint modeling
- Heuristic / evolutionary search
- Modular Python design
- Testing with synthetic data
- Performance profiling

## Results
This system was evaluated in a competitive optimization setting and placed 2nd out of 60 groups based on overall schedule quality, including coverage, workload balance, and preference satisfaction.

## Why This Project Matters
Real scheduling problems are about balancing trade-offs, not finding a perfect answer. This project shows how to model those trade-offs cleanly and build a system that consistently produces strong solutions.
