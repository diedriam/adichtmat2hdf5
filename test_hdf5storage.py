import adichtmat

filename = '/Users/diedriam/DATA/DATA_Local/tmp/record_with_old_neuroamp.mat'
ad = adichtmat.adichtmatfile(filename)
ad.loadmat()
ad.save_to_hdf5()

print('done')