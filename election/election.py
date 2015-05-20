#!/usr/bin/env python

from pulp import *
import csv

votes = {}
total_votes = 0.0
with open('election.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        score = int(row["Total votes"])
        votes[row["Party"]] = score
        total_votes += score

expected = {party: 650*score/total_votes for party, score in votes.items()}

for party, score in expected.items():
    print("{} => {}".format(party, score))

prob = LpProblem("UK general election 2015", LpMinimize)

# We minimize sum(abs(seats - expected_seats)) using a trick described at
# http://lpsolve.sourceforge.net/5.5/absolute.htm
bounds = []
seat_vars = []
for party in votes:
    seats = LpVariable("{}_seats".format(party), 0, 650, LpInteger)
    bound = LpVariable("{}_bound".format(party), 0, 650)
    diff = seats - expected[party]
    prob += diff <= bound
    prob += -diff <= bound
    bounds.append(bound)
    seat_vars.append(seats)

prob += lpSum(bounds)

prob.solve()

print("Status:", LpStatus[prob.status])
results = [(v.name, v.varValue) for v in seat_vars]
print(sorted(results, key=lambda x:-x[1]))
print("Error = ", value(prob.objective))
