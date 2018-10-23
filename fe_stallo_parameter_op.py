from ase.build import bulk
from ase.db import connect
from ase.visualize import view
from gpaw import GPAW, PW, FermiDirac
import sys


def save_atoms(my_atoms, E_c, Nbands, Kpts, Fermi_dirac, Lattice_constant, Is_varying):

    db = connect('fe_kpts.db')
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


    atoms = sys.argv[5]
    atoms = int(atoms)
    bulk_mat = bulk('Fe','bcc',a)*(atoms,atoms,atoms)
    bulk_mat.set_initial_magnetic_moments([1.0])

    is_varying = str(sys.argv[6])



    calc = GPAW(mode=PW(e_cut), nbands = nbands,
                xc='PBE', spinpol = True, kpts=(k_pts,k_pts,k_pts),
                occupations=FermiDirac(smear), txt='Fe.out')

    bulk_mat.set_calculator(calc)
    bulk_mat.get_potential_energy()
    calc.write('Fe.gpw')
    save_atoms(bulk_mat, e_cut, nbands, k_pts, smear, a, is_varying)
