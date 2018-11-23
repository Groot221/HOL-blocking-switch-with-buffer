import random
import collections
import numpy as np
import itertools
from discreteMarkovChain import markovChain

def transition_matrix(transitions, k):
    n = k #number of states

    M = [[0]*n for _ in range(n)]

    for (i,j) in zip(transitions,transitions[1:]):
        M[i][j] += 1

    #now convert to probabilities:
    for row in M:
        s = sum(row)
        if s > 0:
            row[:] = [float(f)/float(s) for f in row]
    return M

def probRange(n):
    alphaL = [0] * (n+1)
    alphai = 1.0/n
    incAlpha = 0
    for a in range(n+1):
        alphaL[a] = incAlpha
        incAlpha = incAlpha + alphai
    return alphaL

def repeated_op(inp):
    return [item for item, count in collections.Counter(inp).items() if count > 1]

def Head_of_line(n, inpList):
    
    #input list to the switch
    #print "Input list before the cycle: ", inpList
    opList = [0] * n
    #differents outputs
    rangee = range(1, n+1, 1)

    #send the values to the outputs which have only one input -- 
    # which wants repeated outputs -- 
    repeatedOP = repeated_op(inpList)

    #Empty singly mapped i/o o/p ie they have been sent to O/P --
    for i,j in enumerate(inpList):
        if j not in repeatedOP:
            opList[j-1] = i+1
            inpList[i] = 0
    #Use RNG to decide which repeated I/P to transition to O/P
    cnt = 0
    listRepeat = {}
    for inp in inpList:
        if inp != 0 and inp not in listRepeat:
            listRepeat[inp] = [k for k, y in enumerate(inpList) if y == inp]

    #print "repeated numbers location in the list : %s "% listRepeat

    for b in listRepeat:
        p = probRange(len(listRepeat[b]))
        
        #p = lambda listRepeat: probRange(listRepeat) if len(listRepeat) != 0 else 0
        #print "probability division for repeated number %s, = %s"%(b ,p)
        #Gen rand number to decide which to select
        ran = random.random()
        #compare the ran with p and listRepeat and remove that value from input list
        #print "input list and output list state", inpList, opList
        propagate = np.digitize(ran, p)
        #print "number to be propagated, ran", propagate, ran
        
        # np is the location of the number in the input list which needs to be delivered to the output
        prop = listRepeat[b][propagate-1]
        opList[inpList[prop]-1] = prop +1
        inpList[prop] = 0
        #opList = 
        #print "prop",prop

         

    #print "input and output values after a cycle: ",inpList, opList
    return inpList, opList

