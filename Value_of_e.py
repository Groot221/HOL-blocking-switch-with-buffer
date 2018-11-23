import random
def createList(n):
    randNum = 0
    deckOfCard = range(1,n+1)
    numSelectList = {}
    for i in range(1, n+1):
        randNum = random.sample(deckOfCard, 1)
        if randNum[0] not in numSelectList:
            numSelectList[randNum[0]] = 0
        numSelectList[randNum[0]] = numSelectList[randNum[0]] + 1
    return numSelectList    

def probFinder(probDict):
    for key in probDict:
        val = probDict[key] 
        numberCount = [0] * key
        i = 0
        for a in range(1,key+1):
            if a in val:
                countVal =  val[a]

                numberCount[countVal] = numberCount[countVal] + 1
                probability = ((1.00/float(key))**val[a])* (((float(key)-1.00)/float(key))**(float(key)-float(val[a])))
                #print "Probability for a = %s is %s with number of outcomes = %s"% (a, probability, val[a])
            else:
                numberCount[0] = numberCount[0] + 1
                probability = ((float(key)-1.00)/float(key))**key
                #print "Probability for a = %s is %s with number of outcomes = %s"% (a, probability, 0)
        for val in numberCount:
            if i < 10:
                print "Probability that a card will be selected %s times in %s selections is %s"% (i, key, (float(val)/float(key)))
                i = i + 1



runs = [10,52,100,1000,10000]
#runs = [1000]
probDict = {}
for run in runs:
  #  for N in range(run):
    numSelect = createList(run)
    probDict[run] = numSelect

probFinder(probDict)
