import random
import collections
import numpy as np
import itertools
import matplotlib.pyplot as plt
import scipy.stats as stats
import pylab as pl

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

inp = [ 8]

#100% load
throughputDictFromProject4 = {
        2: [0.55425, 0.61455, 0.68015, 0.7305, 0.7485], 
        4: {    "balanced": 0.65497, 
               "unbalanced": [0.49372, 0.63262, 0.65518]   },
        8: {"balanced": 0.6184375,    
               "unbalanced": [0.24909, 0.37425125, 0.4924, 0.57409125, 0.6052675, 0.61697125, 0.61879625] 
            }    
            }

#70% load
#throughputDictFromProject4 = {
#        2: [0.387975, 0.430185, 0.476105, 0.51135, 0.52395],
#        4: {    "balanced": 0.458479,
#               "unbalanced": [0.345604, 0.442834, 0.458626]   },
#        8: {"balanced": 0.43290625,
#               "unbalanced": [0.174363, 0.261975875, 0.34468, 0.401863175, 0.42368725, 0.431879875, 0.433157375]
#            }
#            }

traffic = ["unbalanced"]
#traffic = [2, "balanced", "unbalanced"]

Percentage_P_Arrival = 0.90

print "The values below are calculated for %s percent of the maximum throughput" % (Percentage_P_Arrival*100)


for i in inp:
    print "start for number or input output switch:%s \n"% i
    # create a n x n matrix transition matrix
    #tMatrix = [[0 for x in range(states)] for y in range(states)]
    
    rangee = range(1, i+1, 1)
    inpListTemp = []
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
            for seqAlpha, al in enumerate(alpha1):

                #queue at the input ports
                #queue = [[0]*10]*i
                totalPackets = 0
                HOLdelay = [[0] for _ in range(i)]
                queue = [[0]*10 for _ in range(i)]
                outPutEfficiency = [0] * i
                overflow = [0]*i
                slots = 100000

                #delays based on the output port
                nodeIqueueStat = [0] * i
                nodeIHOLStat = [0] * i

                queueStat = [[] for _ in range(i)]
                for a in range(slots):
                
                    inList, outList = Head_of_line(i, inpListTemp[:])
                    
                    #add to queue wrt P_arrival according to the throughputs calculated in project 4
                    ranChoice = random.random()
                    #ranChoice = 0.1
                    if ranChoice < (throughputDictFromProject4[i][seqAlpha] * Percentage_P_Arrival):
                        totalPackets = totalPackets + 1
                        blah = queue[:]
                        for seq, que in enumerate(blah):
                            queueStat[seq].append(len(queue[seq])-queue[seq].count(0))
                            for inseq, q in enumerate(que):
                                
                                #increment the value of that queue delay for the port i
                                if q != 0:
                                    nodeIqueueStat[q-1] = nodeIqueueStat[q-1] + 1

                                if q == 0:
                                    ranChoice = random.random()
                                    if ranChoice < al:
                                        queue[seq][inseq] = 1
                                    else:
                                        queue[seq][inseq] = 2
                                    break;
                                elif inseq == (len(que)-1):
                                    overflow[seq] = overflow[seq] + 1 
                                    break;
                                
                   #get the number of 0's and remove values from queue and add to the HOL input
                    for z, nul in enumerate(inList):

                        #queueStat[z].append(len(queue[z])-queue[z].count(0))
                        if nul == 0:
                            HOLdelay[z].append(0)
                            inList[z] = queue[z][0]
                            del queue[z][0]
                            queue[z].append(0)
                        else:
                            nodeIHOLStat[nul-1] = nodeIHOLStat[nul-1] + 1
                            HOLdelay[z][-1] = HOLdelay[z][-1] + 1 
                        
                    #choose according to different values of alpha
                    inpListTemp = inList
                    for e,f in enumerate(outList): #Increment which output port got the packet
                        if f != 0:
                            outPutEfficiency[e] = outPutEfficiency[e] + 1
                
                portEfficiencies = [l / float(slots) for l in outPutEfficiency]
                print "Throughput of each port for n = %s alpha = %s: %s"% (i, al, portEfficiencies)
                print "Throughput of the switch: %s and the efficiency: %s"% (sum(portEfficiencies), sum(portEfficiencies)/i)
                print "overflows occured in each of the queues: %s"% overflow
                for pri, prin in enumerate(queueStat):

                    print "output statistics"
                    lambdaa = float(totalPackets)
                    
                    meanIHOLStat = float(nodeIHOLStat[pri])/slots
                    AWT_HOL = float(meanIHOLStat)/(lambdaa-overflow[pri])
