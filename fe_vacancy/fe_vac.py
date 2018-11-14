from ase.build import bulk
from ase.db import connect
from ase.optimize.precon import PreconLBFGS
from ase.visualize import view
from ase.io.trajectory import Trajectory
from gpaw import GPAW, PW, FermiDirac
import time
import sys

#SPINPOOOL!

class Gpw_save(object):

    def __init__(self, calc, txtname):

        self.calc = calc
        self.txtname = txtname

    def __call__(self):

        self.calc.write(self.txtname)

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


    atoms = sys.argv[5]
    atoms = int(atoms)
    bulk_mat = bulk('Fe','bcc',a)
    bulk_mat.set_initial_magnetic_moments([2.2])
    bulk_mat = bulk_mat*(atoms,atoms,atoms)


    is_varying = str(sys.argv[6])

    if (str(sys.argv[8]) == 'True'):

        del bulk_mat[[atom.index for atom in bulk_mat if atom.index == 0]]

    #view(bulk_mat)
    #time.sleep(3600)
    calc = GPAW(mode=PW(e_cut), nbands = nbands,
                xc='PBE', kpts=(k_pts,k_pts,k_pts),
                occupations=FermiDirac(smear), txt='Fe.out')


    bulk_mat.set_calculator(calc)
    saver = Gpw_save(calc, 'Fe.gpw')
    traj = Trajectory('some_test_fe.traj', 'w', bulk_mat)
    relaxer = PreconLBFGS(bulk_mat, variable_cell = True, logfile = 'my_log.txt')
    relaxer.attach(traj)
    relaxer.attach(saver)
    relaxer.run(fmax = 0.025, smax = 0.003)

    bulk_mat.get_potential_energy()
    calc.write('Fe.gpw')
    save_atoms(bulk_mat, e_cut, nbands, k_pts, smear, a, is_varying, str(sys.argv[7]))
