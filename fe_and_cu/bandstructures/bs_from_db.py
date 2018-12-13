
from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac
import matplotlib.pyplot as plt
import numpy as np
from ase.db import connect
from ase.visualize import view

db = connect('fecu_8atoms_first.db')
atoms = db.get_atoms(id=24)


calc = GPAW(mode=PW(500),
            nbands=-16,
            fixdensity=True,
            symmetry='off',
            spinpol=True,
            kpts={'path': 'GXHAG', 'npoints': 60},
            convergence={'bands': 8},txt=None)

atoms.calc = calc
calc.get_potential_energy()

e_f = calc.get_fermi_level()
e1, dos1 = calc.get_dos(spin=1, npts=2001, width=0.1) #What is spin?
e0, dos0 = calc.get_dos(spin=0, npts=2001, width=0.1)
#
plt.figure(0)
plt.plot(dos1, e1)
plt.plot(dos0, e0)
plt.plot([0,4], e_f*np.ones(2),'r--')
plt.ylim(-0.2,e_f+10)
plt.xlim(0,4)
plt.legend(['DOS spin up','Dos spin down', 'Fermi level'],fancybox=True, framealpha=1,shadow=True,prop={'size': 10})
plt.xlabel('Density of states [1/eV]')
plt.ylabel('Energy [eV]')
plt.show()
# P3
bs = calc.band_structure()
bs.plot(filename='bandstructurefecu.png', show=True, emax=10.0)
