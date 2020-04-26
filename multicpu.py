from timeit import default_timer as timer
import random
import multiprocessing
import numpy as np
from random import randint


if __name__ == "__main__":

    def function(x):
        s = np.ones(1000000000)
        t = 0
        while t < 100000:
            s[t]*= randint(0,100)
            t+=1
        print('finished',x)

    count=1

    while count < 20:
        process1 = multiprocessing.Process(target=function('1'))
        process2 = multiprocessing.Process(target=function('2'))
        process3 = multiprocessing.Process(target=function('3'))
        process4 = multiprocessing.Process(target=function('4'))
        count+=1




    print ("List processing complete.")
