"""
exports blocks identified by token
"""
import argparse
import os
import sys
from pathlib import Path
from shutil import copyfile
import adichtmat_export_blocks_by_tok
from adichtmat import Adichtmatfile
from xtokens import Xtoken, Xtokenset   

def adichtmat_export_blocks_by_tok_batch(from_path,
    xtoken_def:str = "", ext=None) -> None:

    if not ext:
        ext = '*.mat'
    file_list = list(Path(from_path).glob('**/' + ext))

    print(f"running batch adichmat export blocks in {from_path}...") 
    for file in file_list: 
        if not (file.name.startswith(".") or str(file.parent).find('cuts') > 0 or file.name.find('hdf5') > 0): 
            print(f"processing file {file}...")
            try:
                adichtmat_export_blocks_by_tok.adichtmat_export_blocks_by_tok(file, 
                    xtoken_def = xtoken_def)
                print(f"processing file {file} done.")

            except:
                print(f"processing file {file} failed.")

    print('batch done.') 

def main(args):
    from_path = args.from_path
    if from_path == None:
        from_path = from_path = os.path.join(Path.home(),'tmp')
    adichtmat_export_blocks_by_tok_batch(from_path, ext = args.ext,
            xtoken_def = args.xtoken_def)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description = "export blocks by tok batch")
   parser.add_argument("-f", "--from_path", type=str, default = '')
   parser.add_argument("--ext", type=str, default = None)
   parser.add_argument("-x", "--xtoken_def", type=str, default="./conf/xtokens.json")
   args = parser.parse_args()
   main(args)


