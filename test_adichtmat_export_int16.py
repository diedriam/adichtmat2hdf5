
import hdf5storage
import matplotlib.pyplot as plt


fn='./hv_resp_vol_only_int16.mat'
mat_contents = hdf5storage.loadmat(fn)

# data has only 1 signal - no need to use pointer start, stop
y = mat_contents['data'][0]

# y is array int16 
# array([[-10666, -10667, -10667, ...,  -5755,  -5755,  -5754]], dtype=int16)

plt.plot(y)
plt.show()


fn = './tt.mat'
mat_contents = hdf5storage.loadmat(fn)
hdf5storage.write(mat_contents, '.', 'tt_pythonsave.mat', matlab_compatible=True, oned_as='col',
                          format='7.3')

