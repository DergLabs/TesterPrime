# TesterPrime
This code is bad and unoptimized 

This is a simple python program that will run a performance/stress test on your CPU.
This program works by running a prime number generator. After each prime number (q) is found, the program will then calculate q^(qxq). 
By performing this last computation, a massively large number is created that increases in size exponentially. 
The time it takes for each prime number generation and power operation is measured and recorded and then graphed. 
Finally a performance score is given to each CPU core based on the number of operations performed in the given amount of time, the total CPU score is the sum of all Core scores. 
