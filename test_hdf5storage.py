import adichtmat

filename = '/Users/diedriam/DATA/DATA_Local/AD045P_ThoS/2021-04-19_0800_AD045P_ThoS_Day0/2021-04-19_0800_AD045P_ThoS_Day0_edited_info.mat'
ad = adichtmat.adichtmatfile(filename)
ad.loadmat()
ad.save_to_hdf5()

print('done')