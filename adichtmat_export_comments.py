# saves file in hdf5 format
# labchart export matfile are saved in older matlab format
# which is limited in size for import into Matlab
# converts into newer format
# it allows to import bigger files into Matlab
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-05-23

import argparse
import sys, getopt
from adichtmat import Adichtmatfile

def adichtmat_export_comments(filename):
    ad = Adichtmatfile(filename)
    ad.loadmat()
    ad.export_comments_table()

def main(args):
    adichtmat_export_comments(args.filename)
    
if __name__ == "__main__":
   parser = argparse.ArgumentParser(description = "export comments to text file")
   parser.add_argument("-f", "--filename", type=str)
   args = parser.parse_args()
   main(args)
