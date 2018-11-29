from ase.build import bulk
from ase import Atom, Atoms
from ase.db import connect
from ase.optimize.precon import PreconLBFGS
from ase.visualize import view
from ase.io.trajectory import Trajectory
from gpaw import GPAW, PW, FermiDirac, restart
import time
import sys
import os

#This script is used to relax both 64 and 63 fe systems for vac energy

class Gpw_save(object):

    def __init__(self, calc, txtname):

        self.calc = calc
        self.txtname = txtname

    def __call__(self):

        self.calc.write(self.txtname)

def save_atoms(my_atoms, E_c, Nbands, Kpts, Fermi_dirac, Lattice_constant, Magmom, Is_initial, database):

    db = connect(database)
    db.write(my_atoms, energy_cutoff = E_c,
             nbands = Nbands, k_points = Kpts,
             smearing_factor = Fermi_dirac,
             lattice_constant = Lattice_constant,
             magmom_initial = Magmom,
             is_initial = Is_initial)

if __name__ == "__main__":


    #Main arguments:
    e_cut = 500
    nbands = -25
    xc = 'PBE'
    k_pts = 10
    smear = 0.1
    system_name = str(sys.argv[7])

    if os.path.isfile('./' + system_name + '_relaxed.gpw'):
        #Recover past done calculations if available
        bulk_mat, calc = restart(system_name + '_relaxed.gpw', txt = None)
        bulk_mat.set_calculator(calc)

    else:
        #Initialize new calculations
        db = connect(sys.argv[8])
        bulk_mat = db.get_atoms(id = sys.argv[9])

        calc = GPAW(mode=PW(e_cut), nbands = nbands,
                    xc='PBE', spinpol=True, kpts=(k_pts,k_pts,k_pts),
                    occupations=FermiDirac(smear), txt=system_name + '.out')

        bulk_mat.set_calculator(calc)

        save_atoms(bulk_mat, e_cut, nbands, k_pts, smear, a, initial_magmom, 1, str(sys.argv[6]))


    saver = Gpw_save(calc, system_name + '_relaxed.gpw')
    traj = Trajectory(system_name + '_relaxed.traj', 'w', bulk_mat)
    relaxer = PreconLBFGS(bulk_mat, variable_cell = True, logfile = system_name + '.txt')
    relaxer.attach(traj)
    relaxer.attach(saver)
    relaxer.run(fmax = 0.025, smax = 0.003)
    bulk_mat.get_potential_energy()
    #Save the final state of the calculations
    calc.write(system_name + '_relaxer_final.gpw')
    save_atoms(bulk_mat, e_cut, nbands, k_pts, smear, a, initial_magmom, 0, str(sys.argv[6]))
