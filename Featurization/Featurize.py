# IMPORTS -------------------------------------------------------------------------------

import copy, os

# CONSTANTS (Defined by the user as needed) ---------------------------------------------

ORCA_PATH = '/home/ubuntu/soft/orca/orca'   # <------- has to point to the orca software. Will be used to run orca via the command line (os)
cores = 16
X = "Br"   # <------- Define the atom of interest. This is needed to calculate VBur and find the relevant carbon atoms for UMAP.
file_prefix = ""

# DONT CHANGE! The dictionaries are used to switch between different Xs. Can also be expanded to other functional groups

FG_dict = {
    "B": {"remove_n_atoms": 3},
    "Br": {"remove_n_atoms": 1},
}

# FUNCTIONS ------------------------------------------------------------------------------

def get_text_from_file(file_name):

   f = open(file_name, "r")
   lines = f.readlines()
   f.close()

   return lines


def make_input_file(file_name, header, coordinates, footer):
   
   inp = open(file_name + ".txt", "w")
   inp.writelines(header)
   inp.writelines(coordinates)
   inp.writelines(footer)
   inp.close()


def make_new_folder(folder_name):
   os.system("mkdir " + folder_name)


def convert_smile_to_xyz(smile, file_name):
   temp = '"' + smile + '"'
   os.system("obabel -:" + temp + " -O " + file_name + ".xyz --gen3d")


# commands for Multiwfn to generate charges
pa_commands = {'Hirshfeld': '7\n1\n1\nn\n0\nq\n',
               'ADCH': '7\n11\n1\nn\n0\nq\n',
               'MK-ESP': '7\n13\n1\n\nn\n0\n0\nq\n',
               'CM5': '7\n16\n1\nn\n0\nq\n',
               'QTAIM': '17\n1\n1\n2\n7\n2\n1\n-10\nq\n'}

# parameters for output files processing 
pa_types={'Hirshfeld': {'search_target': 'Final atomic charges, after normalization', 'line_offset': 0, 'value_index': -1},
          'ADCH': {'search_target': 'Final atomic charges, after normalization', 'line_offset': 0, 'value_index': -1},
          'MK-ESP': {'search_target': ' Calculation of ESP took up wall clock time', 'line_offset': 2, 'value_index': -1},
          'CM5': {'search_target': 'Final atomic charges, after normalization', 'line_offset': 0, 'value_index': -1},
          'QTAIM': {'search_target': ' The atomic charges after normalization and atomic volumes:', 'line_offset': 0, 'value_index': -4},
          'IBO': {'search_target': 'IAO PARTIAL CHARGES', 'line_offset': 2, 'value_index': -1}}

# Bondi radii
VdW_radii = {'H': 1.20,
             'B': 1.92,
             'C': 1.70,
             'N': 1.55,
             'O': 1.52,
             'F': 1.47,
             'Si': 2.10,
             'P': 1.80,
             'S': 1.80,
             'Cl': 1.75,
             'As': 1.85,
             'Se': 1.90,
             'Br': 1.85,
             'Te': 2.06,
             'I': 1.98}


def get_molecule(filename):
    '''Returns molecule as a dictionary of the form:
    {1: {'type': H, 'coord': [0.0, 0.0, 0.0]}}'''
    with open(filename + '.xyz', 'r') as xyzfile:
        xyz_data = xyzfile.readlines()
        num_atoms = int(xyz_data[0])
        molecule = {}
        for i in range(num_atoms):
            atom_type, x, y, z = xyz_data[i+2].split()
            molecule[i+1] = {'type': atom_type, 'coord': [float(x), float(y), float(z)]}
    return molecule

def molecule_2_xyz(molecule, filename='out'):
    '''Generates .xyz file for molecule'''
    with open(filename + '.xyz', 'w') as f:
        f.write(f'{len(molecule)}\n')
        f.write('\n')
        for x in molecule:
            coord = '  '.join(str(x) for x in molecule[x]["coord"])
            f.write(f'{molecule[x]["type"]}    {coord}\n')
    return None

def get_atom_indeces(molecule, atom_type):
    '''Returns a list of indeces of all atom_type atoms in molecule'''
    indeces = [atom_index for atom_index in molecule if molecule[atom_index]['type'] == atom_type]
    n_indeces = len(indeces)
    # output check
    if n_indeces == 0:
        #print(f'Error: no {atom_type} atom was found')
        return
    elif n_indeces > 1:
        pass#print(f'Warning: {n_indeces} {atom_type} atoms were found, only the first one will be used')
    return indeces

def get_distance(x, y):
    '''Returns distance between points x and y in 3D space'''
    return ((y[0] - x[0])**2 + (y[1] - x[1])**2 + (y[2] - x[2])**2)**0.5

