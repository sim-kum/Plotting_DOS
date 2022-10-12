import glob
import os
import matplotlib.pyplot as plt
print("BEFORE STARTING THIS")
print("HAVE YOU PUT ALL THE DOSCAR IN THIS FOLDER THAT YOU NEED TO PLOT")
input_the_atom_number = input("Enter a list of elements on which to calculate the DOS: ")
s = input_the_atom_number.split()
print(s)
for i in s:
        with open("DOSCAR_%s" %i) as j:
                X, Y , lines , values = [], [], [], []
                lines=j.readlines()
                fermi = lines[5].split()[3]
                for k in range(7, len(lines)):
                        values = lines[k].split()
                        X.append(float(values[0]) - float(fermi))
                        Y.append(float(values[1]))
                plt.ylim(0,100)
                plt.xlim(-5,5)
                plt.xlabel('E-E$_F$ (eV)')
                plt.ylabel('DOS')
                if i=='0':
                        plt.plot(X,Y, label='Pure In$_{2}$O$_{3}$')
                else:
                        plt.plot(X,Y, label='Site_%s' %i )
                plt.legend()
plt.show()
