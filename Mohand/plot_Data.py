# All issues to be addressed to be written here in comments.
# 1. setup the data reading from file - DONE
# 2. Plot the raw data after calculating the dist, vel, acc. - DONE
# 3. Add conversion factors from one screen to another and pixels to mm.

def dayTitle(x):
    return {
        0 : '_EarlyPractice_',
        1 : '_Day1_' ,
        2 : '_Day2_',
    }.get(x,'_Day3_')

import math
import matplotlib.pyplot as plt

subject = input("Enter Subject Number: ");
dayNo = input("Enter Day Number (Enter 0 for early practice) :");
horiz = input("Enter Horizontal Resolution of screen :");
verti = input("Enter Vertical Resolution of screen :");
s = 'Data/Subject'+str(subject)+dayTitle(dayNo)+'Data.txt';
f = open(s, 'r');
old_tr_no = 0;
old_x = 0
old_y = 0
old_t = 0
D=[];
V=[];
A=[];
T=[];
X=[];
Y=[];
for line in f:
    tr_no, x , y , t = [float(i) for i in line.split()];
    if old_tr_no==0:
        old_tr_no = tr_no
        old_x = x
        old_y = y
        old_t = t
        T=[t];
        X=[x];
        Y=[y];
    elif old_tr_no != tr_no:
        #plot figures!!
        #print len(X), len(Y), len(T), len(D), len(V), len(A);
        #print X
        #print Y
        #print T
        #print D
        #print V
        #print A
        plt.subplot(221)
        plt.plot(X,Y);
        plt.axis([0,horiz,0,verti])
        #plt.show()
        plt.subplot(222)
        plt.plot(T[1:len(T)],D);
        #plt.show()
        plt.subplot(223)
        plt.plot(T[1:len(T)],V);
        #plt.show()
        plt.subplot(224)
        plt.plot(T[2:len(T)],A);
        plt.show()
        old_x = x
        old_y = y
        old_t = t
        old_tr_no = tr_no
        D=[];
        V=[];
        A=[];
        T=[t];
        X=[x];
        Y=[y];
    else:
        X.append(x);
        Y.append(y);
        T.append(t);
        dist = math.sqrt((x-old_x)*(x-old_x) + (y-old_y)*(y-old_y));
        D.append(dist);
        vel = dist/(t-old_t);
        if(len(V)!=0):
            old_v = V[len(V)-1];
            acc = (vel-old_v)/(t-old_t);
            A.append(acc);
        V.append(vel);
        old_x = x
        old_y = y
        old_t = t