def closest_n_atoms_indeces(molecule, atom_index, num_atoms=1):
    '''Returns a list of indeces of num_atoms closest atoms to atom_index'''
    # input check
    if len(molecule) < num_atoms + 1:
        #print('Error: not enough atoms in molecule')
        return
    reference = molecule[atom_index]['coord']
    distances = [(atom_index, get_distance(molecule[atom_index]['coord'], reference)) for atom_index in molecule]
    distances = sorted(distances, key=lambda x: x[1])[1:num_atoms+1]
    return [x[0] for x in distances]

def closest_within_indeces(molecule, atom_index, radius=6):
    '''Returns list of indeces of all atoms within radius, sorted by distance'''
    dist = [(index, get_distance(molecule[atom_index]['coord'], molecule[index]['coord'])) for index in molecule]
    dist = sorted(filter(lambda x: x[1] < radius, dist), key=lambda x: x[1])
    return [x[0] for x in dist][1:]

def Vbur_prepare(molecule, metal_to_ligand=2.10):
    '''Returns modified molecule without functional group (Br or B(OH)2) and with X at the metal center'''
    molecule = copy.deepcopy(molecule)
    atom_index = get_atom_indeces(molecule, X)[0]
    for index in closest_n_atoms_indeces(molecule, atom_index, num_atoms=FG_dict[X]["remove_n_atoms"]):

        if X == "B":
            if molecule[index]['type'] == 'O':
                del molecule[closest_n_atoms_indeces(molecule, index, num_atoms=1)[0]]
                del molecule[index]

        if molecule[index]['type'] == 'C':
            atom_coord = molecule[atom_index]['coord']
            C_coord = molecule[index]['coord']
            C_to_atom_coord = [atom_coord[i] - C_coord[i] for i in range(3)]
            C_to_atom_coord_len = sum(x**2 for x in C_to_atom_coord)**0.5
            new_coord = [C_to_atom_coord[i] / C_to_atom_coord_len * metal_to_ligand + C_coord[i] for i in range(3)]
            molecule[atom_index]['type'] = 'X'
            molecule[atom_index]['coord'] = new_coord
        else:
            #print('Error: not a boronic acid')
            return
    return molecule

def Vbur_calc(molecule, metal_center='X', radius=3.5, grid=0.05, remove_H=True, VdW_radii=VdW_radii, coeff=1.17):
    '''Returns Vbur% value for the ligand attached to the metal_center'''
    exceptions = [metal_center]
    if remove_H: exceptions.append('H')
    metal_index = get_atom_indeces(molecule, metal_center)[0]
    coord_center = molecule[metal_index]['coord'][:]
    x0, y0, z0 = coord_center
    N_point = int(radius/grid)
    Vbur, Vfree = 0, 0
    close_atoms = closest_within_indeces(molecule, metal_index)
    for i in range(-N_point, N_point):
        for j in range(-N_point, N_point):
            for k in range(-N_point, N_point):
                point = [x0 + (i + 0.5)* grid, y0 + (j + 0.5) * grid, z0 + (k + 0.5) * grid]
                if get_distance(point, coord_center) < radius:
                    for index in close_atoms:
                        if (molecule[index]['type'] not in exceptions) and (get_distance(point, molecule[index]['coord']) < VdW_radii[molecule[index]['type']]*coeff):
                            Vbur += 1
                            break
                    else:
                        Vfree += 1
    return Vbur / (Vbur + Vfree) * 100

def calc_charges(basename, commands=pa_commands):
    '''Set up PA calculations with ORCA and Multiwfn'''
    # all electron orbitals calculation
    with open(f'{basename}_all_e.txt', 'w') as input:
        input.write(f'! wB97X old-TZVP\n! Pal16\n\n%maxcore 3700\n\n%scf\nMaxIter 500\nend\n\n* xyzfile 0 1 {basename}.xyz\n')
    os.system(f'{ORCA_PATH} {basename}_all_e.txt > {basename}_all_e.out')
    # with Multiwfn
    for pa_type in commands:
        with open(f'{basename}_{pa_type}.inp', 'w') as input:
            input.write(commands[pa_type])
        os.system(f'Multiwfn {basename}_all_e.gbw < {basename}_{pa_type}.inp > {basename}_{pa_type}.out')
        os.system(f'rm {basename}_{pa_type}.inp')
    # with ORCA (IBO)
    with open(f'{basename}_IBO.txt', 'w') as input:
        input.write(f'! wB97X old-TZVP\n! Pal16\n\n%maxcore 3700\n\n%scf\nMaxIter 500\nend\n\n%loc\nlocmet IAOIBO\nvirt false\nocc true\nt_core -100000.0\nend\n\n* xyzfile 0 1 {basename}.xyz\n')
    os.system(f'{ORCA_PATH} {basename}_IBO.txt > {basename}_IBO.out')
    return None

