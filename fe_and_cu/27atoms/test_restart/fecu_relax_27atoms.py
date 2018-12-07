from ase.db import connect
from ase.build import bulk
from ase import Atoms, Atom
from ase.optimize import BFGS
from ase.constraints import UnitCellFilter
from ase.visualize import view
from ase.io.trajectory import Trajectory
from gpaw import GPAW, PW, FermiDirac, restart
import sys
import os

#This script is used to relax both 64 and 63 fe systems for vac energy

class Gpw_save(object):

    def __init__(self, calc, txtname):

        self.calc = calc
        self.txtname = txtname

    def __call__(self):

        self.calc.write(self.txtname)

def save_atoms(my_atoms, E_c, Nbands, Kpts, Fermi_dirac, Magnetic_moment, Initial_id, Is_initial, database):

    db = connect(database)
    db.write(my_atoms, energy_cutoff = E_c,
             nbands = Nbands, k_points = Kpts,
             smearing_factor = Fermi_dirac,
             magnetic_moment = Magnetic_moment,
             initial_id = Initial_id,
             is_initial = Is_initial)

if __name__ == "__main__":


    #Main arguments:
    e_cut = 500
    nbands = -25
    xc = 'PBE'
    k_pts = 5
    smear = 0.1
    system_name = str(sys.argv[3])

    if os.path.isfile('./' + system_name + '_relaxed.gpw'):
        #Recover past done calculations if available
        print('Restarting gpw: ' + system_name + '_relaxed.gpw')
        bulk_mat, calc = restart(system_name + '_relaxed.gpw')
        bulk_mat.set_calculator(calc)

    else:
        #Initialize new calculations
        db = connect(sys.argv[1])
        bulk_mat = db.get_atoms(id = sys.argv[2])
        initial_magmom = 0

        for atom in bulk_mat:

            if atom.symbol == 'Fe':
                atom.magmom = 2.2
                initial_magmom += 2.2
            else:
                atom.magmom = 0.0



        calc = GPAW(mode=PW(e_cut), nbands = nbands,
                    xc='PBE', spinpol=True, kpts=(k_pts,k_pts,k_pts),
                    occupations=FermiDirac(smear), txt=system_name + '.out')

        bulk_mat.set_calculator(calc)

        save_atoms(bulk_mat, e_cut, nbands, k_pts, smear, initial_magmom, int(sys.argv[2]), 1, str(sys.argv[4]))


    saver = Gpw_save(calc, system_name + '_relaxed.gpw')
    traj = Trajectory(system_name + '_relaxed.traj', 'w', bulk_mat)
    ucf = UnitCellFilter(bulk_mat)
    relaxer = BFGS(ucf, logfile = system_name + '.txt')
    relaxer.attach(traj)
    relaxer.attach(saver)
    relaxer.run(fmax = 0.025)
    bulk_mat.get_potential_energy()

    #Save the final state of the calculations
    calc.write(system_name + '_relaxer_final.gpw')
    save_atoms(bulk_mat, e_cut, nbands, k_pts, smear, initial_magmom, int(sys.argv[2]), 0, str(sys.argv[4]))
