import argparse
import sys
import adichtmat

def adichtmat_export_blocks(filename: str) -> None:
    # create object and load data
    ad = adichtmat.Adichtmatfile(filename)
    ad.loadmat()

    # export block data
    nblk = ad.get_blockcount()
    for indx in range(0, nblk - 1):
        ad.export_block(indx)
    # export comments     
    ad.export_comments_table()

def main(args):
    adichtmat_export_blocks(args.filename)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description = "export comments to text file")
   #parser.add_argument("filename", type=str)
   parser.add_argument("filename", type=str)
   args = parser.parse_args()
   main(args)

