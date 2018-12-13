# Creates: bandstructure.png
"""Band structure tutorial

Calculate the band structure of Si along high symmetry directions
Brillouin zone
"""
# P1
from ase import Atoms
from ase.build import bulk
from ase.visualize import view
from gpaw import GPAW, PW, FermiDirac, restart
import matplotlib.pyplot as plt
import numpy as np
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter


# Perform standard ground state calculation (with plane wave basis)
#si =  Atoms('Fe', scaled_positions=[(0, 0, 0)], magmoms=[k], cell=(b, b, b), pbc=True)

si = bulk('Fe','bcc', a=3.1)*(2,1,1)

for atom in si:

    if atom.index == 0:

        atom.symbol = 'Cu'
    else:

        atom.magmom = 2.2

system_name = 'fecu2'
# calc = GPAW(mode=PW(500), xc='PBE', kpts=(8,8,8), nbands=-10, spinpol=True, occupations=FermiDirac(0.1), txt=system_name+'.out')
# si.set_calculator(calc)
# si, calc = restart(system_name + '_relaxed.gpw', txt=None)
# saver = Gpw_save(calc, system_name + '_relaxed.gpw')
#
#
# ucf = UnitCellFilter(si)
# relaxer = BFGS(ucf, logfile = system_name + '.txt')
# relaxer.attach(saver)
# relaxer.run(fmax = 0.025)
# si.get_potential_energy()
# calc.write(system_name + '.gpw')


calc = GPAW(mode=PW(600),
            xc='PBE',
            kpts=(8, 8, 8),
            random=True,  # random guess (needed if many empty bands required)
            occupations=FermiDirac(0.1),
            txt='Si_gs.txt')
si.calc = calc
si.get_potential_energy()
calc.write('Si_gs.gpw')
# P2
# Restart from ground state and fix potential:
calc = GPAW(system_name + '_relaxed.gpw',
            nbands=16,
            fixdensity=True,
            symmetry='off',
            kpts={'path': 'GHPNG', 'npoints': 60},
            convergence={'bands': 8}, txt='Fecu_gs.txt')
bulk_mat, calc = restart('fecu2_relaxed.gpw',txt=None)#, kpts={'path': 'GHPNG', 'npoints': 60}, convergence={'bands': 8}, symmetry='off')
bulk_mat.set_calculator(calc)
bulk_mat.get_potential_energy()
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
#
# print(e_f)
# P3
bs = calc.band_structure()

bs.write('my_js.js')
bs.plot(filename='bandstructurefecu.pdf',ylabel = 'Energies [eV]', show=True, emax=10.0)
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
