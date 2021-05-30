import adichtmat
import os

filename = '/Users/diedriam/DATA/DATA_Local/AD045P_ThoS/2021-04-19_0800_AD045P_ThoS_Day0/2021-04-19_0800_AD045P_ThoS_Day0_edited_info.mat'
filename = '/Users/diedriam/DATA/DATA_Local/AD040H_HarbB/Recordings/2021-03-02_0900_HarB_AD040H_edit.mat'
# filename = '/Users/diedriam/DATA/DATA_Local/AD045P_ThoS/2021-04-19_0800_AD045P_ThoS_Day0/cutted_files_day0/2021-04-19_0800_AD045P_ThoS_Day0_edited_HV_T155834.mat'
filename = '/Users/diedriam/DATA/DATA_Local/AD047P_SheA/2021-05-10_0800_AD047P_SheA_Day0/2021-05-10_0800_AD047P_SheA_Day0.mat'
filename = '/Users/diedriam/DATA/DATA_Local/AD048P_HavM/2021-05-19_0800_AD048P_HavM_Day0/2021-05-19_0800_AD048P_HavM_Day0.mat'
ad = adichtmat.adichtmatfile(filename)
ad.loadmat()
ad.export_comments_table()

comtab = ad.get_comments_table()

path = os.path.dirname(filename)
fn_base = os.path.basename(filename)



# define dicionary for id and token text
tokens = {
    'VM': '@Valsalva Maneuver',
    'NB': '@Normal Breathing',
    'NS010': '@Necksuction 0.1 Hz',
    'NSRND': '@Randomized Neck Suction',
    'CB010': '@Controlled Breathing 0.1 Hz',
    'CB025': '@Controlled Breathing 0.25 Hz',
    'HV': '@Hyperventilation',
    'BH': '@Breathhold',
    'TT': '@HUT15'
    }

#for (token, tokid) in tokens:
for tokid, token in tokens.items():
    a = comtab[comtab.comments == token]
    blk_id = a.blk_id
    date_time = a.date_time
    for blk, dtm in zip(blk_id,date_time):
        fn_out = '{}_blk{}_{}_T{}.mat'.format(os.path.splitext(fn_base)[0], blk, tokid, dtm.strftime('%H%M%S'))
        ad.export_block(blk-1, filename = os.path.join(path,fn_out))
print('test done.')

#ad.save_to_hdf5()

#ad.print_signames()
ad.export_comments_table()

#nblk = ad.get_blockcount()
#for indx in range(0,nblk-1):
#    ad.export_block(indx)
#print('test done.')
