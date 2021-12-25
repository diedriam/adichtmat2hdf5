# saves file in hdf5 format
# labchart export matfile are saved in older matlab format
# which is limited in size for import into Matlab
# converts into newer format
# it allows to import bigger files into Matlab
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-11-23

import sys
import adichtmat

def adichtmat_saveto_hdf5(filename):

    ad = adichtmat.adichtmatfile(filename)
    ad.loadmat()
    ad.save_to_hdf5()

def main():
    script = sys.argv[0]
    filename = sys.argv[1]
    adichtmat_saveto_hdf5(filename)

if __name__ == "__main__":
    main()