#                    print "Average wait time of a packet which wants to go to port %s in the HOL is: %s" % (pri, AWT_HOL)
                    meanIqueueStat = float(nodeIqueueStat[pri])/slots
                    AWT_QUEUE = float(meanIqueueStat)/(lambdaa-overflow[pri])
                    print "Average wait time of a packet which wants to go to port %s in the queue is: %s" % (pri, AWT_QUEUE)
                    print "Average wait time of a packet which wants to go to port %s in the HOL is: %s" % (pri, AWT_HOL)
                    print "The average total wait time using input statistics: %s seconds\n" % (AWT_HOL + AWT_QUEUE)

                    print "Input statistics"
                    meanQ = np.mean(prin)

                    #using Little's result N = lambda * T and lambda = Totalpackets/10**-6
                    #lambdaa = float(totalPackets)/float(totalPackets-overflow[pri])
                    #time an average packet spends in the system 
                    AvgPacTime = float(meanQ)/lambdaa
                    print "The mean queue length of the system for i: %s, port number: %s is : %s\n The value of lambda is %s packets/sec and avg packet time in queue is: %s seconds"% (i, pri, meanQ, lambdaa, AvgPacTime)
                    #calculate the HOL delay
                    AvgHOLwaitSlots = np.mean(HOLdelay[pri])
                    AvgHOLwaitTime = AvgHOLwaitSlots/lambdaa
                    print "The Average wait time at the input due to HOL blocking: %s micro sec and the average total wait time i.e HOL delay + queue delay: %s seconds \n"% (AvgHOLwaitTime, (AvgHOLwaitTime + AvgPacTime))
                    
 #                   plt.figure(1)
 #                   plt.subplot(211)
 #                   plt.plot(prin)
 #                   
 #                   plt.subplot(212)
 #                   n, bins, patches = plt.hist(x=prin, bins=10, color='#0504aa')
 #                   plt.xlabel('Value')
 #                   plt.ylabel('Frequency')
                    #plt.show()
                print "\n\n"
                

        #For Balanced Traffic alpha = 1/n
        elif traff == "balanced" and inp != 2:
            queue = [[0]*10 for _ in range(i)]
            overflow = [0]*i
            slots = 100000
            totalPackets = 0
            HOLdelay = [[0] for _ in range(i)]
            queueStat = [[] for _ in range(i)]
            outPutEfficiency = [0] * i

            #delays based on the output port
            nodeIqueueStat = [0] * i
            nodeIHOLStat = [0] * i
            for a in range(slots):
                inList, outList = Head_of_line(i, inpListTemp[:])

                #add to queue wrt P_arrival according to the throughputs calculated in project 4
                ranChoice = random.random()
                    #ranChoice = 0.1
                if ranChoice < (throughputDictFromProject4[i]["balanced"] * Percentage_P_Arrival):
                    totalPackets = totalPackets + 1
                    blah = queue[:]
                    for seq, que in enumerate(blah):
                        queueStat[seq].append(len(queue[seq])-queue[seq].count(0))
                        for inseq, q in enumerate(que):
                            
                            #increment the value of that queue delay for the port i
                            if q != 0:
                                nodeIqueueStat[q-1] = nodeIqueueStat[q-1] + 1

                            if q == 0:
                                queue[seq][inseq] = random.choice(rangee)
                                break;
                            elif inseq == (len(que)-1):
                                overflow[seq] = overflow[seq] + 1
                                break;
                for z, nul in enumerate(inList):


                    #queueStat[z].append(len(queue[z])-queue[z].count(0))
                    if nul == 0:
                        HOLdelay[z].append(0)
                        inList[z] = queue[z][0]
                        del queue[z][0]
                        queue[z].append(0)
                    else:
                        nodeIHOLStat[nul-1] = nodeIHOLStat[nul-1] + 1
                        HOLdelay[z][-1] = HOLdelay[z][-1] + 1

                inpListTemp = inList
                for e,f in enumerate(outList): #Increment which output port got the packet
                        if f != 0:
                            outPutEfficiency[e] = outPutEfficiency[e] + 1
            portEfficiencies = [l / float(slots) for l in outPutEfficiency]
            print "Throughput of each port for n = %s traffic = %s: %s"% (i, traff, portEfficiencies)
            print "Throughput of the switch: %s and the efficiency: %s"% (sum(portEfficiencies), sum(portEfficiencies)/i)
            print "overflows occured in each of the queues: %s "% overflow
            for pri, prin in enumerate(queueStat):

                print "output statistics"
                lambdaa = float(totalPackets)

                meanIHOLStat = float(nodeIHOLStat[pri])/slots
                AWT_HOL = float(meanIHOLStat)/lambdaa
