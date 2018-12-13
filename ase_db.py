from ase.db import connect
from ase import Atoms
from ase.build import bulk
from ase.visualize import view
import matplotlib.pyplot as plt
import numpy as np


def save_atoms(my_atoms, E_c, Nbands, Kpts, Fermi_dirac, Lattice_constant, Magnetic_moment, Is_varying):

    db = connect('fe_1atom.db')
    db.write(my_atoms, energy_cutoff = E_c, nbands = Nbands, k_points = Kpts, smearing_factor = Fermi_dirac, lattice_constant = Lattice_constant, magnetic_moment = Magnetic_moment, is_varying = Is_varying)

def print_energies(Is_varying):

    db = connect('single_cu_xc_PBE.db')
    print('The changing parameter is ' + Is_varying)
    for obj in db.select(is_varying = Is_varying):

        print(Is_varying + ' is ' + str(obj[Is_varying]))

        print('The energy is ' + str(obj['energy']))




def db_deleter():

    param = 'magnetic_moment'
    db = connect('single_fe_ver2.db')
    for obj in db.select(is_varying = param):

        del db[obj.id]

def plot_from_db(Is_varying, database_name):

    db = connect(database_name)
    energies = []
    changing_parameter = []
    for obj in db.select(is_varying = Is_varying):

        energies.append(obj['energy'])
        changing_parameter.append(obj[Is_varying])
        #print(obj['k_points'])

    plt.figure(0)
    if Is_varying == 'lattice_constant' or Is_varying == 'magnetic_moment':
        if Is_varying == 'magnetic_moment':
            plt.plot(changing_parameter, [i/2 for i in energies])
            plt.plot(changing_parameter, [i/2 for i in energies], 'ro')
        else:
            plt.plot(changing_parameter, energies)
            plt.plot(changing_parameter, energies, '*')
    else:
        plt.semilogx(changing_parameter, energies)
        plt.semilogx(changing_parameter, energies, '*')
    plt.ylabel('Potential energy [eV/atom]')
    plt.xlabel('Varying parameter = ' + Is_varying)
    if (Is_varying == 'magnetic_moment'):
        plt.xlabel('Magnetic moment [' + r'$\mu_{B}$' + '/atom]')
        plt.grid('True')
    #plt.show()
    return energies, changing_parameter

def plot_from_db_two_db(Is_varying, database_name1, database_name2):

    db1 = connect(database_name1)
    db2 = connect(database_name2)
    energies1 = []
    energies2 = []
    changing_parameter1 = []
    changing_parameter2 = []
    amt1 = db1.get_atoms(id = 1)
    amt2 = db2.get_atoms(id = 1)

    for obj in db1.select(is_varying = Is_varying):

        energies1.append(obj['energy']/amt1.get_number_of_atoms())
        changing_parameter1.append((obj[Is_varying]))

    plt.figure(0)

    if (Is_varying == 'k_points'):
        changing_parameter1 = [i**3 for i in changing_parameter1]
        plt.semilogx(changing_parameter1, energies1,'b')
        plt.semilogx(changing_parameter1, energies1, 'bo',label='_nolegend_')
    else:
        if (Is_varying == 'smearing_factor'):
            plt.plot([k/(8.62*10**-5) for k in changing_parameter1], energies1,'b')
            plt.plot([k/(8.62*10**-5) for k in changing_parameter1], energies1, 'bo',label='_nolegend_')
        else:
            plt.plot(changing_parameter1, energies1,'b')
            plt.plot(changing_parameter1, energies1, 'bo',label='_nolegend_')

    for obj in db2.select(is_varying = Is_varying):

        energies2.append(obj['energy']/amt2.get_number_of_atoms())

        changing_parameter2.append((obj[Is_varying]))


    if (Is_varying == 'k_points'):
        changing_parameter2 = [i**3 for i in changing_parameter2]
        plt.semilogx(changing_parameter2, energies2,'r')
        plt.semilogx(changing_parameter2, energies2, 'r+',label='_nolegend_')
        plt.xlabel('Number of k-points')
    else:
        if (Is_varying == 'smearing_factor'):
            plt.plot([k/(8.62*10**-5) for k in changing_parameter2], energies2,'r')
            plt.plot([k/(8.62*10**-5) for k in changing_parameter2], energies2, 'r+',label='_nolegend_')
            plt.xlabel('Smearing factor [K]')
        else:
            if (Is_varying == 'energy_cutoff'):
                changing_parameter2, energies2 = (list(t) for t in zip(*sorted(zip(changing_parameter2, energies2))))
            plt.plot(changing_parameter2, energies2,'r')
            plt.plot(changing_parameter2, energies2, 'r+',label='_nolegend_')
            plt.xlabel(r'$E_{cut}$'+' [eV]')


    plt.ylabel('Potential energy [eV/atom]')
    plt.legend(['1 atom', '64 atoms'],fancybox=True, framealpha=1,shadow=True,prop={'size': 10})
    plt.grid(True)
    #plt.show()
    #return energies, changing_parameter


