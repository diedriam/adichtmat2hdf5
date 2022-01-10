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

    path = os.path.dirname(filename)
    fn_base = os.path.basename(filename)

    ad = adichtmat.adichtmatfile(filename)
    ad.loadinfo()
    comtab = ad.get_comments_table()

    ad.loaddata()
    for tokid, token in tokens.items():
        a = comtab[comtab.comments == token]
        blk_id = a.blk_id.astype(int)
        date_time = a.date_time
        for blk, dtm in zip(blk_id,date_time):

            fn_root ='{}_blk{}_{}_T{}'.format(os.path.splitext(fn_base)[0], blk, tokid, dtm.strftime('%H%M%S'))
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
    if len(sys.argv) > 1:
        adichtmat_export_blocks_by_token(sys.argv[1])
        if len(sys.argv) == 4:
            adichtmat_export_blocks_by_token(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print('adichtmat_export_blocks_by_token: missing argument filename')


if __name__ == "__main__":
    main()


