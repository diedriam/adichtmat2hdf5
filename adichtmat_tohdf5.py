"""
convert Labchar adichtmat exportfile into hdf5 matlabfile
otherwise large adichtmat exportfiles ar not readable by Matlab
"""
import argparse
from adichtmat import Adichtmatfile


def adichtmat_tohdf5(filename:str):
    """load mat and save in hdf5.mat file 

    Args:
        filename (str): source file name
    """
    ad = Adichtmatfile(filename)
    if ad.loadmat():
        ad.save_to_hdf5()

def main(filename):
    """
    main
    """
    adichtmat_tohdf5(filename)
     
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "save adichtmat to hdf5")
    parser.add_argument("filename", type=str)
    args = parser.parse_args()
    main(args.filename)