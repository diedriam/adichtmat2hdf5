import h5py


filename = '/Users/diedriam/DATA_local/tmp/tmp/2022-09-28_080000_SubJ2_Day0_tilt_hdf5.mat'
with h5py.File(filename, "r") as f:
    print(list(f.keys()))
    
    data = f['data']

    
    print(data[0:10])