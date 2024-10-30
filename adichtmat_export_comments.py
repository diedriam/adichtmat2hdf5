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