#                print "Average wait time of a packet which wants to go to port %s in the HOL is: %s" % (pri, AWT_HOL)
                meanIqueueStat = float(nodeIqueueStat[pri])/slots
                AWT_QUEUE = float(meanIqueueStat)/lambdaa
                print "Average wait time of a packet which wants to go to port %s in the queue is: %s" % (pri, AWT_QUEUE)
                print "Average wait time of a packet which wants to go to port %s in the HOL is: %s" % (pri, AWT_HOL)
                print "The average total wait time using input statistics: %s seconds\n" % (AWT_HOL + AWT_QUEUE)

                print "Input statistics"

                meanQ = np.mean(prin)
                print meanQ, meanIqueueStat, len(prin)
                    #using Little's result N = lambda * T and lambda = Totalpackets/10**-6
                #lambdaa = float(totalPackets)/float(slots)
                    #time an average packet spends in the system 
                AvgPacTime = float(meanQ)/(lambdaa-overflow[pri])
                print "The mean queue length of the system for i: %s, port number: %s is : %s\n The value of lambda is %s and avg packet time in queue is: %s micro seconds"% (i, pri, meanQ, lambdaa, AvgPacTime)

                #calculate the HOL delay
                AvgHOLwaitSlots = np.mean(HOLdelay[pri])
                AvgHOLwaitTime = AvgHOLwaitSlots/(lambdaa-overflow[pri])
                print "The Average wait time at the input due to HOL blocking: %s micro sec and the average total wait time i.e HOL delay + queue delay: %s seconds \n"% (AvgHOLwaitTime, (AvgHOLwaitTime + AvgPacTime))
            #    plt.figure(1)
            #        plt.subplot(211)
            #        plt.plot(prin)
