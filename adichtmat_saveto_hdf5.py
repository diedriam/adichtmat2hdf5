# saves file in hdf5 format
# labchart export matfile are saved in older matlab format
# which is limited in size for import into Matlab
# converts into newer format
# it allows to import bigger files into Matlab
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-05-09

import adichtmat

def adichtmat_saveto_hdf5(filename):

    ad = adichtmat.adichtmatfile(filename)
    ad.loadmat()
    ad.save_to_hdf5()

def main():
    #script = sys.argv[0]
    #filename = sys.argv[1]
    filename = '/Users/diedriam/DATA/DATA_Local/AD045P_ThoS/2021-04-19_0800_AD045P_ThoS_Day0/2021-04-19_0800_AD045P_ThoS_Day0_edited_info.mat'

    adichtmat_saveto_hdf5(filename)

main()
