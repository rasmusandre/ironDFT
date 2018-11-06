#!/usr/bin/env python

'''Example of fitting the Birch-Murnaghan EOS to data'''

from pylab import * #this includes numpy as np!
from scipy.optimize import leastsq
from ase_db import plot_from_db
import matplotlib.pyplot as plt
# raw data from 2.2.3-al-analyze-eos.py
v = np.array([13.72, 14.83, 16.0, 17.23, 18.52])
e = np.array([-56.29, -56.41, -56.46, -56.46, -56.42])

e, v = plot_from_db('lattice_constant', 'single_cu.db')
plt.clf()
e = np.array([i for i in e])
v = np.array([k**3/4 for k in v]) #Divide by two for bcc, divide by four for fcc
#print(e,v)
#make a vector to evaluate fits on with a lot of points so it looks smooth
vfit = np.linspace(min(v),max(v),100)

### fit a parabola to the data
# y = ax^2 + bx + c
a,b,c = polyfit(v,e,2) #this is from pylab

'''
the parabola does not fit the data very well, but we can use it to get
some analytical guesses for other parameters.

V0 = minimum energy volume, or where dE/dV=0
E = aV^2 + bV + c
dE/dV = 2aV + b = 0
V0 = -b/2a

E0 is the minimum energy, which is:
E0 = aV0^2 + bV0 + c

B is equal to V0*d^2E/dV^2, which is just 2a*V0

and from experience we know Bprime_0 is usually a small number like 4
'''

#now here are our initial guesses.
v0 = -b/(2*a)
e0 = a*v0**2 + b*v0 + c
b0 = 2*a*v0
bP = 4

#now we have to create the equation of state function
def Murnaghan(parameters,vol):
    '''
    given a vector of parameters and volumes, return a vector of energies.
    equation From PRB 28,5480 (1983)
    '''
    E0 = parameters[0]
    B0 = parameters[1]
    BP = parameters[2]
    V0 = parameters[3]

    E = E0 + B0*vol/BP*(((V0/vol)**BP)/(BP-1)+1) - V0*B0/(BP-1.)

    return E

# and we define an objective function that will be minimized
def objective(pars,y,x):
    #we will minimize this function
    err =  y - Murnaghan(pars,x)
    return err

x0 = [e0, b0, bP, v0] #initial guesses in the same order used in the Murnaghan function

murnpars, ier = leastsq(objective, x0, args=(e,v)) #this is from scipy

#now we make a figure summarizing the results
plot(v,e,'rx', label='Calculated data')
plot(vfit, a*vfit**2 + b*vfit + c,'g--',label='Parabolic fit')
plot(vfit, Murnaghan(murnpars,vfit),'b', label='Murnaghan fit')
xlabel('Volume of unit cell [Å$^3$]')
ylabel('Potential energy [eV/atom]')
legend(loc='best')

#add some text to the figure in figure coordinates
# ax = gca()
# text(0.4,0.5,'Min volume = %1.2f $\AA^3$' % murnpars[3],
#      transform = ax.transAxes)
# text(0.4,0.4,'Bulk modulus = %1.2f eV/$\AA^3$ = %1.2f GPa' % (murnpars[1],
#                                                               murnpars[1]*160.21773)
#      , transform = ax.transAxes)
print('The min lattice constant is: ' + str((2*float(murnpars[3]))**(1/3)))
print('The bulk modulus is: ' + str(murnpars[1]*160.21773))
savefig('a-eos.png')
show()


#print 'initial guesses  : ', x0
#print 'fitted parameters: ', murnpars
