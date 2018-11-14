from ase.build import bulk
from ase.db import connect
from ase.visualize import view
from gpaw import GPAW, PW, FermiDirac
import sys


def save_atoms(my_atoms, E_c, Nbands, Kpts, Fermi_dirac, Lattice_constant, Is_varying, database):

    db = connect(database)
    db.write(my_atoms, energy_cutoff = E_c,
             nbands = Nbands, k_points = Kpts,
             smearing_factor = Fermi_dirac,
             lattice_constant = Lattice_constant,
             is_varying = Is_varying)

if __name__ == "__main__":

    a = 2.86
    e_cut = int(sys.argv[1])
    nbands = int(sys.argv[2])
    xc = 'PBE'
    k_pts = sys.argv[3]
    k_pts = int(k_pts)
    smear = float(sys.argv[4])
    #set hunds rule
    #precon lfgs variable_cell = true

    atoms = sys.argv[5]
    atoms = int(atoms)

    bulk_mat = bulk('Fe','bcc',a)
    print(len(bulk_mat))
    bulk_mat.set_initial_magnetic_moments([2.2])
    bulk_mat = bulk_mat*(atoms,atoms,atoms)
    is_varying = str(sys.argv[6])

    del bulk_mat[[atom.index for atom in bulk_mat if atom.index != 0]]

    calc = GPAW(mode=PW(e_cut), nbands = nbands,
                xc='PBE', spinpol = True, kpts=(k_pts,k_pts,k_pts),
                occupations=FermiDirac(smear), txt='Fe_single_in_64.out')

    view(bulk_mat)
    bulk_mat.set_calculator(calc)



    bulk_mat.get_potential_energy()
    calc.write('Fe_single_in_64.gpw')
    save_atoms(bulk_mat, e_cut, nbands, k_pts, smear, a, is_varying, str(sts.argv[7]))
