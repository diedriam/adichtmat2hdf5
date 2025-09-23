import argparse
import adichtmat

def adichtmat_tohdf5(filename):
    ad = adichtmat.Adichtmatfile(filename)
    if ad.loadmat():
        ad.save_to_hdf5()

def main(filename):
    adichtmat_tohdf5(filename)
     
if __name__ == "__main__":
    
   #parser = argparse.ArgumentParser(description = "save adichtmat to hdf5")
   #parser.add_argument("filename", type=str)
   #args = parser.parse_args()
   #main(args.filename)
   
   filename = "/Volumes/AD1/DATA_POTS1/DATA_POTS_VesyHab/170997_VesyHab/DATA/DATA_Recordings/sGVS007P_MorN/DATA_Recordings/2019-12-10_152600_sGVS007P_MorN_Acute_post/2019-12-10_152600_sGVS007P_MorN_Acute_post_edited.mat"
   main(filename)