def extract_charges(basename, atom_index, pa_types=pa_types):
    '''Returns a list of partial charges for atom with atom_index'''
    charges = []
    for pa_type in pa_types:
        with open(f'{basename}_{pa_type}.out', 'r') as tmp:
            tmp = tmp.readlines()
        for i in range(len(tmp)):
            if pa_types[pa_type]['search_target'] in tmp[i]:
                charges.append(float(tmp[i + pa_types[pa_type]['line_offset'] + atom_index].strip().split()[pa_types[pa_type]['value_index']]))
                break
    return charges

def data_to_csv(lst, filename='results'):
    '''Generates .csv file with data from lst, lst must be a list of lists'''
    with open(filename + '.csv', 'a') as outfile:
        outfile.write(','.join(str(x) for x in lst) + '\n')
    return None

# MAIN -------------------------------------------------------------------------------

index = 0

assigned_list = open("assigned_list.txt", "w")
assigned_list.close()

smiles_list = get_text_from_file("dataset.txt")

header_geo_opt = get_text_from_file("inp_header_geo_opt.txt")
footer_geo_opt = get_text_from_file("inp_footer_geo_opt.txt")

header = get_text_from_file("inp_header.txt")
footer = get_text_from_file("inp_footer.txt")

if not os.path.exists("./results"):
   make_new_folder("results")

out_filename = 'results'
with open(out_filename + '.csv', 'w') as out:
    out.write('basename,Hirshfeld,ADCH,MK-ESP,CM5,QTAIM,IBO,Vbur\n')

for smile in smiles_list:

   os.chdir("./results")

   folder_name = str(index)

   if not os.path.exists("./" + folder_name):
      make_new_folder(folder_name)


      os.chdir("./" + folder_name)
      convert_smile_to_xyz(smile.strip("\n"), folder_name)

      geo = get_text_from_file(folder_name + ".xyz")
      geo.pop(0)
      geo.pop(0)

      make_new_folder("orca")
      make_new_folder("crest")
      make_new_folder("xtb")
   
      os.system(f"mv {folder_name}.xyz xtb")
      os.chdir("xtb")
      os.system(f"xtb {folder_name}.xyz --opt -P {cores} > {folder_name}_xtb.out 2>&1")
      print("xtb finished.\n")

      os.system(f"mv xtbopt.xyz ../crest")
      os.chdir("../crest")
      os.system(f"crest xtbopt.xyz --gfn2 -T {cores} > {folder_name}_crest.out 2>&1")
      print("crest finished.\n")

      os.system(f"mv crest_best.xyz ../orca")
      os.chdir("../orca")

      geo_lowest_e = get_text_from_file("crest_best.xyz")
      geo_lowest_e.pop(0)
      geo_lowest_e.pop(0)

      make_input_file(file_prefix + "_" + folder_name, header_geo_opt, geo_lowest_e, footer_geo_opt)

      os.system(ORCA_PATH + " " + file_prefix + "_" + folder_name + ".txt > out_" + folder_name + ".out")
      print("geometry optimization finished.\n")
   
      geo_lowest_e_opt = get_text_from_file(file_prefix + "_" + folder_name + ".xyz")
      geo_lowest_e_opt.pop(0)
      geo_lowest_e_opt.pop(0)

      make_input_file(file_prefix + "_param_" + folder_name, header, geo_lowest_e_opt, footer)

      os.system(ORCA_PATH + " " + file_prefix + "_param_" + folder_name + ".txt > out_param_" + folder_name + ".out")
      print("featurization part I finished.\n")

      # load the structure
      molecule = get_molecule("_" + folder_name)
      # determine index of C bonded to B
      atom_index = get_atom_indeces(molecule, X)[0]
      C_index = closest_n_atoms_indeces(molecule, atom_index, num_atoms=1)[0]   
      # calculate charges
      calc_charges("_" + folder_name)
      # extracht charges for C_index
      results = extract_charges("_" + folder_name, C_index)
      # calculate Vbur
      Vbur = Vbur_calc(Vbur_prepare(molecule, metal_to_ligand=2.05), grid=0.05, remove_H=False)
      # save results
      results = [folder_name] + results + [Vbur]
      print("featurization part II finished.\n")

      os.chdir("../../../")

   with open("assigned_list.txt", "a") as f:
      f.write(folder_name + ": " + smile)

   data_to_csv(results, filename=out_filename)

   print(f"{index + 1}/{len(smiles_list)} entries done.\n")

   index += 1
