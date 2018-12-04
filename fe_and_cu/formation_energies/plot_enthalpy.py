from ase.build import bulk
from ase import Atom, Atoms
from ase.visualize import view
from ase.db import connect
import matplotlib.pyplot as plt

def get_energies():

    db = connect('fecu_8atoms.db')
    energies = []
    cu_conc = []
    fe_bulk = 0
    cu_bulk = 0

    for obj in db.select(is_initial = 0):

        if obj['formula'] == 'Fe8':
            fe_bulk = obj['energy']
        if obj['formula'] == 'Cu8':
            cu_bulk = obj['energy']


    for obj in db.select(is_initial = 0):

        formula = obj['formula']
        if formula == 'Fe8':
            numcu = 0
        if formula == 'Cu8':
            numcu = 1
        elif len(formula) > 3:
            formula.split('Fe')
            print(formula)

        cu_conc.append(numcu/obj['natoms'])

        energy = obj['energy'] - cu_bulk*numcu/obj['natoms'] - fe_bulk*(1-numcu/obj['natoms'])

        energies.append(energy)

    plt.figure(0)
    plt.plot(energies, cu_conc)
    plt.grid(True)
    plt.show()

def find_atoms():

    db = connect('fecu_8atoms_first.db')

    atom1 = db.get_atoms(id=20)
    view(atom1)




def brute_force():
    efe = -72.032
    ecu = -28.897
    magmoms = [17.267, 16.077, 0, 10.628, 13.002, 14.416, 2.961, 10.227, 5.491, 10.416, 8.913, 14.793, 7.816, 10.349, 5.346, 12.546]
    energies = [-72.032, -66.090, -28.897, -48.475, -54.355, -60.329, -33.341, -49.211, -38.469, -48.967, -43.276, -60.259, -43.730, -49.158, -38.500, -54.701]
    conc = [0, 1/8, 1, 1/2, 3/8, 2/8, 7/8, 1/2, 6/8, 1/2, 5/8, 2/8, 5/8, 1/2, 6/8, 3/8]
    conc2 = conc
    conc2, magmoms = (list(t) for t in zip(*sorted(zip(conc2, magmoms))))

    conc, energies = (list(t) for t in zip(*sorted(zip(conc, energies))))

    energies = [energies[i] - conc[i]*ecu - (1-conc[i])*efe for i in range(0,len(energies))]

    plt.figure(0)
    plt.plot(conc, energies, 'bo')
    plt.xlabel('X(Cu)')
    plt.ylabel('Energy of formation [eV]')
    plt.grid(True)

    plt.figure(1)
    plt.plot(conc, magmoms, 'r*')
    plt.plot([0,1], [17.267,0], 'b')
    plt.xlabel('X(Cu)')
    plt.ylabel('Total magnetic moment [$\mu_B$]')
    plt.legend(['Calculated magnetic moment', 'Zero induced magnetic moment'],fancybox=True, framealpha=1,shadow=True,prop={'size': 10})
    plt.grid(True)
    plt.show()

#brute_force()
find_atoms()











#get_energies()
