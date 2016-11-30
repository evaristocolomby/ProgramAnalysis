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
        "label": 1,
        "prev": []
    },
    2: {
        "destinations": [3],
        "assignment": "counter = 0",
        "label": 2,
        "prev": [1]
    },
    3: {
        "destinations": [4],
        "assignment": "int foo[10]",
        "label": 3,
        "prev": [2]
    },
    4: {
        "destinations": [5],
        "assignment": "1 < 2",
        "label": 4,
        "prev": [3, 6]
    },
    5: {
        "destinations": [6],
        "assignment": "counter = counter + 1",
        "label": 5,
        "prev": [4]
    },
    6: {
        "destinations": [7, 4],
        "assignment": "counter == 5",
        "label": 6,
        "prev": [5]
    },
    7: {
        "destinations": [8, 9],
        "assignment": "counter == 9",
        "label": 7,
        "prev": [6]
    },
    8: {
        "destinations": [4],
        "assignment": "foo[counter] = counter",
        "label": 8,
        "prev": [7]
    },
    9: {
        "destinations": [],
        "assignment": "int z",
        "label": 9,
        "prev": [7]
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

def isVar(l):
    try:
        test = int(l)
        return False
    except:
        return True
        
def getVarName(la):
    # if it is an assignment
    if ("=" in la) and (not "==" in la):
        splitVar = la.split(" = ")[0]
    
        if "[" in splitVar:
            splitVar = splitVar.split("[")[0]
    
        if " " in splitVar:
            splitVar = splitVar.split(" ")[1]
        
        if not isVar(splitVar):
                return
        
        return splitVar
    else:
        # we are gonna assume that only something like var == int is possible
        # not int == var
        if "==" in la:
            splitVar = la.split(" == ")[0]
        
            if "[" in splitVar:
                splitVar = splitVar.split("[")[0]
    
            return splitVar
        elif "int" in la or "void" in la:
            splitVar = la.split(" ")[1]
            if "[" in splitVar:
                splitVar = splitVar.split("[")[0]

            if not isVar(splitVar):
                return
    
            return splitVar
        # else it is a boolean expression like (1 < 2)
        # here we assume it is only possible to do counter < 2
        # not 2 < counter
        else:
            splitVar = la.split(" ")[0]
            if "[" in splitVar:
                splitVar = splitVar.split("[")[0]

            # there is no variable in the expression e.g. 1 < 2
            if not isVar(splitVar):
                return
    
            return splitVar


# Initialize datastructures
for i in range(1,len(flowGraphInput) + 1):
    node = flowGraphInput[i]
    l = node["label"]
    la = node["assignment"]

    varName = getVarName(la)
    
    if l in extremaLabels:
        analysis[l] = {}  
    else:
        analysis[l] = {} #emptyset (the bottom of the lattice)
        
        
    if varName is not None:
        variableNames.append(varName)
    
    for l_prime in node["destinations"]:
        pair = (l, l_prime)
        W.append(pair)
        
for i in range(1,len(flowGraphInput) + 1):
    for varName in variableNames:
        analysis[flowGraphInput[i]["label"]][varName] = Set(["0"]) 
        


# transfer function for n
def transfer(n):
    if int(n) > 0:
        return Set(['+'])
    elif int(n) < 0:
        return Set(['-'])
    elif int(n) == 0:
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

    if "[" in split[0]:
        firstVar = transferA(split[0], label)
    else:
        try:
             firstVar = transfer(int(split[0]))
        except Exception:
             firstVar = transferX(split[0], label)
         
    # if it is something like counter = counter + 1
    # or counter = counter * counter
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
    # result set of possible signs
    for lvar in firstVar:
        for rvar in secondVar:
            lookup = SignsTable[split[1]][lvar][rvar]
            result.update(Set([lookup]))

    return result


# Using algorithm and doing detection of signs
while (len(W) > 0):
    (l, l_prime) = W[0]
    W = W[1:]
    
    assi = flowGraphInput[l]["assignment"]
    
    
    if ("=" in assi) and (not "==" in assi):
        varName = getVarName(flowGraphInput[l]["assignment"])
        for l_o in flowGraphInput[l]["prev"]:
            for name in variableNames:
                analysis[l][name] = analysis[l_o][name]
        l_analysis = analysis[l][varName]
        l_prime_analysis = analysis[l_prime][varName]

        # Are there two variables on the right hand side or 1?
        s2 = assi.split(" = ")[1].split(" ")
        if len(s2) > 2:
            # it is something like counter = counter + 1 
            f_l_set = transferOP(s2, l)
            analysis[l][varName] = f_l_set
            if not (f_l_set.issubset(l_prime_analysis)):
                if not (f_l_set == Set([])):
                    l_prime_analysis.update(f_l_set)
                    analysis[l_prime][varName] = l_prime_analysis
                    if flowGraphInput[l_prime]["destinations"] == []:
                        for l_o in flowGraphInput[l_prime]["prev"]:
                            for name in variableNames:
                                analysis[l_prime][name] = analysis[l_o][name]
                        continue
                    for nextNode in flowGraphInput[l_prime]["destinations"]:
                        W.append((l_prime, nextNode))
        else:
            varType = getType(s2)
            
            if varType == "int":
                f_l_set = transfer(s2[0])
                analysis[l][varName] = f_l_set
                if not (f_l_set.issubset(l_prime_analysis)):
                    if not (f_l_set == Set([])):
                        l_prime_analysis.update(f_l_set)
                        analysis[l_prime][varName] = l_prime_analysis
                        analysis[l][varName] = f_l_set
                        if flowGraphInput[l_prime]["destinations"] == []:
                            for l_o in flowGraphInput[l_prime]["prev"]:
                                for name in variableNames:
                                    analysis[l_prime][name] = analysis[l_o][name]
                            continue
                        for nextNode in flowGraphInput[l_prime]["destinations"]:
                            W.append((l_prime, nextNode))
            else:
                f_l_set = transferX(s2[0], l)
                analysis[l][varName] = f_l_set
                if not (f_l_set.issubset(l_prime_analysis)):
                    if not (f_l_set == Set([])):
                        l_prime_analysis.update(f_l_set)
                        analysis[l_prime][varName] = l_prime_analysis
                        if flowGraphInput[l_prime]["destinations"] == []:
                            for l_o in flowGraphInput[l_prime]["prev"]:
                                for name in variableNames:
                                    analysis[l_prime][name] = analysis[l_o][name]
                            continue
                        for nextNode in flowGraphInput[l_prime]["destinations"]:
                            W.append((l_prime, nextNode))
                print "variable"
        

    else:
        # what comes out of the previous
        # label gets propagated here
        for l_o in flowGraphInput[l]["prev"]:
            for name in variableNames:
                analysis[l][name] = analysis[l_o][name]

        if flowGraphInput[l_prime]["destinations"] == []:
            for l_o in flowGraphInput[l_prime]["prev"]:
                for name in variableNames:
                    analysis[l_prime][name] = analysis[l_o][name]
            continue
       
    
   
          
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


