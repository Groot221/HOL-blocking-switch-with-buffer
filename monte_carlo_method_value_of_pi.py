import random
import math
import numpy as np
import scipy.stats as stats
import pylab as pl
import matplotlib.pyplot as plt

def withinCircle(x,y):
    if(x**2+y**2<1):
        return True
    else:
        return False
 
def valueOfPi(z):
    circleArea = 0
    squareArea = 0
    pi = 0
    percentagein = False
    for i in range(0,z):
        x = random.random()
        y = random.random()
        if(withinCircle(x,y)==1):
                   circleArea=circleArea+1
        squareArea=squareArea+1
    pi = 4.0*circleArea/squareArea
    print pi
    percentage_Variation = (math.pi-pi)/math.pi
    if percentage_Variation < 0.01 and percentage_Variation > -0.01:
           # print "Values for n = %s are within +- 1 percent of the exact value."% (z)
            percentagein = True
            
    #print "Approximate value for pi for n = %s is : %s and percentage variation with the exact value of pi: %s"% (z, pi, percentage_Variation)
    return pi, percentagein

piVal = []
boundCount = 0
percentageWithin = False
for i in range(9000,10000):
  pi, percentageWithin = valueOfPi(i)
  if percentageWithin:
    boundCount = boundCount + 1
  piVal.append(pi)

print boundCount
print "probability of pi within 1 percent : %f"% (float(boundCount)/float(1000))
mean = np.mean(piVal)
StdDiv = np.std(piVal)
print mean
print StdDiv
confidenceInterval_1 = (mean-(1.96*StdDiv/math.sqrt(1000)))
confidenceInterval_2 = (mean+(1.96*StdDiv/math.sqrt(1000)))
print "The confidence interval for N = %s is %s <= p^ <= %s\n" % (1000, confidenceInterval_1, confidenceInterval_2)
#PLOT THE NORMAL DISTRIBUTION
h = sorted(piVal)
fit = stats.norm.pdf(h, np.mean(h), np.std(h))
pl.plot(h,fit,'-o')
pl.hist(h,normed=True)
pl.show()
#PLOT OF SUCCESSIVE VALUES OF THE ESTIMATE AS THE NUMBER OF SAMPLES INCREASES
xAxis = range(9000, 10000)
plt.plot(xAxis, piVal)
plt.show()
