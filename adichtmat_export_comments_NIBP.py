import argparse
import os
from adichtmat import Adichtmatfile

def adichtmat_export_comments_NIBP(filename:str, regexp:str = ""):   
    
    if regexp == "":
        regexp = "@NIBP = (\d+)\s*/\s*(\d+)\s*\((\d+)\)\,\s*(\d+)"
    
    ad = Adichtmatfile(filename)
    ad.loadmat()
    
    df = ad.get_comments_table()
    df[['SBP','DBP','MBP','HR']] = df.comments.str.extract(regexp)
    df.drop(columns=['sig_id','type_id','text_id','tick_pos'], inplace = True)

    path = os.path.dirname(ad.filename)
    fn_out = os.path.basename(ad.filename)
    fn_out = f'{os.path.join(path, os.path.splitext(fn_out)[0])}_comments_wNIBP.xlsx'
    
    print(f'export comments table {fn_out}...')
    df.to_excel(fn_out, index=False)
    print('export comments table with NIBP done.')

def main(args):
    adichtmat_export_comments_NIBP(args.filename, args.regexp)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "export comments with NIBP to Excel")
    parser.add_argument("filename", type=str)
    parser.add_argument("-r", "--regexp", default="", type=str) 
    args = parser.parse_args()
    main(args)
