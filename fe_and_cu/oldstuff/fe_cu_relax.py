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
    a = 3.62
    e_cut = int(sys.argv[1])
    nbands = int(sys.argv[2])
    xc = 'PBE'
    k_pts = int(sys.argv[3])
    smear = float(sys.argv[4])
    initial_magmom = 2.2
    atoms = int(sys.argv[5])

    system_name = str(sys.argv[7])
    if os.path.isfile('./' + system_name + '_relaxed.gpw'):
        #Recover past done calculations if available
        bulk_mat, calc = restart(system_name + '_relaxed.gpw', txt = None)
        bulk_mat.set_calculator(calc)

    else:
        #Initialize new calculations

        bulk_mat = bulk('Cu','fcc',a)
        bulk_mat = bulk_mat*(2,2,3)

        #del bulk_mat[[atom.index for atom in bulk_mat if atom.index == 0]]

        del bulk_mat[[atom.index for atom in bulk_mat if atom.index == 0]]
        new_atom = Atom('Fe')
        #new_atom.set_initial_magnetic_moments([initial_magmom])
        bulk_mat.append(new_atom)
        #bulk_mat.set_initial_magnetic_moments([2.2, 0])

        #view(bulk_mat)


        calc = GPAW(mode=PW(e_cut), nbands = nbands,
                    xc='PBE', spinpol=True, kpts=(k_pts,k_pts,k_pts),
                    occupations=FermiDirac(smear), txt=system_name + '.out')

        bulk_mat.set_calculator(calc)
        #print(bulk_mat.get_magnetic_moment())
        #time.sleep(120)
        #Save the initial state of the calculations
        #calc.write('Fe_relaxer_initial.gpw')
        save_atoms(bulk_mat, e_cut, nbands, k_pts, smear, a, initial_magmom, 1, str(sys.argv[6]))


    saver = Gpw_save(calc, system_name + '_relaxed.gpw')
    traj = Trajectory(system_name + '_relaxed.traj', 'w', bulk_mat)
    relaxer = PreconLBFGS(bulk_mat, variable_cell = True, logfile = system_name + '.txt')
    relaxer.attach(traj)
    relaxer.attach(saver)
    relaxer.run(fmax = 0.025, smax = 0.003)
    bulk_mat.get_potential_energy()
    print(bulk_mat.get_magnetic_moments())
    #Save the final state of the calculations
    calc.write(system_name + '_relaxer_final.gpw')
    save_atoms(bulk_mat, e_cut, nbands, k_pts, smear, a, initial_magmom, 0, str(sys.argv[6]))
