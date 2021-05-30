import adichtmat

filename = '/Users/diedriam/DATA/DATA_Local/AD045P_ThoS/2021-04-19_0800_AD045P_ThoS_Day0/2021-04-19_0800_AD045P_ThoS_Day0_edited_info.mat'
filename = '/Users/diedriam/DATA/DATA_Local/AD045P_ThoS/2021-04-19_0800_AD045P_ThoS_Day0/cutted_files_day0/2021-04-19_0800_AD045P_ThoS_Day0_edited_HV_T155834.mat'
filename = '/Users/diedriam/DATA/DATA_Local/AD040H_HarbB/Recordings/2021-03-02_0900_HarB_AD040H_edit.mat'
filename = '/Users/diedriam/DATA/DATA_Local/AD045P_ThoS/2021-04-19_0800_AD045P_ThoS_Day0/cutted_files_day0/2021-04-19_0800_AD045P_ThoS_Day0_edited_HV_T155834.mat'
ad = adichtmat.adichtmatfile(filename)
ad.loadmat()
ad.save_to_hdf5()

print('done')