# saves file in hdf5 format
# labchart export matfile are saved in older matlab format
# which is limited in size for import into Matlab
# converts into newer format
# it allows to import bigger files into Matlab
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-11-23

import argparse
import adichtmat

def adichtmat_saveto_hdf5(filename):

    ad = adichtmat.adichtmatfile(filename)
    ad.loadmat()
    ad.save_to_hdf5()

def main(args):
    adichtmat_saveto_hdf5(args.filename)


    adichtmat_export_blocks(args.filename)

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description = "save adichtmat to hdf5")
   #parser.add_argument("filename", type=str)
   parser.add_argument("filename", type=str)
   args = parser.parse_args()
   main(args)