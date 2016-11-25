# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 15:32:47 2016

@author: 
"""

#from collections import namedtuple
import numpy as np
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
        "assignment": "counter == 5",
        "label": 6
    },
    7: {
        "destinations": [8, 9],
        "assignment": "counter == 9",
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

SignsTable = {
    # Plus    
    "+": {
        "+": {
            "+":"+" ,
            "-":"+,-,0",
            "0":"+"
        },
        "-": {
            "+":"0,-,+" ,
            "-":"-",
            "0":"-"
        },
        "0": {
            "+":"+" ,
            "-":"-",
            "0":"0"
        }
    },
    # Minus    
    "-": {
        "+": {
            "+":"+,0,-" ,
            "-":"-,+,0",
            "0":"+"
        },
        "-": {
            "+":"-" ,
            "-":"-,0,+",
            "0":"-"
        },
        "0": {
            "+":"-" ,
            "-":"+",
            "0":"0"
        }
    },
    # multiplication    
    "*": {
        "+": {
            "+":"+" ,
            "-":"-",
            "0":"0"
        },
        "-": {
            "+":"-" ,
            "-":"+",
            "0":"0"
        },
        "0": {
            "+":"0" ,
            "-":"0",
            "0":"0"
        }
    },
    # division    
    "/": {
        "+": {
            "+":"+" ,
            "-":"-",
            "0":"0"
        },
        "-": {
            "+":"-" ,
            "-":"+",
            "0":"0"
        },
        "0": {
            "+":"ø" ,
            "-":"ø",
            "0":"ø"
        }
    },
        
}

# Extrema labels
extremaLabels = [1,9]

# Initial worklist
W = []

variableNames = []

# Worklist algorithm for Detection of sign analysis
for i in range(1,len(flowGraphInput) + 1):
    node = flowGraphInput[i]
    l = node["label"]

    if "=" in node["assignment"] and not "==" in node["assignment"]:
            splitVar = node["assignment"].split(" = ")[0]
            if splitVar not in variableNames:
                variableNames.append(splitVar)
                print "Variable Name in label ", i, variableNames
    
    for l_prime in node["destinations"]:
        pair = (l, l_prime)
        W.append(pair)
    
    
    if l in extremaLabels:
        # I am trying to use varibale names instead of l but I have this error: TypeError: unhashable type: 'list'
        analysis[l] = Set([]); 
    else:
        analysis[l] = Set([]) #emptyset (the bottom of the lattice)
        
        

# transfer function for n
def transfer(n):
    if np.sign(n) == 1:
        return '+'
    elif np.sign(n) == -1:
        return '-'
    elif np.sign(n) == 0:
        return '0'


# x is the label of a node
def transferX(x):
    return analysis[x]
        
    
def transferOP(node):
    splitLHS = node["assignment"].split(" = ")[0]
    splitRHS = node["assignment"].split(" = ")[1]
    # counter + 1
    # counter = a + 1
        
    # ['1']
    # ['counter', '+', '1']
    split = splitRHS.split(" ")
    
    firstVar = None
    secondVar = None
    op = None

    try:
         firstVar = transfer(int(split[0]))
    except Exception:
         firstVar = transferX(split[0])
         
    # if it is something like counter = counter + 1
    if(len(split) > 1):
        try:
            secondVar = transfer(int(split[2]))
        except Exception:
            secondVar = transferX(split[2])
            
        result = Set([])
            
        for lvar in firstVar:
            for rvar in secondVar:
                split[1]
                print "lvar",lvar , "rvar", rvar
                
        analysis[splitLHS].update(result)
        
    # if it is something like counter = 1
    else:
        analysis[splitLHS].update(firstVar)


# transfer function for array
def transferA(array):
    if np.sign(array) == 1:
        return '+'
    elif np.sign(array) == -1:
        return '-'
    elif np.sign(array) == 0:
        return '0'



    
while len(W) > 0:
    (l, l_prime) = W[0]
    W = W[1:]
    
    l_analysis = analysis[l]
    l_prime_analysis = analysis[l_prime]
    
    
    
for i in range(1,len(flowGraphInput) + 1):
    node = flowGraphInput[i]
    
    if "=" in node["assignment"] and not "==" in node["assignment"]:
        #print "I want to update the sign ", node["assignment"]
        
        transferOP(node)
        
        
        #split = node["assignment"].split(" = ")[1]
        #print split, "split is "
        #analysis[node["label"]].update(transfer())
        #z.add("+")
        #print z
    else:
        continue
    
    
'''
    if not (f_l_set.issubset(l_prime_analysis)):
        if not (f_l_set == Set([])):
            l_prime_analysis.update(f_l_set)
            analysis[l_prime] = l_prime_analysis
            for nextNode in flowGraphInput[l_prime]["destinations"]:
                W.append((l_prime, nextNode))
    else:
        continue
        
'''



'''
                   
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

'''
