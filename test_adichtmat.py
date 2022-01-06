# labchart export matfile are saved in older matlab format
# which is limited in size for import into Matlab
# this routine searches for identifier in records blocks
# and if token is found it exports the block
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-11-23

import adichtmat
import os
from shutil import copyfile



def adichtmat_export_blocks_by_token(filename, token_id = '', token_longid='', token_start='', token_stop=''):
    """ export block identified by token_longid and select interval defined by token_start and token_stop """

    if len(token_id) > 0 & (len(token_longid) > 0):
        tokens = {token_id: [token_longid, token_start, token_stop] }
    else:
        tokens = {
            'VM': ['@Valsalva Maneuver','[BLK_VM','VM_BLK]'],
            'NB': ['@Normal Breathing', '[BLK_NB','NB_BLK]'],
            'NS010': ['@Necksuction 0.1 Hz', '[BLK_NS010','NS010_BLK]'],
            'NSRND': ['@Randomized Neck Suction', '[BLK_NSRND','NSRND_BLK]'],
            'CB010': ['@Controlled Breathing 0.1 Hz', '[BLK_CB010','CB010_BLK]'],
            'CB025': ['@Controlled Breathing 0.25 Hz', '[BLK_CB025','CB025_BLK]'],
            'HV': ['@Hyperventilation', '[BLK_HV','HV_BLK]'],
            'BH': ['@Breathhold', '[BLK_BH','BH_BLK]'],
            'TT': ['@HUT15', '[BLK_TILT','TILT_BLK]'],
        }
    print(tokens)

    path = os.path.dirname(filename)
    fn_base = os.path.basename(filename)

    ad = adichtmat.adichtmatfile(filename)
    ad.loadinfo()

    """ get comtab in form of df """
    comtab = ad.get_comments_table()   
    

    for id, tok in tokens.items():
    
        # TODO: convert to function for seaching token in comtab  
        token_longid= tok[0]
        token_start = tok[1]
        token_stop = tok[2]
        
        
        """search main token id """
        """time info in output filename is derived from main tokenid"""
        c = ad.find_comment(token_longid, searchmode = 'startswith')
    
        if c.empty:
            print('block for ' + token_longid + ' not found.')
        else:
            
            """call procedure for each found longid token """
            """it would be better to put this in function"""
            for index, row in c.iterrows():
                longid_tick = row.tick_pos
                longid_blk = row.blk_id-1 # we use blk = blk_id -1 counting from 0
                longid_dtm = row.date_time

                """"search for closest start token before the longid""" 
                a = ad.find_comment(token_start, longid_blk, to_tick_pos = longid_tick, searchmode = 'startswith')
                if not a.empty:
                    start_tick = a.tick_pos.iloc[-1]
                else: 
                    start_tick = 0    
                """search for closest stop token after the longid"""
                b = ad.find_comment(token_stop, longid_blk, from_tick_pos = start_tick, searchmode = 'startswith')
                if not b.empty:
                    stop_tick = b.tick_pos.iloc[0]
                else:
                    stop_tick = -1    
            
                fn_root ='{}_blk{}_{}_T{}'.format(os.path.splitext(fn_base)[0], longid_blk+1, id, longid_dtm.strftime('%H%M%S'))
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

    print('adichtmat export by token for ' + fn_base + ' done.')


def main():
    filename = '/Users/diedriam/DATA/DATA_Local/tmp/TomM/2021-12-14_080000_TomM_AD059P_Day0_tilt.mat'
    adichtmat_export_blocks_by_token(filename)

    #if len(sys.argv) > 1:
    #    adichtmat_export_blocks_by_token(sys.argv[1])
    #    if len(sys.argv) == 4:
    #        adichtmat_export_blocks_by_token(sys.argv[1], sys.argv[2], sys.argv[3])
    #else:
    #    print('adichtmat_export_blocks_by_token: missing argument filename')


if __name__ == "__main__":
    main()


