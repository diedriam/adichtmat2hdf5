import argparse
import os
from pathlib import Path
from adichtmat_tohdf5 import adichtmat_tohdf5

def adichtmat_tohdf5_batch(from_path, ext = None):
    if not ext:
        ext = '*.mat'
    file_list = list(Path(from_path).glob('**/' + ext))

    print(f"running batch adichmat to hdf5 in {from_path}...") 
    for file in file_list: 
        if not (file.name.startswith(".") or file.name.find('_hdf5') > 0): 
            print(f"processing file {file}...")
            adichtmat_tohdf5(file)
        else:    
            print(f"skip file {file}...")
            
    print('batch done.') 

def main(args):
    from_path = args.from_path
    if from_path == None:
        from_path = from_path = os.path.join(Path.home(),'tmp')
    adichtmat_tohdf5_batch(from_path, ext = args.ext)
             

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description = "save adichtmat to hdf5 batch")
   parser.add_argument("-f", "--from_path", type=str, default = '/Users/diedriam/tmp/tmp/')
   parser.add_argument("--ext", type=str, default = None)
   args = parser.parse_args()
   main(args)


