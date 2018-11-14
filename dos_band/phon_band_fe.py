from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac
from ase.dft.kpoints import ibz_points, bandpath
from ase.phonons import Phonons
from ase.db import connect
import time

def save_atoms(my_atoms, small_q, big_q, Omega_kn, Point_names, Dos_e, Omega_e):

    db = connect('fe_phon_band.db')
    db.write(my_atoms, data = {'q': small_q, 'Q': big_q, 'omega_kn': Omega_kn, 'point_names': point_names, 'dos_e': Dos_e, 'omega_e': Omega_e})

# Setup crystal and EMT calculator
atoms = bulk('Fe', 'bcc', a=2.86)
calc = GPAW(mode=PW(600), nbands = -60, xc='PBE', kpts=(5,5,5), symmetry={'point_group': False}, occupations=FermiDirac(0.1))
#
# # Phonon calculator
N = 3
ph = Phonons(atoms, calc, supercell=(N, N, N), delta=0.05)
ph.run()
time.sleep(250)

# Read forces and assemble the dynamical matrix
ph.read()

# High-symmetry points in the Brillouin zone
points = ibz_points['bcc']
G = points['Gamma']
H = points['H']
N = points['N']
P = points['P']


point_names = ['$\Gamma$', 'H', 'P', '$\Gamma$', 'N']
path = [G, H, P, G, N]

# Band structure in meV
path_kc, q, Q = bandpath(path, atoms.cell, 100)
omega_kn = 1000 * ph.band_structure(path_kc)

# Calculate phonon DOS
omega_e, dos_e = ph.dos(kpts=(50, 50, 50), npts=5000, delta=5e-4)
omega_e *= 1000
save_atoms(atoms, q, Q, omega_kn, point_names, dos_e, omega_e)
# Plot the band structure and DOS
# import matplotlib.pyplot as plt
# plt.figure(1, (8, 6))
# plt.axes([.1, .07, .67, .85])
# for n in range(len(omega_kn[0])):
#     omega_n = omega_kn[:, n]
#     plt.plot(q, omega_n, 'k-', lw=2)
#
# plt.xticks(Q, point_names, fontsize=18)
# plt.yticks(fontsize=18)
# plt.xlim(q[0], q[-1])
# plt.ylabel("Frequency ($\mathrm{meV}$)", fontsize=22)
# plt.grid('on')
#
# plt.axes([.8, .07, .17, .85])
# plt.fill_between(dos_e, omega_e, y2=0, color='lightgrey', edgecolor='k', lw=1)
# plt.ylim(0, 35)
# plt.xticks([], [])
# plt.yticks([], [])
# plt.xlabel("DOS", fontsize=18)
# plt.show()
