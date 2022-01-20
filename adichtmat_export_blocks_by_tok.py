# labchart export matfile are saved in older matlab format
# which is limited in size for import into Matlab
# this routine searches for identifier in records blocks
# and if tok is found it exports the block
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-11-23

from distutils import filelist
from adichtmat import Adichtmatfile
from xtokens import Xtoken, Xtokenset
import os
import sys
from pathlib import Path
from shutil import copyfile

def adichtmat_export_blocks_by_tok2(filename, tok_id = '', tok_longid='', tok_start='', tok_stop=''):
    """ export block identified by tok_longid and select interval defined by tok_start and tok_stop """

    if len(tok_id) > 0 & (len(tok_longid) > 0):
        tokens = [Xtoken(tok_id, tok_longid, tok_start, tok_stop)]
    else:
        xtokenset = Xtokenset()
        xtokenset.load()
        tokens = xtokenset.xtokens
    
    print(tokens)

    path = os.path.dirname(filename)
    fn_base = os.path.basename(filename)

    ad = Adichtmatfile(filename)
    ad.loadinfo()

    """ get comtab in form of df """
    comtab = ad.get_comments_table()   
    

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
                path_out = os.path.join(path, fn_root)

                if not os.path.isdir(path_out):
                    os.mkdir(path_out)
                print('export blk  ' + fn_root + '.mat' + '...')
                ad.export_block3(longid_blk, start_tick = start_tick, stop_tick = stop_tick, filename = os.path.join(path_out, fn_root+'.mat'))
            
                ''' copy pin file if available '''
                fn_pin = os.path.splitext(fn_base)[0] +'.pin'
                if os.path.join(path, fn_pin):
                    print('coping pin ' + fn_pin + '...')
                    copyfile(os.path.join(path, fn_pin), os.path.join(path_out, fn_root+'.pin'))

    print('adichtmat export by tok for ' + fn_base + ' done.')

def batch_adichtmat_export_blocks_bytok2(from_path =''):
    ext = '*.mat'
    file_list = list(Path(from_path).glob('**/' + ext))

    print(('running batch adichmat export blocks in {}...').format(from_path)) 
    for file in file_list:       
        print(('processing file {}...').format(file))
        adichtmat_export_blocks_by_tok2(str(file)) 

    return 
    print('batch done.') 
   

def main():
 
    if len(sys.argv) > 1:
        argcount = len(sys.argv)
        if argcount == 2:
            filename = sys.argv[1]
            print(filename)
            
            if os.path.isfile(filename):
               adichtmat_export_blocks_by_tok2(filename)     
            else:
                batch_adichtmat_export_blocks_bytok2(from_path = filename)
                   
        if len(sys.argv) == 4:
            adichtmat_export_blocks_by_tok2(sys.argv[1], sys.argv[2], sys.argv[3])
        if len(sys.argv) == 6:
            adichtmat_export_blocks_by_tok2(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        from_path = os.path.join(Path.home(),'tmp')
        #batch_adichtmat_export_blocks_bytok2(from_path = from_path)
        fn='/Users/diedriam/tmp/AD003H_DemT/2019-10-30_092700_AD003H_DemT_Day0.mat'
        adichtmat_export_blocks_by_tok2(fn,'NB','@Normal Breathing', '[BLK_NB','BLK_NB]')
if __name__ == "__main__":
    main()


