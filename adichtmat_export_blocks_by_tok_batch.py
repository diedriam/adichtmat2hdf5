import argparse
from adichtmat import Adichtmatfile
from xtokens import Xtoken, Xtokenset   
import os
import sys
from pathlib import Path
from shutil import copyfile
import adichtmat_export_blocks_by_tok

def adichtmat_export_blocks_by_tok_batch(from_path,
    tok_id: str = '', tok_longid:str = '', 
    tok_start:str ='', tok_end:str = '', 
    xtoken_def:str = "", ext=None) -> None:

    if not ext:
        ext = '*.mat'
    file_list = list(Path(from_path).glob('**/' + ext))

    print(f"running batch adichmat export blocks in {from_path}...") 
    for file in file_list: 
        if not (file.name.startswith(".") or str(file.parent).find('cuts') > 0): 
            print(f"processing file {file}...")
            adichtmat_export_blocks_by_tok.adichtmat_export_blocks_by_tok(file, 
                tok_id = tok_id, tok_longid = tok_longid, 
                tok_start = tok_start, tok_end = tok_end, 
                xtoken_def = xtoken_def)
    print('batch done.') 

def main(args):
    from_path = args.from_path
    if from_path == None:
        from_path = from_path = os.path.join(Path.home(),'tmp')
        adichtmat_export_blocks_by_tok_batch(from_path, ext = args.ext,
                tok_id = args.tok_id, tok_longid = args.tok_longid, 
                tok_start = args.tok_start, tok_end = args.tok_end, 
                xtoken_def = args.xtoken_def)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description = "export blocks by tok batch")
   parser.add_argument("-f", "--from_path", type=str, default = None)
   parser.add_argument("--ext", type=str, default = None)
   parser.add_argument("-i", "--tok_id", default="")
   parser.add_argument("-l", "--tok_longid", type=str, default="")
   parser.add_argument("-s", "--tok_start", type=str, default="")
   parser.add_argument("-e", "--tok_end", type=str, default="")
   parser.add_argument("-x", "--xtoken_def", type=str, default="./conf/xtokens.json")
   args = parser.parse_args()
   main(args)


