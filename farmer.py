from pulp import *

prob = LpProblem("Farmer", LpMaximize)

barley = LpVariable("barley", 0, None)
rice = LpVariable("rice", 0, None)

prob += 50 * barley + 20 * rice, "money for selling grain"
prob += barley + rice <= 100, "total size of fields"
prob += 5 * barley + 3 * rice <= 400, "available fertilizer"

prob.writeLP("farmer.lp")
prob.solve()

print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total income = ", value(prob.objective))
