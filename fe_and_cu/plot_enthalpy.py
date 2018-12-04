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
        formula.split('Fe')
        formula[0].split('Cu')
        formula = int(formula[0])
        print(formula)
        cu_conc.append(formula/obj['natoms'])

        energy = obj['energy'] - cu_bulk*formula/obj['natoms'] - fe_bulk*(1-formula/obj['natoms'])

        energies.append(energy)

    plt.figure(0)
    plt.plot(energies, cu_cunc)
    plt.grid(True)
    plt.show()
