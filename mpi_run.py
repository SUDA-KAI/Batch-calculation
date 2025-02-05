import os
import shutil
import joblib
import warnings
warnings.filterwarnings("ignore")
import numpy as np
from tqdm import tqdm
import sys
from pymatgen.io.vasp.sets import MPStaticSet, MPRelaxSet
from pymatgen.core import Structure
import subprocess
def run_vasp(_st, _res_dir):
    os.makedirs(_res_dir, exist_ok=True)
    try:
        vasp_input = MPStaticSet(_st, user_potcar_functional='PBE_54',)
        vasp_input.poscar.write_file(os.path.join(_res_dir, 'POSCAR'))
        vasp_input.incar.write_file(os.path.join(_res_dir, 'INCAR'))
        vasp_input.kpoints.write_file(os.path.join(_res_dir, 'KPOINTS'))
        vasp_input.potcar.write_file(os.path.join(_res_dir, 'POTCAR'))

        os.system(f'cd {_res_dir}; mpirun -np 16 vasp_std > vasp.log ')
        print(_res_dir, 'OK!')

    except:
        print(_res_dir, 'ERROR!')

def get_folders_from_index(main_folder, start_index, num_folders):
    folder_paths = []
    count = 0
    for i, folder in enumerate(os.listdir(main_folder)):
        full_path = os.path.join(main_folder, folder)
        if os.path.isdir(full_path):
            if i >= start_index:
                folder_paths.append(folder)
                count += 1
            if count == num_folders:
                break
    
    return folder_paths

main_folder = r"/public/home/yinwanjian/KAI/help_mg/I/perturb/stastic-more/"
st ,st_dir = [], []
index = int(sys.argv[1])
selected_folders = get_folders_from_index(main_folder, index, 40)
tasks = []

for path in selected_folders:
    res_dir = os.path.join(main_folder, path)
    poscar_path = os.path.join(res_dir, 'POSCAR')
    if os.path.exists(poscar_path):
        st = Structure.from_file(poscar_path)
        tasks.append((st, res_dir))

joblib.Parallel(n_jobs=4)(joblib.delayed(run_vasp)(st, res_dir) for st, res_dir in tqdm(tasks))

