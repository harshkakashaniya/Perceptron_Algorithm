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
target_fn_m=1
# keep value of c between -1<c<1 because we have points between -1 to 1
target_fn_c=0.2

for i in range(0,len(data1)):

    data1[i,0]=random.uniform(-1,1)
    data1[i,1]=random.uniform(-1,1)
    if (data1[i,0]*target_fn_m+target_fn_c<data1[i,1]):
        a=i
        data1[i,2]=1
    else:
        b=i
        data1[i,2]=-1
#print (data1)
#-------------------------------------------------------------------------------
#data plotting
count=0
break_point=1
for i in range(0,len(data1)):
    if(data1[i,2]==1):
        plt.plot(data1[i,0],data1[i,1],'*b')
    else:
        plt.plot(data1[i,0],data1[i,1],'or')

plt.plot(data1[a,0],data1[a,1],'*b', label='y=1 points')
plt.plot(data1[b,0],data1[b,1],'or', label='y=-1 points')
#-------------------------------------------------------------------------------
def ProbabilityError(target_line_m,target_line_c,hypothesis_line_m,hypothesis_line_c):
    x=(hypothesis_line_c-target_line_c)/(target_line_m-hypothesis_line_m)
    y=target_line_m*x+target_line_c
##
    y_minus=-1
    y_plus=1

    x_y_minus_t=(y_minus-target_line_c)/target_line_m
    x_y_plus_t=(y_plus-target_line_c)/target_line_m
    x_y_minus_h=(y_minus-hypothesis_line_c)/hypothesis_line_m
    x_y_plus_h=(y_plus-hypothesis_line_c)/hypothesis_line_m

    x_minus=-1
    x_plus=1
    y_x_minus_t=target_line_m*x_minus+target_line_c
    y_x_plus_t=target_line_m*x_plus+target_line_c
    y_x_minus_h=hypothesis_line_m*x_minus+hypothesis_line_c
    y_x_plus_h=hypothesis_line_m*x_plus+hypothesis_line_c


    if(abs(x_y_minus_t)<=1):
        Dty=y_minus
        Dtx=x_y_minus_t
        print('y_minus_t')

    if(abs(y_x_minus_t)<=1):
        Dty=y_x_minus_t
        Dtx=x_minus
        print('x_minus_t')

    if(abs(x_y_minus_h)<=1):
        Dhy=y_minus
        Dhx=x_y_minus_h
        print('y_minus_h')

    if(abs(y_x_minus_h)<=1):
        Dhy=y_x_minus_h
        Dhx=x_minus
        print('x_minus_h')

        #------------------
    if(abs(x_y_plus_t)<=1):
        Uty=y_plus
        Utx=x_y_plus_t
        print('y_plus_t')

    if(abs(y_x_plus_t)<=1):
        Uty=y_x_plus_t
        Utx=x_plus
        print('x_plus_t')

    if(abs(x_y_plus_h)<=1):
        Uhy=y_plus
        Uhx=x_y_plus_h
        print('y_plus_h')

    if(abs(y_x_plus_h)<=1):
        Uhy=y_x_plus_h
        Uhx=x_plus
        print('x_plus_h')

##

    if (abs(x) < 1 and abs(y) < 1):
        intersect = 1
        xm=x
        ym=y
        def Area(x1,y1,x2,y2,x3,y3):
            return abs(0.5*((x1)*(y2-y3)+(x2)*(y3-y1)+(x3)*(y1-y2)))
        Area1=Area(xm,ym,Dtx,Dty,Dhx,Dhy)
        Area2=Area(xm,ym,Utx,Uty,Uhx,Uhy)
        Area=Area1+Area2
    else:
        intersect = 0
        def LineLeftArea(Ux,Uy,Dx,Dy):
            if(Ux>Dx):
                Area=abs(abs(Ux+1)*abs(Uy-Dy)-0.5*abs(Ux-Dx)*abs(Uy-Dy))
            else:
                Area=abs(abs(Ux+1)*abs(Uy-Dy)+0.5*abs(Ux-Dx)*abs(Uy-Dy)+abs(Dy+1)*2)
            return Area


        def LineRightArea(Ux,Uy,Dx,Dy):
            if(Ux>Dx):
                Area=abs(abs(Ux-1)*abs(Uy-Dy)+0.5*abs(Ux-Dx)*abs(Uy-Dy)+abs(Dy+1)*2)
            else:
                Area=abs(abs(Ux-1)*abs(Uy-Dy)-0.5*abs(Ux-Dx)*abs(Uy-Dy))
            return Area

        Area1=LineLeftArea(Utx,Uty,Dtx,Dty)
        Area2=LineRightArea(Uhx,Uhy,Dhx,Dhy)
        print(Area1,'ar1')
        print(Area2,'ar2')
        Area=abs(4-Area1-Area2)

    return Area


#-------------------------------------------------------------------------------

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
        #print("Misclas. pts:",misclassify)
    print("Misclas. pts count",len(misclassify))
    length=len(misclassify)
    return a,break_point,length


X=np.column_stack((np.ones(len(data1),dtype=int),data1[:,0],data1[:,1]))

mis_counter=0
mis_avg=0

w=np.mat([0.5,0,0])

while(break_point==1):
    count=count+1
    print("Iterations count:",count)
    koyal,break_point,length=misclassified(data1,w)
    if(koyal!=-5):
        mis_counter=mis_counter+length
        #print("Misclas. pts count",mis_counter)
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

#mis_avg=mis_counter/(len(data1)*count)
#print('Probability of f(x)!=g(x)',mis_avg)


m=float(-w_new[0,1]/w_new[0,2])
c=float(-w_new[0,0]/w_new[0,2])
x_line1=np.mat([[-1],[1]])
y_line1=m*x_line1+c
x_linet=x_line1
y_linet=target_fn_m*x_linet+target_fn_c
Area=ProbabilityError(target_fn_m,target_fn_c,m,c)
print(Area/4,'Area')

plt.plot(x_line1,y_line1,'-y',label='PLA Lines')
plt.plot(x_line1,y_line1,'-m',label='Best Fit Line')
plt.plot(x_linet,y_linet,'-g',label='target_function')

plt.xlabel('x')
plt.ylabel('y')
plt.axis([-1,1,-1,1])
plt.title('Data set')
plt.legend()
plt.show()
