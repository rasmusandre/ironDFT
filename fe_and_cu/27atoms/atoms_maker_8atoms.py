from ase.build import bulk
from ase import Atom, Atoms
from ase.visualize import view
from ase.db import connect
from ase.utils.structure_comparator import SymmetryEquivalenceCheck
from itertools import product

def prepare_structures():

    atoms = bulk('Fe', 'bcc', a = 2.6)*(2,2,2)
    symbols = ['Fe', 'Cu']
    #SET MAGMOM!
    db = connect('FeCu_8_and_27.db')
    for s in product(symbols, repeat = 8):
        for atom in atoms:
            atom.symbol = s[atom.index]
        if not exists_in_db(atoms):
            db.write(atoms, struct_type = 'initial')

#Len(gittervektor)*antallkpunk > 25 k = {density: 5.4, even = True}

def exists_in_db(a):

    db = connect('FeCu_8_and_27.db')
    atoms = []

    for row in db.select(struct_type = 'initial'):

        atoms.append(row.toatoms())

    symcheck = SymmetryEquivalenceCheck()

    return symcheck.compare(a, atoms)

prepare_structures()
