#Written By John Hofmeyr
#04/16/2022

from multiprocessing import Process, Value, Array, Manager
import time
import numpy as np
import matplotlib.pyplot as plt
import os

def genPrime(CPU_CORE, exec_time, exec_num, test_time, operation_time):
        D = {}
        q = 2 #Starting Prime number, the bigger this is, the slower it will run
        exec_index = 0 #Execution index, keeps track of how many times this code has run and how many primes have been found
        start = time.time() #Start measuring time
        while True:
            if q not in D:
                exec_start = time.time() #Start execution timer
                x = q**q**2  #This is the real CPU killer, x becomes a HUGE number really fast and it takes a lot of CPU power to calculate it
                D[q * q] = [q]
                exec_index += 1 #Add one to the execution count each time this is run. This will only run if a new prime has been found
                exec_end = time.time() #End Execution timer
                operation = operation_time[CPU_CORE] #Add the exectuion time as a row for the current operation to the 2D array
                operation.append(exec_end-exec_start)
                operation_time[CPU_CORE] = operation
            else:
                for p in D[q]:
                    D.setdefault(p + q, []).append(p)
                del D[q]
            q += 1
            end = time.time()

            # if CPU_CORE == 0: #If we are running core 0, print out the current status, used to make sure the program is running (it also looks nice :3)
            #     print("Running Prime Calculator on core #{}, iteration #{}, prime number: {} | Time: {:.5f}".format(CPU_CORE, exec_index, q, end-start), end = "\r")
            if end-start >= test_time: #If we have reached the desired time, record how many executions each CPU has done, how long it took, and end the loop
                exec_num[CPU_CORE] = exec_index
                exec_time[CPU_CORE] = end-start
                break

def timer(freeCore, totalCores, exec_time):
    runtime = 0
    while True:
        runtime += 0.01 #Simple and not very accurate, just used to display something while we wait for the test to run
        time.sleep(0.01)
        print("Running Prime Calculator on cores #{} - {} | Run Time: {:.2f} seconds | Time Left: {:.2f} seconds".format(freeCore+1, totalCores-1, runtime, exec_time - runtime), end = "\r")
        if runtime >= exec_time:
            break

def createProcess(core_Count):
    for i in range(core_Count): #For the specified number of cores, append that number to CPU_
         core.append("CPU_"+str(i))
         operation_time.append([0]) #Create a 2D array with as many elements as there are CPU cores to be tested

    for i in range(core_Count): #For each core value create a new process
        if i == 0:
            core[i] = Process(target = timer, args=(i, core_Count, test_time))  #Create a special Process on CPU_0 for keeping track of test run time
        else:
            core[i] = Process(target = genPrime, args=(i, exec_time, exec_num, test_time, operation_time)) #All other CPU cores can be used for the test

def start_and_run(core_Count):
    for i in range(core_Count): #Start each core process
        core[i].start()

    for i in range(core_Count): #Join each core process
        core[i].join()

def calculateAverage(core_Count, exec_num, exec_time):
    avg_Speed = 0
    for i in range(core_Count):
        if i != 0:  #Dont want to count CPU_0 since it was just keeping track of time
            avg_Speed += exec_num[i]/exec_time[i]   #Calculate average execution speed of each CPU core
    return(avg_Speed)

def plotPerformance(operation_time):
    figure = plt.figure() #Create figure

    for i in range(len(operation_time)): #Run For each element in the 2D operation time array
        if i != 0: #Again, ignore CPU_0
            elementLen = np.arange(0, len(operation_time[i]), 1) #Get the number of times recorded, each column of the operation time array corresponds to one CPU core, each row is the execution time, each index value for that row is the operation number
            plt.plot(elementLen, operation_time[i], linewidth=2, markersize=2, label = "CPU {}".format(i)) #Plot all that good data
    plt.xlabel("Number of Operations Executed")
    plt.ylabel("Time to Execute one Operation (seconds)")
    plt.title("CPU Performance: Time per Operation vs Number of Operations")
    plt.legend()
    plt.show()

def printCoreData(core_Count, exec_num, exec_time):
    for i in range(core_Count): #Print out the execution time and process count for each core
        if i != 0:
            print("CPU {} executed {} operations in {:.5f} seconds | Core Score: {:.2f}".format(i, exec_num[i], exec_time[i], (exec_num[i]/exec_time[i])))

def readCoreInput(totalCoreCount):
    while True: #Makes sure you can only enter the right number of cores
        try:
            core_Count = int(input("Enter The Number of CPU Cores to test, Min of 1, Max of {}: ".format(totalCoreCount-1))) + 1
            if (core_Count <= totalCoreCount) and (core_Count >= 2):
                break
            else:
                print("Number of CPU cores entered is invalid. Please Try again")
        except ValueError:
            print("Error, entered core count higher than available cores.")

    return(core_Count)

def readTimeInput():
    timer = 0
    while True: #Makes sure you can only enter the time as a number or type default
        try:
            test_time = str(input("Enter Test Duraton (seconds) or type 'Default' for defualt 60s test time: "))
            if test_time == "Default":
                timer = 60
                break
            elif test_time != "Default" and int(test_time)==False:
                print("Invalid input. Please enter the test duaration in seconds or enter 'Default' for default 60s test time.")
            else:
                timer = int(test_time)
                break
        except ValueError:
            print("Invalid input. Please enter the test duaration in seconds or enter 'Default' for default 60s test time.")

    return(timer)

if __name__ == "__main__":
    totalCoreCount = os.cpu_count()
    test_time = readTimeInput()
    numCores = readCoreInput(totalCoreCount)

    exec_time = Array('d', range(numCores)) #1D Array of total execution time for each core
    exec_num = Array('i', range(numCores))  #1D Array of the number of operations run by each core
    core = []  #Array of Cores
    manager = Manager()
    operation_time = manager.list() #Array of execution times

    createProcess(numCores) #Create each core test process based on the number of cores selected
    print("Running Prime Number Generator Benchmark. Benchmark Time is: {} seconds".format(test_time))
    time.sleep(0.5)
    start_and_run(numCores) #Start and run each core test Process
    print("")
    printCoreData(numCores, exec_num, exec_time) #Print out the number of executions and time taken for each tested core
    print("Total CPU Score: {:.2f}".format(calculateAverage(numCores, exec_num, exec_time)))
    plotPerformance(operation_time) #Plot the performance of each core as a function of time/operation vs number of operations
