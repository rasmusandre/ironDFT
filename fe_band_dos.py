# Creates: bandstructure.png
"""Band structure tutorial

Calculate the band structure of Fe along high symmetry directions
Brillouin zone
"""
# P1
from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac
import matplotlib.pyplot as plt
import numpy as np

# Perform standard ground state calculation (with plane wave basis)
# fe = bulk('Fe', 'bcc', 2.87)
# calc = GPAW(mode=PW(600),
#             xc='PBE',
#             kpts=(8, 8, 8),
#             random=True,
#             occupations=FermiDirac(0.1, fixmagmom=True),
#             parallel={'band': 1, 'domain': 1},
#             txt='Fe_gs.txt')
# fe.calc = calc
# fe.get_potential_energy()
# calc.write('Fe_gs.gpw')
#
# # Restart from ground state and fix potential:
# calc = GPAW('Fe_gs.gpw',
#             nbands=16,
#             fixdensity=True,
#             symmetry='off',
#             kpts={'path': 'GXWKL', 'npoints': 60},
#             convergence={'bands': 8})
#
# calc.get_potential_energy()
# e_f = calc.get_fermi_level()
# e, dos = calc.get_dos(spin=0, npts=2001, width=0.1)
name = 'Fe_bcc'
fe = bulk('Fe', 'bcc', 2.87)
fe.set_initial_magnetic_moments([1.0])
calc = GPAW(mode=PW(600), nbands = -2, xc='PBE', kpts=(8,8,8),
            occupations=FermiDirac(0.1, fixmagmom=True), spinpol=True, parallel={'band': 1, 'domain': 1},
            txt=name + '.txt')
fe.set_calculator(calc)
fe.get_potential_energy()
e_f = calc.get_fermi_level()
e, dos = calc.get_dos(spin=1, npts=2001, width=0.1)
plt.figure(0)
plt.plot(dos, e)
plt.plot([0,5], e_f*np.ones(2))
plt.ylim(-1,17.5)
plt.show()

print(e_f)
# P3
bs = calc.band_structure()
#bs.plot()
bs.plot(filename='bandstructure.png', show=True, emax=10.0)
