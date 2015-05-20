#!/usr/bin/env python

from pulp import *
import csv

votes = {}
actual_seats = {}
total_votes = 0.0
with open('election.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        score = int(row["Total votes"])
        votes[row["Party"]] = score
        actual_seats[row["Party"]] = row["Total MPs"]
        total_votes += score

expected = {party: 650*score/total_votes for party, score in votes.items()}

prob = LpProblem("UK general election 2015", LpMinimize)

# We minimize sum(abs(seats - expected_seats)) using a trick described at
# http://lpsolve.sourceforge.net/5.5/absolute.htm
bounds = []
seat_vars = {}
for party in votes:
    seats = LpVariable("{}_seats".format(party), 0, 650, LpInteger)
    bound = LpVariable("{}_bound".format(party), 0, 650)
    diff = seats - expected[party]
    prob += diff <= bound
    prob += -diff <= bound
    bounds.append(bound)
    seat_vars[party] = seats

prob += lpSum(seat_vars.values()) == 650
prob += lpSum(bounds)

prob.solve()

print("Status:", LpStatus[prob.status])
results = [(party, v.varValue) for party, v in seat_vars.items()]
results.sort(key=lambda x:-x[1])
for result in results:
    party = result[0]
    print("{:.2f}\t{}\t{}\t{}".format(
        expected[party], int(result[1]), actual_seats[party], party))
print("Error = ", value(prob.objective))
