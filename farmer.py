#!/usr/bin/env python

from pulp import *

prob = LpProblem("Farmer", LpMaximize)

barley = LpVariable("barley", 0, None)
rice = LpVariable("rice", 0, None)

prob += 300 * barley + 250 * rice, "money for selling grain"
prob += barley + rice <= 100, "total size of fields"
prob += 5 * barley + 3 * rice <= 400, "available fertilizer"

prob.writeMPS("farmer.mps")
prob.solve()

print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total income = ", value(prob.objective))