inp = [2, 3, 4]
traffic = [2, "balanced", "unbalanced"]
#traffic = [2, "balanced", "unbalanced"]
for i in inp:
    inRangeMatrix = []
    states = i**i
    print "start for number or input output switch:%s \n"% i
    # create a n x n matrix transition matrix
    #tMatrix = [[0 for x in range(states)] for y in range(states)]
    
    rangee = range(1, i+1, 1)
    inpListTemp = []
    inMatrixTemp = []
    rangeinpList = []
    portEfficiencies = []
    for inp in rangee:
        #list inpList = list(i) wants to go to the particular output
        #initial input value
        inpListTemp.append(random.choice(rangee))
    #print "input List = ",inpList
    
    #values after each cycle
    for traff in traffic:

        outPutEfficiency = [0] * i
        inRangeMatrix = []
        #for n = 2 and alpha = [0, 0.1,0.2,0.3,0.4,0.5]
        if traff == 2 and inp == 2:
            #alpha1 = [0]
            alpha1 = [0.1, 0.2, 0.3, 0.4, 0.5]
            for al in alpha1:
                inMatrixTemp = []
                slots = 10000
                outPutEfficiency = [0] * i
                for a in range(slots):
                     
                    inMatrixTemp.append(inpListTemp[:])
                    inList, outList = Head_of_line(i, inpListTemp[:])
                    #get the number of 0's and their location
                    
                    for z, nul in enumerate(inList):
                        if nul == 0:
                            ranChoice = random.random()
                            if ranChoice < al:
                                inList[z] = 1
                            else:
                                inList[z] = 2
                            #choose according to different values of alpha
                    for e,f in enumerate(outList): #Increment which output port got the packet
                        if f != 0:
                            outPutEfficiency[e] = outPutEfficiency[e] + 1
                    inpListTemp = inList
                portEfficiencies = [l / float(slots) for l in outPutEfficiency]
                print "Efficiency of each port for n = %s alpha = %s: %s \n"% (i, al, portEfficiencies)
                inRangeMatrix.append(inMatrixTemp[:])


        #For Balanced Traffic alpha = 1/n
        elif traff == "balanced" and inp != 2:
            inMatrixTemp = []
            slots = 100000
            outPutEfficiency = [0] * i
            for a in range(slots):
                inMatrixTemp.append(inpListTemp)
                inList, outList = Head_of_line(i, inpListTemp[:])
                for z, nul in enumerate(inList):
                    if nul == 0:
                        inList[z] = random.choice(rangee)   
                inpListTemp = inList
                for e,f in enumerate(outList): #Increment which output port got the packet
                        if f != 0:
                            outPutEfficiency[e] = outPutEfficiency[e] + 1
            portEfficiencies = [l / float(slots) for l in outPutEfficiency]
            print "Efficiency of each port for n = %s traffic = %s: %s \n"% (i, traff, portEfficiencies)
            inRangeMatrix.append(inMatrixTemp)
            

        elif traff == "unbalanced" and inp != 2: #unbalanced traffic alpha1 = 1/k alphaj = (1/n-1)(k-1/k)
            kList = range(2, i+1, 1)
            print kList
            #kList = [4]
            for kk in kList:
                inMatrixTemp = []
                alphaL = [0]
                alphaL.append(1.0/kk)
                qVal = (1.0/(i-1))*((kk-1)/float(kk))

                for g in range(i-1):
                    alphaL.append(alphaL[g+1] + qVal)
                print "probability bins: ",alphaL
                slots = 100000
                outPutEfficiency = [0] * i
                for a in range(slots): #10^6 slots per second
                    inMatrixTemp.append(inpListTemp[:])
                    inList, outList = Head_of_line(i, inpListTemp[:])
                    for z, nul in enumerate(inList):
                        if nul == 0:
                            rand = random.random()
                            inList[z] = int(np.digitize(rand, alphaL))
                    inpListTemp = inList
                    for e,f in enumerate(outList): #Increment which output port got the packet
                        if f != 0:
                            outPutEfficiency[e] = outPutEfficiency[e] + 1
                portEfficiencies = [l / float(slots) for l in outPutEfficiency] 
                print "Efficiency of each port for n = %s traffic = %s, alpha1= %s: %s \n"% (i, traff, alphaL[1] , portEfficiencies)
                inRangeMatrix.append(inMatrixTemp[:])

    
            #for a in inList:
            #    if a == 0:
        for inMatrix in inRangeMatrix:
            #print inMatrix
            RangeOfInputs = range(1, i+1)
            cartesianProduct = list(itertools.product(RangeOfInputs, repeat = i))
            #print cartesianProduct
            efficiancyMatrix = [] #has info about what combination has what OP
            stateThroughputCount = 0
            #calculate throughput multiplier for each state using the cartesian product
            for throu in cartesianProduct:
                stateThroughputCount = 0
                rep = repeated_op(list(throu))
                for thr in list(throu):
                    if thr not in rep:
                        stateThroughputCount = stateThroughputCount + 1
        
                stateThroughputCount = stateThroughputCount + len(rep)
                efficiancyMatrix.append(stateThroughputCount)
                #print stateThroughputCount, throu
        
            
           # print efficiencyMatrix, cartesianProduct
                        
            relationShipList = []
            #map from cartesian product to the input list and store as a list of transitions
            for inMat in inMatrix:
                for d, lis in enumerate(cartesianProduct):
                    if lis == tuple(inMat):
                        relationShipList.append(d)
                        
                #i, lis = [(i, lis) for i, lis in enumerate(cartesianProduct) if lis == inMat]
                #print i, lis
            tMatrix = transition_matrix(relationShipList, len(cartesianProduct))
            numPYArray = np.array(tMatrix)
            mc = markovChain(numPYArray)
            mc.computePi('linear') 
            print "PI values: ", mc.pi    
            print "sum of all pi values", sum(mc.pi)
            

            if i == 2:
                for row in tMatrix: print(' '.join('{0:.2f}'.format(x) for x in row))
            #print "relationShipList", relationShipList
        
            #to calculate the overall efficiancy of the switch, multiply the pi values with its corresponding efficiancyMatrix values
            efficiancyOfTheSwitch = sum([a*b for a,b in zip(mc.pi,efficiancyMatrix)])
            print "efficiency of the switch for N = %s is : %s \n"% (i, efficiancyOfTheSwitch)