def show_min_lc():
    en_lda, cp_lda = plot_from_db('lattice_constant', 'single_fe_LDA_bulk.db')
    en_pbe, cp_pbe = plot_from_db('lattice_constant', 'single_fe_PBE_bulk.db')
    en_blyp, cp_blyp = plot_from_db('lattice_constant', 'single_fe_BLYP_bulk.db')
    print('The min values in the dataset are:')
    print(cp_lda[en_lda.index(min(en_lda))])
    print(cp_pbe[en_pbe.index(min(en_pbe))])
    print(cp_blyp[en_blyp.index(min(en_blyp))])
    print('The min values in the fit are: ')
    ldav = np.polyfit(cp_lda, en_lda, 2)
    pbev = np.polyfit(cp_pbe, en_pbe, 2)
    blypv = np.polyfit(cp_blyp, en_blyp, 2)
    ldav = np.polyder(ldav)
    pbev = np.polyder(pbev)
    blypv = np.polyder(blypv)
    print(np.roots(ldav))
    print(np.roots(pbev))
    print(np.roots(blypv))

def bulk_modulus():

    energy, lattice_const = plot_from_db('lattice_constant', 'single_fe.db')

    second_order_coeffs = np.polyfit(lattice_const, energy, 2)

    print('The estimated lattice constant is:')

    second_order_coeffs_deriv = np.polyder(second_order_coeffs)
    estimated_lattice_const = (np.roots(second_order_coeffs_deriv))
    estimated_lattice_const = estimated_lattice_const[0]
    print(estimated_lattice_const)

    print('The values of the polynomial fit are:')

    print(second_order_coeffs)

    print('The bulk modulus (GPa) is found to be:')
    bulk_mod = 2*2*second_order_coeffs[0]*160.2*1/(9*estimated_lattice_const)
    print(bulk_mod)

    print('The speed of sound (m/s) is found to be:')
    density = 7.874*(1/1000)*(100**3)

    speed_of_sound = ((bulk_mod*10**9)/density)**(1/2)
    print(speed_of_sound)

    print('The Debye frequency (rad/s) is found to be:')
    number_density = 2/((estimated_lattice_const*10**(-10))**3)
    debye_freq = 6*np.pi*np.pi*number_density*(speed_of_sound)**3
    print((debye_freq)**(1/3))

    print('The Debye temperature (K) is found to be:')

    planck_con = 1.055*10**-34
    boltz_con = 1.381*10**-23

    print((planck_con/boltz_con)*debye_freq**(1/3))




plot_from_db_two_db('smearing_factor','fe_1atom.db','fe_kpts.db')
#plot_from_db('lattice_constant','single_fe_BLYP.db')
plt.show()

#bulk_modulus()
#plot_from_db('lattice_constant', 'single_cu_xc_BLYP.db')
#plt.show()
#show_min_lc()
#plt.savefig('my_fig.png')
#plot_from_db('lattice_constant', 'single_cu_xc_LDA2.db')
#plt.show()

#bulk_mat = bulk('Cu','fcc',3.62)*(4,4,4)


#del bulk_mat[[atom.index for atom in bulk_mat if atom.index != 45]]
#view(bulk_mat)




#
