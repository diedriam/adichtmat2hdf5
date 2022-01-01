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
import sys
from shutil import copyfile



def adichtmat_export_blocks_by_token(filename, tokenid='', tokenvalue=''):

    if len(tokenid) > 0 & (len(tokenvalue) > 0):
        tokens = {tokenid: tokenvalue }
    else:
        tokens = {
            'VM': '@Valsalva Maneuver',
            'NB': '@Normal Breathing',
            'NS010': '@Necksuction 0.1 Hz',
            'NSRND': '@Randomized Neck Suction',
            'CB010': '@Controlled Breathing 0.1 Hz',
            'CB025': '@Controlled Breathing 0.25 Hz',
            'HV': '@Hyperventilation',
            'BH': '@Breathhold',
            'TT': '@HUT15',
        }
    print(tokens)

    tokenvalue_start = '[BLK_NB'
    tokenvalue_stop = 'BLK_NB]'
    tokenvalue_id = '@Normal Breathing'
    tokenid = 'NB'

    path = os.path.dirname(filename)
    fn_base = os.path.basename(filename)

    ad = adichtmat.adichtmatfile(filename)
    ad.loadinfo()
    comtab = ad.get_comments_table()   
    
    # TODO: convert to function for seaching token in comtab  

    start_tick = 0
    stop_tick = -1

    a = comtab[comtab.comments.str.startswith(tokenvalue_start)]
    if a.empty:
        ('start token not found')
        return -1

    start_tick = a.tick_pos.iloc[0]
    start_blk = a.blk_id.iloc[0]
    start_dtm = a.date_time.iloc[0]

    b = comtab[comtab.comments.str.startswith(tokenvalue_stop)]
    if b.empty:
        print('stop token not found')
        return -2

    stop_tick = b.tick_pos.iloc[-1]
    stop_blk = b.blk_id.iloc[0]-1
    stop_dtm = b.date_time.iloc[0]

    c = comtab[comtab.comments.str.startswith(tokenvalue_id)]
    if c.empty:
        print('stop token not found')
        return -2

    id_tick = c.tick_pos.iloc[-1]
    id_blk = c.blk_id.iloc[0]-1
    id_dtm = c.date_time.iloc[0]
    
    

    fn_root ='{}_blk{}_{}_T{}'.format(os.path.splitext(fn_base)[0], id_blk+1, tokenid, id_dtm.strftime('%H%M%S'))

    path_out = os.path.join(path, fn_root)
    if not os.path.isdir(path_out):
        os.mkdir(path_out)
    print('export blk  ' + fn_root + '.mat' + '...')
    ad.export_block2(id_blk, start_tick = start_tick, stop_tick = stop_tick, filename = os.path.join(path_out, fn_root+'.mat'))
    #ad.export_block(blk, filename = os.path.join(path_out, fn_root+'.mat'))
    

    ad.loaddata()
    for tokid, token in tokens.items():
        a = comtab[comtab.comments == token]
        blk_id = a.blk_id.astype(int)
        date_time = a.date_time
        for blk, dtm in zip(blk_id,date_time):

            fn_root ='{}_blk{}_{}_T{}'.format(os.path.splitext(fn_base)[0], blk+1, tokid, dtm.strftime('%H%M%S'))
            path_out = os.path.join(path, fn_root)

            if not os.path.isdir(path_out):
                os.mkdir(path_out)
            print('export blk  ' + fn_root + '.mat' + '...')
            ad.export_block(blk-1, filename = os.path.join(path_out, fn_root+'.mat'))

            ''' copy pin file if available '''
            fn_pin = os.path.splitext(fn_base)[0] +'.pin'
            if os.path.join(path, fn_pin):
                print('coping pin ' + fn_pin + '...')
                copyfile(os.path.join(path, fn_pin), os.path.join(path_out, fn_root+'.pin'))

    ad.export_comments_table()
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


