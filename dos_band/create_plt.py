from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac
from ase.dft.kpoints import ibz_points, bandpath
from ase.phonons import Phonons
from ase.db import connect
import matplotlib.pyplot as plt

def create_plt(database):



    db = connect(database)

    for outer_obj in db.select():
            obj = outer_obj['data']
            q = obj['q']
            Q = obj['Q']
            omega_kn = obj['omega_kn']
            point_names = obj['point_names']
            dos_e = obj['dos_e']
            omega_e = obj['omega_e']


    plt.figure(1, (8, 6))
    plt.axes([.1, .07, .67, .85])

    for n in range(len(omega_kn[0])):
        omega_n = omega_kn[:, n]
        plt.plot(q, omega_n, 'k-', lw=2)



    plt.xticks(Q, point_names, fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlim(q[0], q[-1])
    plt.ylabel("Frequency ($\mathrm{meV}$)", fontsize=22)
    plt.grid('on')

    plt.axes([.8, .07, .17, .85])
    plt.fill_between(dos_e, omega_e, y2=0, color='lightgrey', edgecolor='k', lw=1)
    plt.ylim(0, 35)
    plt.xticks([], [])
    plt.yticks([], [])
    plt.xlabel("DOS", fontsize=18)
    plt.show()

db = 'fe_phon_band.db'
create_plt(db)
