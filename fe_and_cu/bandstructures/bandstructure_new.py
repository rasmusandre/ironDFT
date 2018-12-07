# Creates: bandstructure.png
"""Band structure tutorial

Calculate the band structure of Si along high symmetry directions
Brillouin zone
"""
# P1
from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac
import matplotlib.pyplot as plt
import numpy as np

# Perform standard ground state calculation (with plane wave basis)
# si = bulk('Fe','bcc', a=3)*(2,1,1)
#
# for atom in si:
#
#     if atom.index == 0:
#
#         atom.symbol = 'Cu'
#     else:
#
#         atom.magmom = 2.2
#
# calc = GPAW(mode=PW(500),
#             xc='PBE',
#             kpts=(8, 8, 8),
#             spinpol=True,
#             random=True,  # random guess (needed if many empty bands required)
#             occupations=FermiDirac(0.1),
#             txt='Si_gs.txt')
# si.calc = calc
# si.get_potential_energy()
# calc.write('Si_gs.gpw')
# P2
# Restart from ground state and fix potential:

calc = GPAW('Si_gs.gpw',
            nbands=16,
            fixdensity=True,
            symmetry='off',
            kpts={'path': 'GXHAG', 'npoints': 60},
            convergence={'bands': 8},txt=None)

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
