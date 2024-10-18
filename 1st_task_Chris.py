########################
#Import needed libraries
########################

import numpy as np
import matplotlib.pyplot as plt
import random  
from numpy import prod
import os

##############################
#Define mathematical functions
##############################

def poly(n):
    return n 

def exponential(n):
    return np.exp(n)

######################
#Define task functions
######################

#Define a PUF
def PUF(x, A, B): #x is the input and A a the domain (challenges) that is mapped to the image B (responses).
    y = 0 #We initialize the return variable.
    for i in A:
        if x == i:
            y = i
    return y

#Define attacker training stage 
def training(PUF, A, B, queries, i):  #queries is a function on the security parameter defining the amount of queries allowed for learning. x is the challenge to be forged.
    #Create a database (memory) for challenges and responses learnt by querying the PUF.
    M_A = np.zeros(len(A)) 
    M_B = np.zeros(len(A))
    #Learning phase
    for i in range(int(queries(i))):
        a = random.randrange(0, len(A), 1)
        M_A[a] = a
        M_B[a] = PUF(a, A, B)
    return M_A, M_B

#Define attacker forgery stage
def forgery(M_A, M_B, PUF, A, B, x):
    success = 0
    if M_B[x] == PUF(x, A, B):
        success = 1
    return success

#Create a plot showing the performance of an attacker as a function of len(A)/queries, by choosing f for len(A) and g for queries over the same variable.

#################
#Define variables
#################

N = 7 #Maximum value attained by sec,
m = 3 #Number combinations among PUF sizes and queries size (different size of learnt database e.g., poly_1, poly_2, etc.) that will be attempted for each different sec.
M = 50 #Number of forgery attempts for each combination to gain statistics

###################
#Data to be plotted
###################

success_ratios = np.zeros((3, N)) #We'll plot for a poly/poly, poly/exponential and exponential/poly.


for i in range(N):
    #PUF creations and training phases (for each combination)
    for k in range(m):
        if k == 0:
            A_1 = np.zeros(poly(i + 1))  #Notice that A and M_A could be removed from the whole code. If you don't see why, let us talk about it next day.
            B_1 = np.zeros(poly(i + 1))
            for l in range(len(A_1)):
                flag_1 = 0
                while flag_1 == 0: #To avoid degeneracy/non bijectivity
                    A_1[l] = l    
                    B_1[l] = random.randrange(0, len(A_1), 1)
                    flag_2 = 0
                    for p in range(l):
                        if B_1[p] == B_1[l]:
                            flag_2 = 1
                    if flag_2 == 0:
                        flag_1 = 1
            M_A_1, M_B_1 = training(PUF, A_1, B_1, poly, i + 1)                  
            print('ara')
            print(A_1)
            print(B_1) 
            print('ja')
            A_2 = np.zeros(int(exponential(i + 1)))  #Notice that A and M_A could be removed from the whole code. If you don't see why, let us talk about it next day.
            B_2 = np.zeros(int(exponential(i + 1)))
            for l in range(len(A_2)):
                flag_1 = 0
                while flag_1 == 0: #To avoid degeneracy/non bijectivity
                    A_2[l] = l    
                    B_2[l] = random.randrange(0, len(A_2), 1)
                    flag_2 = 0
                    for p in range(l):
                        if B_2[p] == B_2[l]:
                            flag_2 = 1
                    if flag_2 == 0:
                        flag_1 = 1
            M_A_2, M_B_2 = training(PUF, A_2, B_2, poly, i + 1) 
            
            A_3 = np.zeros(poly(i + 1))  #Notice that A and M_A could be removed from the whole code. If you don't see why, let us talk about it next day.
            B_3 = np.zeros(poly(i + 1))
            for l in range(len(A_3)):
                flag_1 = 0
                while flag_1 == 0: #To avoid degeneracy/non bijectivity
                    A_3[l] = l    
                    B_3[l] = random.randrange(0, len(A_3), 1)
                    flag_2 = 0
                    for p in range(l):
                        if B_3[p] == B_3[l]:
                            flag_2 = 1
                    if flag_2 == 0:
                        flag_1 = 1
            M_A_3, M_B_3 = training(PUF, A_3, B_3, exponential, i + 1) 
            
    #Forging/attacking stage
    for k in range(m):
            for l in range(M): 
                    if k == 0:
                            x = random.randrange(0, len(A_1), 1)
                            s = forgery(M_A_1, M_B_1, PUF, A_1, B_1, x)
                            success_ratios[k, i] += s/M
                    elif k == 1:
                            x = random.randrange(0, len(A_2), 1)
                            s = forgery(M_A_2, M_B_2, PUF, A_2, B_2, x)
                            success_ratios[k, i] += s/M
                    elif k == 2:
                            x = random.randrange(0, len(A_3), 1)
                            s = forgery(M_A_3, M_B_3, PUF, A_3, B_3, x)
                            success_ratios[k, i] += s/M

filename1 = "success_ratios.txt"
path = os.path.join(r"C:\Users\farre\Desktop\PhD_Pol\Education\Supervision\Chris", filename1)
np.savetxt(path, success_ratios)
print(success_ratios)
print('Done')

t = np.arange(0, N, 1)

poly_poly = success_ratios[0]
exp_poly = success_ratios[1]
poly_exp = success_ratios[2]

#The order in which we mention "growth" (poly or exp) is the following: 1st PUF complexity, 2nd Attacker power
plt.plot(t, poly_poly, color = 'red', label = 'poly-poly')
plt.plot(t, exp_poly, color = 'blue', label = 'exp-poly')
plt.plot(t, poly_exp, color = 'green', label = 'poly-exp')
plt.legend()

filename2 = 'performances.pdf'
path2 = os.path.join(r"C:\Users\farre\Desktop\PhD_Pol\Education\Supervision\Chris",filename2)
plt.savefig(path2)
plt.show()