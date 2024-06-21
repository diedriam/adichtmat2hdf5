# labchart export matfile are saved in older matlab format
# which is limited in size for import into Matlab
# this routine searches for identifier in records blocks
# and if tok is found it exports the block
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-11-23

from adichtmat import Adichtmatfile
from xtokens import Xtoken, Xtokenset   
import os
import sys
from pathlib import Path
from shutil import copyfile

def adichtmat_export_blocks_by_tok2(filename, tok_id = '', tok_longid='', tok_start='', tok_stop='', xtoken_def = "./conf/xtokens.json"):
    """ export block identified by tok_longid and interval defined by tok_start and tok_stop """

    if len(tok_id) > 0 & (len(tok_longid) > 0):
        tokens = [Xtoken(tok_id, tok_longid, tok_start, tok_stop)]
    else:
        xtokenset = Xtokenset(filename = xtoken_def)
        xtokenset.load()
        tokens = xtokenset.xtokens
    
    print(tokens)

    path = os.path.dirname(filename)
    fn_base = os.path.basename(filename)

    ad = Adichtmatfile(filename)
    ad.loadinfo()

    """ get comtab in form of df """
    comtab = ad.get_comments_table()   
    df = ad.get_comments_table() 

    """ extract NIBP """
    df[['SBP','DBP','MBP','HR']] = df.comments.str.extract('@NIBP = (\d+) / (\d+) \((\d+)\)\, (\d+)')
    df.drop(columns=['sig_id','type_id','text_id','tick_pos'], inplace = True)

    path = os.path.dirname(ad.filename)
    fn_out = os.path.basename(ad.filename)
    fn_out = '{}_comments_wNIBP.xlsx'.format(os.path.join(path, os.path.splitext(fn_out)[0]))
    print('export comments table {}...'.format(fn_out))
    df.to_excel(fn_out, index=False)
    print('export comments table with NIBP done.')

    for tok in tokens:
    
        # TODO: convert to function for seaching tok in comtab  
        tok_id = tok.tok_id
        tok_longid= tok.tok_longid
        tok_start = tok.tok_start
        tok_stop = tok.tok_stop

        
        
        """search main tok id """
        """time info in output filename is derived from main tokid"""
        c = ad.find_comment(tok_longid, searchmode = 'startswith')
    
        if c.empty:
            print('block for ' + tok_longid + ' not found.')
        else:
            
            """call procedure for each found longid tok """
            """it would be better to put this in function"""
            for index, row in c.iterrows():
                longid_tick = row.tick_pos
                longid_blk = row.blk_id-1 # we use blk = blk_id -1 counting from 0
                longid_dtm = row.date_time

                """"search for closest start tok before the longid"""

                start_tick = 0    
                if len(tok_start) > 0:
                    a = ad.find_comment(tok_start, longid_blk, to_tick_pos = longid_tick, searchmode = 'startswith')
                    if not a.empty:
                        start_tick = a.tick_pos.iloc[-1]
                    
                
                """search for closest stop tok after the longid"""
                stop_tick = -1   
                if len(tok_stop) > 0:
                    b = ad.find_comment(tok_stop, longid_blk, from_tick_pos = start_tick, searchmode = 'startswith')
                    if not b.empty:
                        stop_tick = b.tick_pos.iloc[0]
            
                fn_root ='{}_blk{}_{}_T{}'.format(os.path.splitext(fn_base)[0], longid_blk+1, tok_id, longid_dtm.strftime('%H%M%S'))
                path_out = os.path.join(path,'cuts')
                if not os.path.isdir(path_out):
                    os.mkdir(path_out)
                path_out = os.path.join(path,'cuts',fn_root)
                if not os.path.isdir(path_out):
                    os.mkdir(path_out)    
                print(f"export blk {fn_root}.mat ...")
                ad.export_block2(longid_blk, start_tick = start_tick, stop_tick = stop_tick, filename = os.path.join(path_out, fn_root+'.mat'))
                
                ''' copy pin file if available '''
                fn_pin = os.path.splitext(fn_base)[0] +'.pin'
                fnfull_pin = os.path.join(path, fn_pin)
                if os.path.isfile(fnfull_pin):
                    print(f"coping pin file {fn_pin} ...")
                    copyfile(fnfull_pin, os.path.join(path_out,fn_root+'.pin'))
                else:
                    print(f"pin file {fn_pin} not found.")
                        

    print(f"adichtmat export by tok for {fn_base} done.")

def batch_adichtmat_export_blocks_by_tok2(from_path =''):
    ext = '*.mat'
    file_list = list(Path(from_path).glob('**/' + ext))

    print(f"running batch adichmat export blocks in {from_path}...") 
    for file in file_list: 
        if not (file.name.startswith(".") or str(file.parent).find('cuts') > 0): 
            print(f"processing file {file}...")
            adichtmat_export_blocks_by_tok2(str(file)) 

    return 
    print('batch done.') 

def adichtmat_export():
    if len(sys.argv) > 1:
        argcount = len(sys.argv)
        if argcount == 2:
            filename = sys.argv[1]
            print(filename)
            
            if os.path.isfile(filename):
               adichtmat_export_blocks_by_tok2(str(filename))     
            else:
                batch_adichtmat_export_blocks_by_tok2(from_path = filename)
                   
        if len(sys.argv) == 4:
            adichtmat_export_blocks_by_tok2(sys.argv[1], sys.argv[2], sys.argv[3])
        if len(sys.argv) == 6:
            adichtmat_export_blocks_by_tok2(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        from_path = os.path.join(Path.home(),'tmp')
        from_path = '/Volumes/AD3/AutoDet_Data_Analysis/AutoDet1/by_test/NSRND/day0/POTS_F/AD071P_HunB/2022-08-09_080000_HunB_AD071P_Day0_tilt_blk29_NSRND_T121245/2022-08-09_080000_HunB_AD071P_Day0_tilt_blk29_NSRND_T121245.mat'
        batch_adichtmat_export_blocks_by_tok2(from_path = from_path)
    

def main():
    adichtmat_export()
    
if __name__ == "__main__":
    main()


