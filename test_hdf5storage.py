import adichtmat

filename = '/Users/diedriam/DATA/DATA_Local/tmp/record_with_old_neuroamp.mat'
ad = adichtmat.Adichtmatfile(filename)
ad.loadmat()
ad.save_to_hdf5()

print('done')