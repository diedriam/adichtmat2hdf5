# saves file in hdf5 format
# labchart export matfile are saved in older matlab format
# which is limited in size for import into Matlab
# converts into newer format
# it allows to import bigger files into Matlab
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-05-23

import sys, getopt
from adichtmat import Adichtmatfile

def adichtmat_export_comments(filename):
    ad = Adichtmatfile(filename)
    ad.loadmat()
    ad.export_comments_table()

def main(argv):
    strhelp = 'adichtmat_export_comments.py -i <inputfile> -o <outputfile>'
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(strhelp)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(strhelp)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    
    adichtmat_export_comments(inputfile)
    
if __name__ == "__main__":
   main(sys.argv[1:])
