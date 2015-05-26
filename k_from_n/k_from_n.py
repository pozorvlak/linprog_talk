#!/usr/bin/env python

from pulp import *
from sys import argv

""" Pick k numbers from {1,...,n} such that none divides another. """

k = int(sys.argv[1])
n = int(sys.argv[2])
prob = LpProblem("{} from {}".format(k, n), LpMinimize)

variables = [LpVariable("i{}".format(i), 0, 1, LpInteger)
             for i in range(1, n + 1)]

prob += sum([(i+1) * variables[i] for i in range(0, n)])
prob += lpSum([variables]) == k, "pick {} numbers".format(k)

for i in range(0, n):
    for j in range(2 * i + 1, n, i + 1):
        prob += variables[i] + variables[j] <= 1, \
            "{} divides {}".format(i+1, j+1)

prob.solve()

print("Status:", LpStatus[prob.status])
winners = [v.name for v in variables if v.varValue == 1]
print(winners)
print("Sum = ", value(prob.objective))
