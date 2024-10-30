import pyprocar
from pymatgen.io.vasp import Vasprun
import numpy as np
import matplotlib.pyplot as plt
import os
# Load VASP calculation results to access DOS and structure data
main_dir = os.path.dirname(os.path.abspath(__file__))
vasprun = Vasprun(main_dir + 'vasprun.xml')
fermi_level = vasprun.efermi
structure = vasprun.final_structure

# Filter atoms for In, Sn, O, H, and Pt in the first two layers
z_min = min([site.coords[2] for site in structure.sites])
z_max_first_two_layers = z_min + 5.5  # Adjust based on layer thickness
in_atoms, sn_atoms, o_atoms, h_atoms, pt_atoms = [], [], [], [], []

for i, site in enumerate(structure.sites):
    if site.coords[2] >= z_max_first_two_layers:
        if site.specie.symbol == 'In':
            in_atoms.append(i)
        elif site.specie.symbol == 'Sn':
            sn_atoms.append(i)
        elif site.specie.symbol == 'O':
            o_atoms.append(i)
        elif site.specie.symbol == 'H':
            h_atoms.append(i)
        elif site.specie.symbol == 'Pt':
            pt_atoms.append(i)

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
    return dos_energies, total_dos if total_dos is not None else np.zeros(len(dos_energies))

# Get summed DOS for each species in the first two layers, with exception handling
energies, in_dos = get_summed_dos(in_atoms)
_, sn_dos = get_summed_dos(sn_atoms) if sn_atoms else (energies, np.zeros(len(energies)))
_, o_dos = get_summed_dos(o_atoms)
_, h_dos = get_summed_dos(h_atoms) if h_atoms else (energies, np.zeros(len(energies)))
_, pt_dos = get_summed_dos(pt_atoms) if pt_atoms else (energies, np.zeros(len(energies)))

# Extract total DOS from all atoms
total_dos = vasprun.complete_dos.get_densities()

# Initialize the cumulative DOS with in_dos
cumulative_dos = in_dos

# Plot stacked DOS using matplotlib
plt.fill_between(energies, cumulative_dos, label='In (First 2 Layers)', alpha=0.5)

if sn_atoms:
    plt.fill_between(energies, cumulative_dos + sn_dos, cumulative_dos, label='Sn (First 2 Layers)', alpha=0.5)
    cumulative_dos += sn_dos

plt.fill_between(energies, cumulative_dos + o_dos, cumulative_dos, label='O (First 2 Layers)', alpha=0.5)
cumulative_dos += o_dos

if h_atoms:
    plt.fill_between(energies, cumulative_dos + h_dos, cumulative_dos, label='H (First 2 Layers)', alpha=0.5)
    cumulative_dos += h_dos

if pt_atoms:
    plt.fill_between(energies, cumulative_dos + pt_dos, cumulative_dos, label='Pt (First 2 Layers)', alpha=0.5)
    cumulative_dos += pt_dos

# Plot the total DOS on top of the stacked plot
plt.plot(energies, total_dos, color='black', label='Total DOS (All Atoms)', linewidth=1.5)

plt.axvline(0, color='k', linestyle='--', label="Fermi Level")
plt.xlim([-1, 1])
plt.ylim([0, 25])
plt.xlabel("Energy (eV)")
plt.ylabel("DOS")
plt.legend()
plt.savefig(main_dir + 'dos-low.png')
plt.show()
