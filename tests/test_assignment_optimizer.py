import numpy as np
from assignment_optimizer import overallocation, conflicts, undersupport, unavailable, unpreferred

def load(path):
    return np.loadtxt(path, delimiter=",", dtype=int)

def test_overallocation():
    assert overallocation(load("tests/data/test1.csv")) == 34
    assert overallocation(load("tests/data/test2.csv")) == 37
    assert overallocation(load("tests/data/test3.csv")) == 19

def test_conflicts():
    assert conflicts(load("tests/data/test1.csv")) == 7
    assert conflicts(load("tests/data/test2.csv")) == 5
    assert conflicts(load("tests/data/test3.csv")) == 2

def test_undersupport():
    assert undersupport(load("tests/data/test1.csv")) == 1
    assert undersupport(load("tests/data/test2.csv")) == 0
    assert undersupport(load("tests/data/test3.csv")) == 11

def test_unavailable():
    assert unavailable(load("tests/data/test1.csv")) == 59
    assert unavailable(load("tests/data/test2.csv")) == 57
    assert unavailable(load("tests/data/test3.csv")) == 34

def test_unpreferred():
    assert unpreferred(load("tests/data/test1.csv")) == 10
    assert unpreferred(load("tests/data/test2.csv")) == 16
    assert unpreferred(load("tests/data/test3.csv")) == 17
