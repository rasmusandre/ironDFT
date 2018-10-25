"""Bulk Fe(bcc) test"""
from __future__ import print_function
from ase import Atoms, Atom
from ase.build import bulk
from ase.visualize import view
from gpaw import GPAW, PW, FermiDirac
from ase_db import save_atoms, print_energies
import matplotlib.pyplot as plt
import numpy as np

def create_calculator(ec, nb, x_c, k_pts, FD, name):
    calc = GPAW(mode=PW(ec), nbands = nb, xc=x_c,spinpol = True, kpts=(k_pts, k_pts, k_pts), occupations=FermiDirac(FD, fixmagmom = True), txt=name + '.txt')
    return calc

def run_parameter_iterator():

    start_iteration = 1
    end_iteration = 3.5
    increment = 0.5

    st_lattice_cnst = 2.86
    st_ec = 600
    st_nb = -10
    st_xc = 'PBE'
    st_kpts = 7
    st_FD = 0.05
    st_mag = 2.2
    is_varying = 'magnetic_moment'
    save_to_db = True

    changing_parameter, energies =  parameter_iterator(start_iteration, end_iteration, increment, st_lattice_cnst, st_ec, st_nb, st_xc, st_kpts, st_FD, st_mag, save_to_db, is_varying)

    #print_energies(is_varying)

def parameter_iterator(start_iteration, end_iteration, increment, st_lattice_cnst, st_ec, st_nb, st_xc, st_kpts, st_FD, st_mag, save_to_db, is_varying):

    changing_parameter = []
    energies = []
    name = 'Fe-bcc'
    k = start_iteration

    while k <= end_iteration:

        b = st_lattice_cnst

        if is_varying == 'lattice_constant':
            b = k

        if is_varying == 'magnetic_moment':
            bulk_mat = Atoms('Fe2',
                       scaled_positions=[(0, 0, 0),(0.5, 0.5, 0.5)],
                       magmoms=[k,k],
                       cell=(b, b, b),
                       pbc=True)

        else:
            bulk_mat = Atoms('Fe',
                       scaled_positions=[(0, 0, 0)],
                       magmoms=[st_mag],
                       cell=(b, b, b),
                       pbc=True)
        #else:
        #    bulk_mat = bulk('Fe', 'bcc', b)
        #    bulk_mat.set_initial_magnetic_moments([st_mag])
        #del bulk_mat[[atom.index for atom in bulk_mat if atom.index != 45]]

        if is_varying == 'energy_cutoff':
            calc = create_calculator(k, st_nb, st_xc, st_kpts, st_FD, name)
        if is_varying == 'k_points':
            calc = create_calculator(st_ec, st_nb, st_xc, k, st_FD, name)
        if is_varying == 'smearing_factor':
            calc = create_calculator(st_ec, st_nb, st_xc, st_kpts, k, name)
        if is_varying == 'lattice_constant':
            calc = create_calculator(st_ec, st_nb, st_xc, st_kpts, st_FD, name)
        if is_varying == 'magnetic_moment':
            calc = create_calculator(st_ec, st_nb, st_xc, st_kpts, st_FD, name)


        bulk_mat.set_calculator(calc)
        energy = bulk_mat.get_potential_energy()
        calc.write(name + '.gpw')


        if (save_to_db == True):
            if is_varying == 'energy_cutoff':
                save_atoms(bulk_mat, k, st_nb, st_kpts, st_FD, st_lattice_cnst, st_mag, is_varying)
            if is_varying == 'k_points':
                save_atoms(bulk_mat, st_ec, st_nb, k, st_FD, st_lattice_cnst, st_mag, is_varying)
            if is_varying == 'smearing_factor':
                save_atoms(bulk_mat, st_ec, st_nb, st_kpts, k, st_lattice_cnst, st_mag, is_varying)
            if is_varying == 'lattice_constant':
                save_atoms(bulk_mat, k, st_nb, st_kpts, st_FD, b, st_mag, is_varying)
            if is_varying == 'magnetic_moment':
                save_atoms(bulk_mat, k, st_nb, st_kpts, st_FD, st_lattice_cnst, k, is_varying)

        print('Energy:', energy, 'eV')
        print('Lattice constant: ', b)
        if is_varying == 'lattice_constant':
            changing_parameter.append(b)
        else:
            changing_parameter.append(k)
        energies.append(energy)

        k += increment

    return changing_parameter, energies



run_parameter_iterator()