#
#                    plt.subplot(212)
#                    n, bins, patches = plt.hist(x=prin, bins=10, color='#0504aa')
#                    plt.xlabel('Value')
#                    plt.ylabel('Frequency')
#                    plt.show()
            print "\n\n"

        elif traff == "unbalanced" and inp != 2: #unbalanced traffic alpha1 = 1/k alphaj = (1/n-1)(k-1/k)
            kList = range(2, i+1, 1)
            print kList
            #kList = [4]
            for kk in kList:
                alphaL = [0]
                alphaL.append(1.0/kk)
                qVal = (1.0/(i-1))*((kk-1)/float(kk))

                for g in range(i-1):
                    alphaL.append(alphaL[g+1] + qVal)
                print "probability bins: ",alphaL
                slots = 100000
                
                HOLdelay = [[0] for _ in range(i)]
                queueStat = [[] for _ in range(i)]
                queue = [[0]*50 for _ in range(i)]
                outPutEfficiency = [0] * i
                totalPackets = 0
                overflow = [0]*i
                #delays based on the output port
                nodeIqueueStat = [0] * i
                nodeIHOLStat = [0] * i

                for a in range(slots): #10^6 slots per second
                    inList, outList = Head_of_line(i, inpListTemp[:])

                    #add to queue wrt P_arrival according to the throughputs calculated in project 4
                    ranChoice = random.random()
                    #ranChoice = 0.1
                    if ranChoice < (throughputDictFromProject4[i]["unbalanced"][kk-2] * Percentage_P_Arrival):
                        totalPackets = totalPackets + 1 
                        blah = queue[:]
                        for seq, que in enumerate(blah):
                            queueStat[seq].append(len(queue[seq])-queue[seq].count(0))
                            for inseq, q in enumerate(que):

                                #increment the value of that queue delay for the port i
                                if q != 0:
                                    nodeIqueueStat[q-1] = nodeIqueueStat[q-1] + 1

                                if q == 0:
                                    rand = random.random()
                                    queue[seq][inseq] = int(np.digitize(rand, alphaL))
                                    break;
                                elif inseq == (len(que)-1):
                                    overflow[seq] = overflow[seq] + 1
                                    break;


                    for z, nul in enumerate(inList):

                       # queueStat[z].append(len(queue[z])-queue[z].count(0))
                        if nul == 0:
                            HOLdelay[z].append(0)
                            inList[z] = queue[z][0]
                            del queue[z][0]
                            queue[z].append(0)
                        else:
                            nodeIHOLStat[nul-1] = nodeIHOLStat[nul-1] + 1
                            HOLdelay[z][-1] = HOLdelay[z][-1] + 1

                    inpListTemp = inList
                    for e,f in enumerate(outList): #Increment which output port got the packet
                        if f != 0:
                            outPutEfficiency[e] = outPutEfficiency[e] + 1
                portEfficiencies = [l / float(slots) for l in outPutEfficiency] 
                print "Throughput of each port for n = %s traffic = %s, alpha1= %s: %s"% (i, traff, alphaL[1] , portEfficiencies)
                print "Throughput of the switch: %s and the efficiency: %s"% (sum(portEfficiencies), sum(portEfficiencies)/i)
                print "overflows occured in each of the queues: %s"% overflow
                for pri, prin in enumerate(queueStat):
                    
                    print "output statistics"
                    lambdaa = float(totalPackets)

                    meanIHOLStat = float(nodeIHOLStat[pri])/slots
                    AWT_HOL = float(meanIHOLStat)/lambdaa
#                    print "Average wait time of a packet which wants to go to port %s in the HOL is: %s" % (pri, AWT_HOL)
                    meanIqueueStat = float(nodeIqueueStat[pri])/slots
                    AWT_QUEUE = float(meanIqueueStat)/lambdaa
                    print "Average wait time of a packet which wants to go to port %s in the queue is: %s" % (pri, AWT_QUEUE)
                    print "Average wait time of a packet which wants to go to port %s in the HOL is: %s" % (pri, AWT_HOL)
                    print "The average total wait time using input statistics: %s seconds\n" % (AWT_HOL + AWT_QUEUE)

                    print "Input statistics"

                    meanQ = np.mean(prin)
                    #using Little's result N = lambda * T and lambda = Totalpackets/10**-6
                    #lambdaa = float(totalPackets)/float(slots)
                    #time an average packet spends in the system
                    AvgPacTime = float(meanQ)/(lambdaa-overflow[pri])
                    print "The mean queue length of the system for i: %s, port number: %s is : %s\n The value of lambda is %s and avg packet time in queue is: %s micro seconds"% (i, pri, meanQ, lambdaa, AvgPacTime)

                    #calculate the HOL delay
                    AvgHOLwaitSlots = np.mean(HOLdelay[pri])
                    AvgHOLwaitTime = AvgHOLwaitSlots/(lambdaa-overflow[pri])
                    print "The Average wait time at the input due to HOL blocking: %s micro sec and the average total wait time i.e HOL delay + queue delay: %s seconds \n"% (AvgHOLwaitTime, (AvgHOLwaitTime + AvgPacTime))

                    
                    if i == 8:
                        plt.figure(1)
                        plt.subplot(211)
                        plt.plot(prin, "r-")

                        plt.subplot(212)
                        n, bins, patches = plt.hist(x=prin, bins=10, color='r')
                        plt.xlabel('Value')
                        plt.ylabel('Frequency')
                        plt.show()
                print "\n\n"
