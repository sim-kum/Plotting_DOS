import glob
import os
import matplotlib.pyplot as plt
for i in (5,13,21,63,71,79,81):
        with open("DOS%s" %i) as j:
                print(i)
                X, z, p, d = [], [], [], []
                for line in j:
                        values = [float(s) for s in line.split()]
                        z.append(values[1])
                        p.append(values[2])
                        d.append(values[3])
                        X.append(values[0])
                plt.ylim(0,100)
                plt.xlabel('E (eV)')
                plt.ylabel('DOS')
                plt.plot(X,z,X,p,X,d, label='site_%s' %i)
                plt.legend()
plt.show()
