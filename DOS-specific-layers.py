import pyprocar
from pymatgen.io.vasp import Vasprun
import numpy as np
import matplotlib.pyplot as plt

# Load VASP calculation results to access DOS and structure data
vasprun = Vasprun('/Users/simrankumari/PHD_WORK/BACKUP/DOS-studies/ITO/vasprun.xml')
fermi_level = vasprun.efermi
structure = vasprun.final_structure

# Filter atoms for In, Sn, and O in the first two layers
z_min = min([site.coords[2] for site in structure.sites])
z_max_first_two_layers = z_min + 5.5  # Adjust based on layer thickness
in_atoms, sn_atoms, o_atoms = [], [], []

for i, site in enumerate(structure.sites):
    if site.coords[2] <= z_max_first_two_layers:
        if site.specie.symbol == 'In':
            in_atoms.append(i)
        elif site.specie.symbol == 'Sn':
            sn_atoms.append(i)
        elif site.specie.symbol == 'O':
            o_atoms.append(i)

# Extract and sum DOS for selected atoms by species
def get_summed_dos(atoms):
    total_dos = None
    for atom in atoms:
        atom_dos = vasprun.complete_dos.get_site_dos(structure[atom])
        dos_energies = atom_dos.energies - fermi_level
        atom_total_dos = atom_dos.get_densities()
        if total_dos is None:
            total_dos = atom_total_dos
        else:
            total_dos += atom_total_dos
    return dos_energies, total_dos

# Get summed DOS for each species in the first two layers
energies, in_dos = get_summed_dos(in_atoms)
_, sn_dos = get_summed_dos(sn_atoms)
_, o_dos = get_summed_dos(o_atoms)

# Extract total DOS from all atoms
total_dos = vasprun.complete_dos.get_densities()

# Plot stacked DOS using matplotlib
plt.fill_between(energies, in_dos, label='In (First 2 Layers)', alpha=0.5)
plt.fill_between(energies, in_dos + sn_dos, in_dos, label='Sn (First 2 Layers)', alpha=0.5)
plt.fill_between(energies, in_dos + sn_dos + o_dos, in_dos + sn_dos, label='O (First 2 Layers)', alpha=0.5)

# Plot the total DOS on top of the stacked plot
plt.plot(energies, total_dos, color='black', label='Total DOS (All Atoms)', linewidth=1.5)

plt.axvline(0, color='k', linestyle='--', label="Fermi Level")
plt.xlim([-2, 2])
plt.xlabel("Energy (eV)")
plt.ylabel("DOS")
plt.legend()
plt.title("Stacked DOS for In, Sn, and O Atoms (First 2 Layers) with Total DOS")
plt.show()
