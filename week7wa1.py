# -*- coding: utf-8 -*-
from collections import namedtuple
from sets import Set

analysis = {}

# Flow Graph
flowGraphInput = {
    1: {
        "destinations": [2],
        "assignment": "int counter",
        "label": 1
    },
    2: {
        "destinations": [3],
        "assignment": "counter = 0",
        "label": 2
    },
    3: {
        "destinations": [4],
        "assignment": "int foo[10]",
        "label": 3
    },
    4: {
        "destinations": [5],
        "assignment": "1 < 2",
        "label": 4
    },
    5: {
        "destinations": [6],
        "assignment": "counter = counter + 1",
        "label": 5
    },
    6: {
        "destinations": [7, 4],
        "assignment": "counter === 5",
        "label": 6
    },
    7: {
        "destinations": [8, 9],
        "assignment": "counter === 9",
        "label": 7
    },
    8: {
        "destinations": [4],
        "assignment": "foo[counter] = counter",
        "label": 8
    },
    9: {
        "destinations": [],
        "assignment": "int z = 1",
        "label": 9
    },
}

# Extrema labels
extremaLabels = [1,9]

# Initial worklist
W = []

# KillRD and GenRD
killsets = {
   1: Set([("counter", 1), ("counter", 2), ("counter", 5)]),
   2: Set([("counter", 1), ("counter", 2), ("counter", 5)]),
   3: Set([("foo", 3), ("foo", 8)]),
   4: Set([]),
   5: Set([("counter", 1), ("counter", 2), ("counter", 5)]),
   6: Set([]),
   7: Set([]),
   8: Set([]),
   9: Set([("z", 9)])
}
gensets = {
   1: Set([("counter", 1)]),
   2: Set([("counter", 2)]),
   3: Set([("foo", 3)]),
   4: Set([]),
   5: Set([("counter", 5)]),
   6: Set([]),
   7: Set([]),
   8: Set([("foo", 8)]),
   9: Set([("z", 9)])
}


# Worklist algorithm for Reaching Definitions
for i in range(1,len(flowGraphInput) + 1):
    node = flowGraphInput[i]
    l = node["label"]
    for l_prime in node["destinations"]:
        pair = (l, l_prime)
        W.append(pair)

    if l in extremaLabels:
        analysis[l] = Set([]) #for RD it is the question mark
    else:
        analysis[l] = Set([]) #emptyset (the bottom of the lattice)
    
while len(W) > 0:
    (l, l_prime) = W[0]
    W = W[1:]
    
    l_analysis = analysis[l]
    l_prime_analysis = analysis[l_prime]

    # Transfer function applied
    l_analysis.difference_update(killsets[l])
    l_analysis.update(gensets[l])
    f_l_set = l_analysis

    if not (f_l_set.issubset(l_prime_analysis)):
        if not (f_l_set == Set([])):
            l_prime_analysis.update(f_l_set)
            analysis[l_prime] = l_prime_analysis
            for nextNode in flowGraphInput[l_prime]["destinations"]:
                W.append((l_prime, nextNode))
                   
print ""
print "1 " + str(analysis[1])
print "2 " + str(analysis[2])
print "3 " + str(analysis[3])
print "4 " + str(analysis[4])
print "5 " + str(analysis[5])
print "6 " + str(analysis[6])
print "7 " + str(analysis[7])
print "8 " + str(analysis[8])
print "9 " + str(analysis[9])