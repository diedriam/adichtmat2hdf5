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
import adichtmat

def adichtmat_export_comments(filename):
    ad = adichtmat.adichtmatfile(filename)
    ad.loadmat()
    ad.export_comments_table()

def main(argv):
    inputfile = ''
    outputfile = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('adichtmat_export_comments.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('adichtmat_export_comments.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('input file is "' + inputfile + '"')
    print('output file is "' + outputfile + '"')

    if inputfile=='':
        #    inputfile = '/Users/diedriam/DATA/DATA_Local/AD040H_HarbB/Recordings/2021-03-02_0900_HarB_AD040H_edit.mat'
        inputfile = '/Volumes/T7 Touch/DATA_POTS/DATA_POTS_AutoDet_Acute_Study_1/DATA/DATA_Recordings/AD048P_HavM/2021-05-19_0800_AD048P_HavM_Day0/2021-05-19_0800_AD048P_HavM_Day0.mat'
        try:
            adichtmat_export_comments(inputfile)
        except:
            print('adichtmat_export_comments.py error.')

if __name__ == "__main__":
   main(sys.argv[1:])
