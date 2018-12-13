# Creates: bandstructure.png
"""Band structure tutorial

Calculate the band structure of Si along high symmetry directions
Brillouin zone
"""
# P1
from ase import Atoms
from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac, restart
import matplotlib.pyplot as plt
import numpy as np
from ase.db import connect
from ase.visualize import view
import time
from ase.dft.kpoints import get_special_points
from ase.dft.kpoints import bandpath



# Perform standard ground state calculation (with plane wave basis)
#si =  Atoms('Fe', scaled_positions=[(0, 0, 0)], magmoms=[k], cell=(b, b, b), pbc=True)
# db = connect('fecu_8atoms_first.db')
# si = db.get_atoms(id=24)
# db = connect('FeCu.db')
# atoms = db.get_atoms(id=6)
#
# for atom in atoms:
#     if atom.symbol == 'Fe':
#         atom.magmom = 2.2
#
# calc = GPAW(mode=PW(600),
#             xc='PBE',
#             kpts=(8, 8, 8),
#             random=True,  # random guess (needed if many empty bands required)
#             spinpol=True,
#             occupations=FermiDirac(0.1),
#             txt='Si_gs.txt')
#
# atoms.calc = calc
# atoms.get_potential_energy()
# calc.write('fecu_v2_gs.gpw')
# P2
# Restart from ground state and fix potential:

# points = get_special_points('bcc', atoms.cell)
# GXW = [points[k] for k in 'GHP']
# kpts, x, X = bandpath(GXW, atoms.cell, 100)
# print(X)

# points = get_special_points(atoms.cell,'bcc')
# GXW = [points[k] for k in 'GHPNG']
# kpts, x, X = bandpath(GXW, atoms.cell, 100)
# print(kpts.shape, len(x), len(X))
# time.sleep(120)

calc = GPAW('fecu_v2_gs.gpw',
            nbands=-50,
            fixdensity=True,
            symmetry='off',
            kpts={'path': 'GHPNG', 'npoints': 60},
            convergence={'bands': 8}, txt='fecu_v2_gs.txt')

calc.get_potential_energy()
e_f = calc.get_fermi_level()
e1, dos1 = calc.get_dos(spin=1, npts=2001, width=0.1) #What is spin?
e0, dos0 = calc.get_dos(spin=0, npts=2001, width=0.1)

plt.figure(0)
plt.plot(dos1, e1)
plt.plot(dos0, e0)
plt.plot([0,4], e_f*np.ones(2),'r--')
plt.ylim(-0.2,e_f+10)
plt.xlim(0,8)
plt.legend(['DOS spin down','DOS spin up', 'Fermi level'],fancybox=True, framealpha=1,shadow=True,prop={'size': 10})
plt.xlabel('Density of states [1/eV]')
plt.ylabel('Energy [eV]')
plt.show()
#
# print(e_f)
# P3
bs = calc.band_structure()
bs.write('my_js.js')
bs.plot(filename='bandstructure_fecu_8atoms.pdf',ylabel = 'Energies [eV]', show=True, emax=10.0)
# print(bs.energies)
#
# my_sum = {}
#
#
#
# for data in bs.energies[0]:
#     print(data)
#     for i in range(0,7):
#         print(round(data[i],0))
#         if (str(round(data[i],0)) in my_sum):
#
#             my_sum[str(round(data[i],0))] = float(my_sum[str(round(data[i],0))]) + 1
#
#         else:
#             my_sum[str(round(data[i],0))] = 1
#
# energies = []
# dosy = []
#
# for key in my_sum:
#     energies.append(float(key))
#     dosy.append(my_sum[key])
#
# list1, list2 = (list(t) for t in zip(*sorted(zip(energies,dosy))))
#
# plt.figure(0)
# plt.plot(list2,list1)
# plt.ylim([-1,17.5])
# plt.show()
# print(my_sum)
