import adichtmat

filename = '/Users/diedriam/DATA/DATA_local/autodet1/2022-07-19_080000_AraJ_AD069P_Day0_tilt/2022-07-19_080000_AraJ_AD069P_Day0_tilt.mat'
ad = adichtmat.Adichtmatfile(filename)
ad.loadmat()
ad.save_to_hdf5()

print('done')