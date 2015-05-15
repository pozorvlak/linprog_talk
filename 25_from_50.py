from pulp import *

prob = LpProblem("25 from 50", LpMinimize)

variables = [LpVariable(i, 0, 1, LpInteger) for i in range(1, 51)]

prob += sum([i * variables[i] for i in range(0, 50)])
prob += lpSum([variables]) == 25, "pick 25 numbers"

for i in range(0, 50):
    for j in range(2 * (i+1), 50, i + 1):
        prob += variables[i] + variables[j] <= 1, "{} divides {}".format(i+1, j)

prob.writeLP("25_from_50.lp")
prob.solve()

print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
winners = [v.name for v in variables if v.varValue == 1]
print(winners)
print("Sum = ", value(prob.objective))
