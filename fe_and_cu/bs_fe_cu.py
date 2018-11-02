# Creates: bandstructure.png

# P1
from ase import Atoms, Atom
from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac
from ase.optimize.precon import PreconLBFGS
from ase.io.trajectory import Trajectory
import numpy as np
from ase.visualize import view
b = 2.86
k = 3
# Perform standard ground state calculation (with plane wave basis)
#si =  Atoms('Fe', scaled_positions=[(0, 0, 0)], magmoms=[k], cell=(b, b, b), pbc=True)
si = bulk('Fe','bcc',b)*(2,2,2)
si.set_initial_magnetic_moments([2.2,2.2,2.2,2.2,2.2,2.2,2.2,2.2])
del si[[atom.index for atom in si if atom.index == 0]]
si.append(Atom('Cu',(0,0,0)))


calc = GPAW(mode=PW(700),
            xc='PBE',
            kpts=(4, 4, 4),
            random=True,  # random guess (needed if many empty bands required)
            occupations=FermiDirac(0.1),
            txt='Si_gs.txt')
si.calc = calc

traj = Trajectory('some_test.traj', 'w', si)
relaxer = PreconLBFGS(si, variable_cell = True, logfile = 'my_log.txt')
relaxer.attach(traj)
relaxer.run(fmax = 0.025, smax = 0.003)

si.get_potential_energy()
calc.write('Si_gs.gpw')
# P2
# Restart from ground state and fix potential:
calc = GPAW('Si_gs.gpw',
            nbands=16,
            fixdensity=True,
            symmetry='off',
            kpts={'path': 'GHPNG', 'npoints': 60},
            convergence={'bands': 8}, txt='Si2_gs.txt')

calc.get_potential_energy()
e_f = calc.get_fermi_level()
# e, dos = calc.get_dos(spin=0, npts=2001, width=0.1)
#
# plt.figure(0)
# plt.plot(dos, e)
# plt.plot([0,4], e_f*np.ones(2),'r--')
# plt.ylim(-0.2,e_f+10)
# plt.xlim(0,4)
# plt.legend(['DOS', 'Fermi level'],fancybox=True, framealpha=1,shadow=True,prop={'size': 10})
# plt.xlabel('Density of states [1/eV]')
# plt.ylabel('Energy [eV]')
# plt.show()
#
# print(e_f)
# P3
bs = calc.band_structure()
bs.write('my_js.js')
bs.plot(filename='bandstructure_fe_cu.pdf',ylabel = 'Energies [eV]', show=True, emax=10.0)
# print(bs.energies)
