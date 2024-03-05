import os, sys, getopt
from adichtmat import Adichtmatfile

def adichtmat_export_comments_NIBP(filename):
    
    
    ad = Adichtmatfile(filename)
    ad.loadmat()
    
    df = ad.get_comments_table()
    df[['SBP','DBP','MBP','HR']] = df.comments.str.extract('@NIBP = (\d+)\s*/\s*(\d+)\s*\((\d+)\)\,\s*(\d+)')
    df.drop(columns=['sig_id','type_id','text_id','tick_pos'], inplace = True)

    path = os.path.dirname(ad.filename)
    fn_out = os.path.basename(ad.filename)
    fn_out = f'{os.path.join(path, os.path.splitext(fn_out)[0])}_comments_wNIBP.xlsx'
    print(f'export comments table {fn_out}...')
    df.to_excel(fn_out, index=False)
    print('export comments table with NIBP done.')

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
    adichtmat_export_comments_NIBP(inputfile)
    
if __name__ == "__main__":
   main(sys.argv[1:])
