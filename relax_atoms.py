from ase.build import bulk
from ase import Atoms
from ase.db import connect
from ase.visualize import view
from ase.optimize.precon import PreconLBFGS
from ase.io.trajectory import Trajectory
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
    e_cut = 500
    nbands = -5
    xc = 'PBE'
    k_pts = 5
    k_pts = int(k_pts)
    smear = 0.1
    #set hunds rule
    #precon lfgs variable_cell = true

    atoms = 1
    atoms = int(atoms)

    #bulk_mat = bulk('Fe','bcc',a, cubic = True)
    bulk_mat = Atoms('FeCu',positions=[(0,0,0),(10,10,10)],cell = [(a/2,a/2,-a/2), (a/2,-a/2,a/2), (-a/2, a/2, a/2)], pbc = True)

    view(bulk_mat)
    print(len(bulk_mat))
    bulk_mat.set_initial_magnetic_moments([2.0, 2.0])
    print(bulk_mat.get_positions())
    bulk_mat = bulk_mat#*(atoms,atoms,atoms)

    is_varying = 'nothing'



    calc = GPAW(mode=PW(e_cut), nbands = nbands,
                xc='PBE', spinpol = True, kpts=(k_pts,k_pts,k_pts),
                occupations=FermiDirac(smear), txt='Fe.out')


    bulk_mat.set_calculator(calc)
    traj = Trajectory('some_test.traj', 'w', bulk_mat)

    #relaxer = PreconLBFGS(bulk_mat, variable_cell = True, logfile = 'my_log.txt')
    #relaxer.attach(traj)
    #relaxer.run(fmax = 0.025, smax = 0.003)


    bulk_mat.get_potential_energy()
    print(bulk_mat.get_magnetic_moments())
    print(bulk_mat.get_positions())
    calc.write('Fe.gpw')
