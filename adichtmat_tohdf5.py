import argparse
import adichtmat

def adichtmat_tohdf5(filename):
    ad = adichtmat.Adichtmatfile(filename)
    if ad.loadmat():
        ad.save_to_hdf5()

def main(args):
    adichtmat_tohdf5(args.filename)
 
if __name__ == "__main__":
   parser = argparse.ArgumentParser(description = "save adichtmat to hdf5")
   parser.add_argument("filename", type=str)
   args = parser.parse_args()
   main(args)