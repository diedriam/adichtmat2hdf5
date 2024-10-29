# library to handle labchart export matfiles
# labchart export matfiles are saved in older matlab format
# which is limited in size for import into Matlab
# export block converts into newer matlab 4.7  hdf format
# it allows to import bigger files into Matlab
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-05-23

# tested with 
# python version
python 3.9.1

# requirements 
et_xmlfile==2.0.0
h5py==3.12.1
hdf5storage==0.1.19
np==1.0.2
numpy==1.22.4
openpyxl==3.1.5
pandas==2.2.3
python-dateutil==2.9.0.post0
pytz==2024.2
scipy==1.13.1
six==1.16.0
tzdata==2024.2
