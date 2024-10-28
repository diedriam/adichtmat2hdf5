# saves file in hdf5 format
# labchart export matfile are saved in older matlab format
# which is limited in size for import into Matlab
# converts into newer format
# it allows to import bigger files into Matlab
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-05-09

import sys
import adichtmat


def adichtmat_export_blocks(filename):

    ad = adichtmat.Adichtmatfile(filename)
    ad.loadmat()

    nblk = ad.get_blockcount()
    for indx in range(0, nblk - 1):
        ad.export_block(indx)
    ad.export_comments_table()

def main():
    script = sys.argv[0]
    filename = sys.argv[1]
    adichtmat_export_blocks(filename)

if __name__ == "__main__":
    main()

