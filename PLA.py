import argparse
import numpy as np
import os, sys
from numpy import linalg as LA
import math
import pickle
import matplotlib.pyplot as plt
import random
N=100
## data generation
#-------------------------------------------------------------------------------
data1=np.column_stack((np.ones(N),np.ones(N),np.ones(N)))

for i in range(0,len(data1)):

    data1[i,0]=random.uniform(-1,1)
    data1[i,1]=random.uniform(-1,1)
    if (data1[i,0]-0.2>data1[i,1]):
        data1[i,2]=1
    else:
        data1[i,2]=-1
#-------------------------------------------------------------------------------
#data plotting
count=0
break_point=1
for i in range(0,len(data1)):
    if(data1[i,2]==1):
        plt.plot(data1[i,0],data1[i,1],'*b')
    else:
        plt.plot(data1[i,0],data1[i,1],'or')


def misclassified(data,w):
    break_point=1
    def safe(num):
        if (num>0):
            return 1
        else:
            return -1
    X=np.column_stack((np.ones(len(data1),dtype=int),data1[:,0],data1[:,1]))
    misclassify=[]
    for i in range(0,len(data1)):
        mul=w*X.transpose()
        sign=safe(float(mul[0,i]))
        if(sign!=data1[i,2]):
            misclassify=np.append([misclassify],[i])
            #print(misclassify,'In loop')
    if(len(misclassify)==0):
        break_point = 0
        a=-5
        length=0
    if(break_point == 1):
        point=random.randint(1,len(misclassify))
        a=int(misclassify[point-1])
        print(misclassify)
        print(len(misclassify),'misclassify number')
        length=len(misclassify)
    return a,break_point,length

X=np.column_stack((np.ones(len(data1),dtype=int),data1[:,0],data1[:,1]))

mis_counter=0
mis_avg=0

w=np.mat([0.5,0,0])

while(break_point==1):
    count=count+1
    print(count)
    koyal,break_point,length=misclassified(data1,w)
    if(koyal!=-5):
        mis_counter=mis_counter+length
        w_new=np.mat([0,0,0])
        w_new= w + X[koyal,:]*data1[koyal,2]
        #print(w_new)
        w=w_new
        m=float(-w_new[0,1]/w_new[0,2])
        c=float(-w_new[0,0]/w_new[0,2])
        x_line1=np.mat([[-1],[1]])
        y_line1=m*x_line1+c
        plt.plot(x_line1,y_line1,'-y')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axis([-1,1,-1,1])
        plt.title('Data set')
        plt.pause(0.01)

mis_avg=mis_counter/(len(data1)*count)
print('Probability is',mis_avg)
#plt.show()

m=float(-w_new[0,1]/w_new[0,2])
c=float(-w_new[0,0]/w_new[0,2])
x_line1=np.mat([[-1],[1]])
y_line1=m*x_line1+c
plt.plot(x_line1,y_line1,'-m')
plt.xlabel('x')
plt.ylabel('y')
plt.axis([-1,1,-1,1])
plt.title('Data set')
plt.show()
