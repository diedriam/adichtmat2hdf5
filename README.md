# adichtmat library to convert labchart export matfiles in hdf5
# which allows to import large files into matlab
#
# labchart export matfile are saved in older matlab format 
# adichtmat files are limited in size to be able to import into Matlab
# this program packet converts adichtmat files into hdf5 files 
# which can be imported without size limit
# 
# function adichtmat_tohdf5
# simple conversion of whole file into newer hdf5 format
#
# function adichtmat_export_blocks_by_tok
# this routine searches for identifier (tok_id) in records blocks files
# and if token is found it exports the block labeled with short tok_id
# start and stop can also be defined by tok_start and tok_end
# token can be defined in xtokens.json file
# 
# function adichtmat_export_blocks_by_tok_batch
# batch of adichtmat_export_blocks_by_tok for files located in from_path
# default from_path ="~/tmp"
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2024-10-30

# tested with python version
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
