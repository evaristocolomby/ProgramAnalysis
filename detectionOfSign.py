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
        # left side
        "+": {
            # right side
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

def getVarName(la):
    if ("=" in la) and (not "==" in la):
        splitVar = la.split(" = ")[0]
    
        if "[" in splitVar:
            splitVar = splitVar.split("[")[0]
    
        if " " in splitVar:
            splitVar = splitVar.split(" ")[1]
        
        return splitVar

# Initialize datastructures
for i in range(1,len(flowGraphInput) + 1):
    node = flowGraphInput[i]
    l = node["label"]
    la = node["assignment"]

    varName = getVarName(la)
    
    if l in extremaLabels:
        # I am trying to use varibale names instead of l but I have this error: TypeError: unhashable type: 'list'
        analysis[l] = {}  
    else:
        analysis[l] = {} #emptyset (the bottom of the lattice)
        
        
    if varName is not None:
        variableNames.append(varName)
        #print varName
        #print "Variable Name in label ", i, variableNames
    
    for l_prime in node["destinations"]:
        pair = (l, l_prime)
        W.append(pair)
        
for i in range(1,len(flowGraphInput) + 1):
    for varName in variableNames:
        analysis[flowGraphInput[i]["label"]][varName] = Set(["0"]) 
        


# transfer function for n
def transfer(n):
    if n > 0:
        return Set(['+'])
    elif n < 0:
        return Set(['-'])
    elif n == 0:
        return Set(['0'])

# x is a variable
def transferX(varName, label):
    return analysis[label][varName]

# transfer function for array
def transferA(array, label):
    #TODO: Create this transfer function
    if np.sign(array) == 1:
        return '+'
    elif np.sign(array) == -1:
        return '-'
    elif np.sign(array) == 0:
        return '0'
        
def getType(split):
    if "[" in split[0]:
        return "array"
    else:
        try:
            firstVar = int(split[0])
            return "int"
        except Exception:
             return "variable"
        
    
def transferOP(split, label):    
    firstVar = None
    secondVar = None
    op = None

    
    # Good thing nobody is gonna do code review!
    if "[" in split[0]:
        firstVar = transferA(split[0], label)
    else:
        try:
             firstVar = transfer(int(split[0]))
        except Exception:
             firstVar = transferX(split[0], label)
         
    # if it is something like counter = counter + 1
    # or counter = counter + counter
    if "[" in split[2]:
        secondVar = transferA(split[2], label)
    else:
        try:
            # second part is an int
            secondVar = transfer(int(split[2]))
        except Exception:
            # second part is a variable
            secondVar = transferX(split[2], label)
        
    result = Set([])
      
    #TODO check for division by 0
    
    # Update the left hand variable for the current label in the
    # anaylsis's set of possible signs
    if firstVar != Set([]) and secondVar != Set([]):
        for lvar in firstVar:
            #print "lvar"
            #print lvar
            for rvar in secondVar:
                #print "rvar"
                #print rvar
                lookup = SignsTable[split[1]][lvar][rvar]
                #print "lookup"
                #print lookup
                result.update(Set([lookup]))
                #print "lvar",lvar , "rvar", rvar

    print "resutl"
    print result
    return result



# Using algorithm and doing detection of signs
while (len(W) > 0):
    #print "W"
    #print len(W)
    (l, l_prime) = W[0]
    W = W[1:]
    
    assi = flowGraphInput[l]["assignment"]
    
    #print "varname: " + str(varName)
    
    
    # We only care about signs if it is an assignment
    if ("=" in assi) and (not "==" in assi):
        varName = getVarName(flowGraphInput[l]["assignment"])
        l_analysis = analysis[l][varName]
        l_prime_analysis = analysis[l_prime][varName]
        # Are there two variables on the right hand side or 1?
        s2 = assi.split(" = ")[1].split(" ")
        if len(s2) > 2:
            # it is something like counter = counter + 1 
            f_l_set = transferOP(s2, l)
            print "fl"
            print f_l_set
            if not (f_l_set.issubset(l_prime_analysis)):
                if not (f_l_set == Set([])):
                    l_prime_analysis.update(f_l_set)
                    analysis[l_prime][varName] = l_prime_analysis
                    for nextNode in flowGraphInput[l_prime]["destinations"]:
                        W.append((l_prime, nextNode))
        else:
            varType = getType(s2)
            
            if varType == "array":
                print "array"
            elif varType == "int":
                f_l_set = transfer(s2[0])
                if not (f_l_set.issubset(l_prime_analysis)):
                    if not (f_l_set == Set([])):
                        l_prime_analysis.update(f_l_set)
                        analysis[l_prime][varName] = l_prime_analysis
                        for nextNode in flowGraphInput[l_prime]["destinations"]:
                            W.append((l_prime, nextNode))
                print "int"
            else:
                f_l_set = transferX(s2[0], l)
                if not (f_l_set.issubset(l_prime_analysis)):
                    if not (f_l_set == Set([])):
                        l_prime_analysis.update(f_l_set)
                        analysis[l_prime][varName] = l_prime_analysis
                        for nextNode in flowGraphInput[l_prime]["destinations"]:
                            W.append((l_prime, nextNode))
                print "variable"
        

    
   
          
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


