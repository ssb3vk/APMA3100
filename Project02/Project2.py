import math
import statistics
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
from matplotlib.ticker import PercentFormatter

# Python3 implementation of the above approach
# Pulled from https://www.geeksforgeeks.org/linear-congruence-method-for-generating-pseudo-random-numbers/
 
# Function to generate random numbers
def linearCongruentialMethod(Xo, m, a, c, randomNums, noOfRandomNums):
    # Initialize the seed state
    randomNums[0] = Xo
 
    # Traverse to generate required
    # numbers of random numbers
    for i in range(1, noOfRandomNums):
        # Follow the linear congruential method
        randomNums[i] = ((randomNums[i - 1] * a) + c) % m

    for i in range(1, noOfRandomNums): 
        randomNums[i] = randomNums[i]/m

def inverseFunction(y): 
    #return 1 - math.exp(-1*y/12); 
    return -12 * math.log(1-y)

def probabilityCalculator(X, list): # a functoin for computing P[x < X]
    for i in range(1, len(list) ): 
        if (X < list[i]): 
            return (i - 1)/len(list); 
    
    #if X is greater than all values, then we simply return 1. 
    return 1;

 
# Driver Code
if __name__ == '__main__':    
    # Seed value
    Xo = 100000
    # Modulus parameter
    m = 32768 #set equal to 2^15
    # Multiplier term
    a = 24693
    # Increment term
    c = 3517

    realizations = 1000 #number of realizations to be defined here REALIZATIONS HERE
 
    # Number of Random numbers
    # to be generated
    noOfRandomNums = 4 * realizations # set this equal to realizations (or the other way around)
 
    # To store random numbers
    randomNums = [0] * (noOfRandomNums)
 
    # Function Call
    linearCongruentialMethod(Xo, m, a, c, randomNums, noOfRandomNums)

    # array to store samples
    times = [0] * (realizations)

    randomNumsIndex = 0; 
    for i in range(1, realizations): 
        callCounter = 1; 
        time = 0.0; 

        while callCounter <= 4:
            time+=6; 
            time += 1; 
            callCounter+=1;
            randomNumsIndex += 1; 

            u = randomNums[randomNumsIndex] #fetching the random number from our array 

            if (u <= 0.2): 
                time += 3; 
                continue; 
            elif (u <= 0.5): 
                time += 25; 
                continue; 
            else: 
                u_2 = (u - 0.5) * 2; 
                v = inverseFunction(u_2); 

                if ( v > 25 ): 
                    time += 25
                    continue; 
                else: 
                    time += v; 
                    break;             
        
        times[i] = time; 

    times10 = times[1:11]
    times100 = times[1:101]
    times.sort(key = int)
    times = times[1:1001]


    print("the mean of the data is: ")
    print(statistics.mean(times))
    print(statistics.quantiles(times))
    print(statistics.median(times))

    
    

    print(times[0])
    print(times[1])

    #for i in range(1, len(times)):
    #    print(times[i]); 

    print("Rnadom nums")
    print(randomNums[1])
    print(randomNums[2])
    print(randomNums[3])

    print(randomNums[51])
    print(randomNums[52])
    print(randomNums[53])


    print("P[x < mean] = ", end = '')
    print( probabilityCalculator(statistics.mean(times), times) )

    print("P[x < 15] = ", end = '')
    print( probabilityCalculator(15, times) )

    print("P[x < 20] = ", end = '')
    print( probabilityCalculator(20, times) )

    print("P[x < 30] = ", end = '')
    print( probabilityCalculator(30, times) )
    
    print("P[x > 40] = ", end = '')
    print( 1 - probabilityCalculator(40, times) )

    print("P[x > 70] = ", end = '')
    print (1 - probabilityCalculator(70, times))

    print("P[x > 100] = ", end = '')
    print (1 - probabilityCalculator(100, times))

    print("P[x > 120] = ", end = '')
    print (1 - probabilityCalculator(120, times))

    Wnp = np.array([[0, 15, 20, 30, 40, 70, 100, 120, 128], [0, probabilityCalculator(15, times), probabilityCalculator(20, times), probabilityCalculator(30, times), probabilityCalculator(40, times), probabilityCalculator(70, times), probabilityCalculator(100, times), probabilityCalculator(120, times), 1]])
    plt.plot(Wnp[0], Wnp[1], 'bo--')
    plt.xlabel("Time spent per customer (min)")
    plt.ylabel("CDF of Time taken")
    plt.title("Fig. 4: Cumulative Distribution Function of W")
    plt.show()

    plt.boxplot([times10, times100, times], notch=False, vert=False)
    plt.xlabel("Time spent per customer (min)")
    plt.yticks([1, 2, 3], ["10 realizations", "100 realizations", "1000 realizations"])
    plt.title("Fig. 1: Boxplots of time per customers for various realizations")
    #plt.show()

    # Creating histogram
    fig, axs = plt.subplots(1, 1,
                            figsize =(10, 7),
                            tight_layout = True)
    
    n_bins = 20

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        axs.spines[s].set_visible(False)
    
    # Remove x, y ticks
    axs.xaxis.set_ticks_position('none')
    axs.yaxis.set_ticks_position('none')
    
    # Add padding between axes and labels
    axs.xaxis.set_tick_params(pad = 5)
    axs.yaxis.set_tick_params(pad = 10)
    
    # Add x, y gridlines
    axs.grid(b = True, color ='grey',
            linestyle ='-.', linewidth = 0.5,
            alpha = 0.6)
    
    # Creating histogram
    N, bins, patches = axs.hist(times, bins = n_bins)
    
    # Setting color
    fracs = ((N**(1 / 5)) / N.max())
    norm = colors.Normalize(fracs.min(), fracs.max())
    
    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm(thisfrac))
        thispatch.set_facecolor(color)
    
    # Adding extra features   
    plt.xlabel("Time spent per customer (min)")
    plt.ylabel("Frequency")
    plt.title('Fig. 3: Histogram for Frequency of 100,000 Call Times')
    
    # Show plot
    plt.show()
    
    
    
    
    
