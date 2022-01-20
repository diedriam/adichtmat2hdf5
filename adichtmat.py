# library to handle labchart export matfiles
# labchart export matfiles are saved in older matlab format
# which is limited in size for import into Matlab
# export block converts into newer matlab 4.7  hdf format
# it allows to import bigger files into Matlab
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-05-23


import hdf5storage
import os
import datetime as dt
import pandas as pd
import numpy as np


class Adichtmatfile(object):

    def __init__(self, filename):
        self.filename = filename
        self.matcontents = []

        self.data = []
        self.flg_loaded_info = False
        self.flg_loaded_data = False

    def loadmat(self):

        fn_in = os.path.basename(self.filename)
        print('loading adicht matlab file ' + fn_in + ' ... ')
        self.mat_contents = hdf5storage.loadmat(self.filename)
        print('loading adicht matlab file ' + fn_in + ' done. ')

        # reformat txt from char array to  string array as a one char array
        self.mat_contents[u'titles'] = self.strip_nparray_txt(self.mat_contents[u'titles'])
        self.mat_contents[u'unittext'] = self.strip_nparray_txt(self.mat_contents[u'unittext'])
        self.mat_contents[u'comtext'] = self.strip_nparray_txt(self.mat_contents[u'comtext'])

        self.flg_loaded_info = True
        self.flg_loaded_data = True

    def loadinfo(self):
        fn_in = os.path.basename(self.filename)
        params = [
            'blocktimes',
            'datastart',
            'dataend',
            'firstsampleoffset',
            'com',
            'comtext',
            'rangemax',
            'rangemin',
            'titles',
            'unittext',
            'unittextmap',
            'tickrate',
            'samplerate',
            'scaleunits',
            'scaleoffset',
        ]
        if ~self.flg_loaded_info:
            print('loading adicht matlab info ' + fn_in + ' ... ')
            self.mat_contents = hdf5storage.loadmat(self.filename, variable_names=params)
            print('loading adicht matlab info ' + fn_in + ' done. ')
            self.flg_loaded_info = True

    def loaddata(self):
        fn_in = os.path.basename(self.filename)
        if ~self.flg_loaded_data:
            print('loading adicht matlab data ' + fn_in + ' ... ')
            self.data = hdf5storage.loadmat(self.filename, variable_names='data')
            print('loading adicht matlab data ' + fn_in + ' done. ')
            self.flg_loaded_data = True

    @staticmethod
    def datenum_to_datetime(datenum):
        """
        Convert Matlab datenum into Python datetime.
        :param datenum: Date in matlab datenum format
        :return: Datetime object corresponding to datenum.
        """
        dayw = dt.datetime.fromordinal(int(datenum))
        dayfrac = dt.timedelta(days=datenum % 1) - dt.timedelta(days=366)
        return dayw + dayfrac

    @staticmethod
    def strip_nparray_txt(nparray_txt):
        if nparray_txt.ndim > 0:
            clean_txt = [txt.strip() for txt in nparray_txt]
        else:
            clean_txt = [nparray_txt.strip()]
        return clean_txt

    def get_blockcount(self):
        return len(self.mat_contents['blocktimes'][0, :])

    def get_blocktimes(self, *indx):
        if not indx:
            indx = range(0, self.get_blockcount())

        # convert mat datenum to python datetime
        datenums = self.mat_contents['blocktimes'][0, indx]
        blocktimes = [self.datenum_to_datetime(item) for item in datenums]
        return blocktimes

    def get_firstsampleoffset(self, *indx, blk = 0):
        if not indx:
            values = self.mat_contents['firstsampleoffset'][:, blk]
        else:
            values = self.mat_contents['firstsanpleoffset'][indx, blk]
        return values

    def get_datastart(self, *indx, blk = 0):
        if not indx:
            values = self.mat_contents['datastart'][:, blk]
        else:
            values = self.mat_contents['datastart'][indx, blk]
        return values.astype(np.int64)

    def get_dataend(self, *indx, blk = 0):
        if not indx:
            values = self.mat_contents['dataend'][:, blk]
        else:
            values = self.mat_contents['dataend'][indx, blk]
        return values.astype(np.int64)

    def get_datalen_smp(self, *indx, blk = 0):
        if not indx:
            values = self.mat_contents['dataend'][:, blk] - self.mat_contents['datastart'][:, blk] + 1
        else:
            values = self.mat_contents['dataend'][indx, blk] - self.mat_contents['datastart'][indx, blk] + 1

        return values

    def get_datalen_sec(self, *indx, blk = 0):
        if not indx:
            values = self.get_datalen_smp(blk = blk) / self.get_samplerates(blk = blk)
        else:
            values = self.get_datalen_smp(indx, blk = blk) / self.get_samplerates(indx, blk = blk)
        return values

    def get_datalen_ticks(self, *indx, blk = 0) -> np.int64:
        if not indx:
            values = self.get_datalen_sec(blk = blk) * self.get_tickrates(blk)
        else:
            values = self.get_datalen_sec(indx, blk = blk) * self.get_tickrates(blk)
        return values

    def get_rangemax(self, *indx, blk = 0):
        if not indx:
            values = self.mat_contents['rangemax'][:, blk]
        else:
            values = self.mat_contents['rangemax'][indx, blk]
        return values.astype(np.float64)

    def get_rangemin(self, *indx, blk=0):
        if not indx:
            values = self.mat_contents['rangemin'][:, blk]
        else:
            values = self.mat_contents['rangemin'][indx, blk]
        return values.astype(np.float64)

    def get_tickrates(self, *blk):
        # blk is block number counting from 0...
        if not blk:
            values = self.mat_contents['tickrate'][0, :]
        else:
            values = self.mat_contents['tickrate'][0, blk]
        return values.astype(np.float64)

    def get_samplerates(self, *indx, blk=0):
        if not indx:
            values = self.mat_contents['samplerate'][:, blk]
        else:
            values = self.mat_contents['samplerate'][indx, blk]
        return values

    def get_sigcount(self):
        count = len(self.mat_contents['titles'])
        return count

    def get_signames(self, *indx):
        if not indx:
            signames = self.mat_contents['titles']
        else:
            signames = self.mat_contents['titles'][indx]
        return signames

    def get_sigunits(self, *indx, blk=0):
        if not indx:
            unittextmap = self.mat_contents['unittextmap'][:, blk]
        else:
            unittextmap = self.mat_contents['unittextmap'][indx, blk]

        unittext = self.mat_contents['unittext'][unittextmap.astype(np.int64) - 1]

        return unittext

    def print_signames(self):
        signame = self.get_signames()
        for i, signame in enumerate(signame):
            print("signal {}: {}".format(i + 1, signame))


    def get_comments_table(self, blk = -1, from_tick_pos = 0, to_tick_pos = -1, format='long')-> pd.DataFrame:
        # blk is block number counting from 0, blk = blk_id -1
        # comtab: [sig_id, blk_id, tick_pos , type_id , text_id]
        # comments string = comtext[text_id]
        # note: labchart stores blk_id from 1...
        # note: labchart stores tick_pos from 0 = block start

        comtab = self.mat_contents['com']
        comtext = self.mat_contents['comtext']

        # get columns and format float to
        sig_id = comtab[:, 0].astype(np.int64)
        blk_id = comtab[:, 1].astype(np.int64)    # starts from 1
        tick_pos = comtab[:, 2].astype(np.int64)  # starts from 0
        type_id = comtab[:, 3].astype(np.int64)
        text_id = comtab[:, 4].astype(np.int64)

        comments = [comtext[id - 1].strip() for id in text_id]

        block_times = self.get_blocktimes()
        tick_rates = self.get_tickrates()
        date_time = [block_times[blk_id[i] - 1] +
                     dt.timedelta(seconds=tick_pos[i] / tick_rates[blk_id[i] - 1])
                     for i, com in enumerate(comments)]

        if format == 'reduced':
            data = {'date_time': date_time, 'comments': comments}
        else:
            data = {'date_time': date_time, 'comments': comments,
                    'blk_id': blk_id, 'sig_id': sig_id, 'type_id': type_id, 'text_id': text_id, 'tick_pos': tick_pos}

        df = pd.DataFrame.from_dict(data)
       

        if (blk > -1)  & (blk < self.get_blockcount()):
            df = df[df['blk_id'] == blk+1]

        if from_tick_pos > 0:
            df = df[ df.tick_pos >= from_tick_pos ]
        
        if to_tick_pos > from_tick_pos:
            df = df[ df.tick_pos <= to_tick_pos ]
     
        return df



    def find_comment(self, token: str, blk = -1, searchmode = 'contains', from_tick_pos = 0, to_tick_pos = -1, format='long') -> pd.DataFrame:
        """" searchmode can be contains (default) or startswith """
        # blk is block number counting from 0, blk = blk_id -1
        
        df = self.get_comments_table(blk = blk, from_tick_pos = from_tick_pos, to_tick_pos = to_tick_pos, format = format )

        if not df.empty:

            if searchmode == 'startswith':
                df = df[ df['comments'].str.startswith(token) ]
            else: 
                df = df[ df['comments'].str.contains(token) ]  

        return  df


    def export_comments_table(self):
        df = self.get_comments_table(format='long')
        path = os.path.dirname(self.filename)
        fn_out = os.path.basename(self.filename)
        fn_out = '{}.xlsx'.format(os.path.join(path, os.path.splitext(fn_out)[0]))
        print('export comments table {}...'.format(fn_out))
        df.to_excel(fn_out, index=False)
        print('export comments table done.')



    def export_block2(self, blk = 0, start_tick=0, stop_tick=-1, filename=''):
        # blk is block number counting from 0 -> blk = blk_id -1
        
        if not self.flg_loaded_info:
            self.loadinfo()
        
        blkcount = self.get_blockcount()
        if (blk < 0) | (blk > self.get_blockcount()):
            print('invalid block number')
            return -1

        datalen = self.get_datalen_ticks(blk = blk)
        tick_lenmax = max(datalen)
        if stop_tick == -1: 
            stop_tick = tick_lenmax


        # generate com info and comtext filtered by block
        com = self.mat_contents['com']

        # filter com table by block (col = 1)
        # we are using block number from 0,...
        # but in table block id counts from 1,...
        com = com[com[:, 1] == (blk+1)]

        # filter com table by tick_pos (col = 2) 
        if start_tick > 0:
            com = com[com[:, 2] >= start_tick]
        if stop_tick > start_tick:
            com = com[com[:, 2] <= stop_tick]

        # matlab has indx start from 1
        # ToDo generate list and index of unique text only
        indx = com[:, 4].astype(int) - 1
        comtext = self.mat_contents['comtext']
        comtext = np.array([comtext[i.astype(int)] for i in indx], dtype="object").reshape(-1, 1)
        com[:, 4] = range(1, len(indx) + 1)

        # correct block nr
        com[:, 1] = 1

        # correct tick_pos of comment
        com[:, 2] = com[:, 2] - start_tick

        # +1 for index matlab

        # get tickrate and samplerate of the present block
        tickrate = self.mat_contents['tickrate'][0, blk].astype(np.float64)
        samplerate = self.mat_contents['samplerate'][:, blk].astype(np.float64).reshape(-1, 1)
        blocktimes = self.mat_contents['blocktimes'][0, blk] + (start_tick / tickrate)/86400
        

        # transpose np arrays for matlab
        # we have to transpose the np arrays because of matlab
        # if we would choose save option oned_as = 'row' then strings are messed up in matlab
        # it was impossible to find a way to avoid this
        # so we transpose the np arrays instead

    
        sel_offset_sec = start_tick / tickrate
        sel_offset_smp = sel_offset_sec * samplerate
        sel_len_sec = (stop_tick - start_tick) / tickrate
        sel_len_smp = samplerate * sel_len_sec
     
        if (start_tick < 0) | (start_tick > tick_lenmax):
            print('error: start_tick out of range')
            return
        if (stop_tick < start_tick) | (stop_tick > tick_lenmax):
            print('error: smaller start_tick or stop_tick out of range')
            return

        '''calculate start end of selcted interval in original data '''
        datastart2 = self.mat_contents['datastart'][:, blk].reshape(-1, 1) + sel_offset_smp
        datastart2 = datastart2.flatten()
        dataend2 = datastart2 + sel_len_smp.flatten()

        firstsampleoffset = self.mat_contents['firstsampleoffset'][:, blk].astype(np.float64).reshape(-1, 1)
        titles = np.array(self.mat_contents['titles'], dtype="object").reshape(-1, 1)
        rangemax = self.mat_contents['rangemax'][:, blk].reshape(-1, 1).astype(np.float64)
        rangemin = self.mat_contents['rangemin'][:, blk].reshape(-1, 1).astype(np.float64)

        # filter unitextmap by block
        unittextmap = self.mat_contents['unittextmap'][:, blk].astype(np.float64).reshape(-1, 1)
        unittext = np.array(self.mat_contents['unittext'], dtype="object").reshape(-1, 1)

        if len(filename) == 0:
            filename = self.filename
            fn_out = os.path.basename(filename)
            # fn_out = '{}_blk{}_hdf5.mat'.format(os.path.splitext(fn_out)[0], blk.astype(int))
            fn_out = '{}_blk{}_hdf5.mat'.format(os.path.splitext(fn_out)[0], blk.astype(int)+1)
        else:
            fn_out = filename
        path = os.path.dirname(fn_out)

        print('export {}...'.format(fn_out))

        # create new dictionary for block export while keeping intact
        matblockdata = {}
        matblockdata[u'block_id_orig'] = blk+1
        matblockdata[u'start_tick_orig'] = start_tick
        matblockdata[u'stop_tick_orig'] = stop_tick

        datastart3 = 1 + (datastart2 - datastart2[0]).astype(np.float64)
        dataend3 = (dataend2 - datastart2[0]).astype(np.float64)

        matblockdata[u'blocktimes'] = blocktimes.astype(np.float64)
        matblockdata[u'datastart'] = datastart3.reshape(-1, 1)
        matblockdata[u'dataend'] = dataend3.reshape(-1, 1)
        matblockdata[u'firstsampleoffset'] = firstsampleoffset.astype(np.float64)
        matblockdata[u'titles'] = titles
        matblockdata[u'tickrate'] = tickrate.astype(np.float64)
        matblockdata[u'samplerate'] = samplerate.astype(np.float64)
        matblockdata[u'rangemax'] = rangemax.astype(np.float64)
        matblockdata[u'rangemin'] = rangemin.astype(np.float64)
        matblockdata[u'unittextmap'] = unittextmap
        matblockdata[u'unittext'] = unittext
        matblockdata[u'com'] = com
        matblockdata[u'comtext'] = comtext

        # check if scaleunit is present

        # check if scaleunit is present
        if 'scaleunits' in self.mat_contents:
            matblockdata[u'scaleunits'] = self.mat_contents['scaleunits'][:, blk].astype(np.float64).reshape(-1,1)
        if 'scaleoffset' in self.mat_contents:     
            matblockdata[u'scaleoffset'] = self.mat_contents['scaleoffset'][:, blk].astype(np.float64).reshape(-1, 1)

        if not self.flg_loaded_data:
            self.loaddata()

        # generate index is temporary solution
        # ToDo: using multiple slices at once would be better

        # indx = []
        # for ind in range(len(datastart)):
        #     indx += range(datastart[ind, 0].astype(int) - 1, dataend[ind, 0].astype(int))
        # indx = [indx, slice(datastart[ind, 0].astype(int) - 1, dataend[ind, 0].astype(int))]
        # indx = [slice( istart.astype(int), iend.astype(int)) for (istart , iend) in zip(datastart, dataend)]
       
        # slices = [slice( istart.astype(int)-1, iend.astype(int)-1) for (istart , iend) in zip(datastart2, dataend2)]
        # data3 = (self.data['data'][0][s] for s in slices)
        # does not work matblockdata[u'data']  = self.data['data'][0][slices]  

        # ranges = [range( istart.astype(int), iend.astype(int)) for (istart , iend) in zip(datastart2, dataend2)]
        # does not work matblockdata[u'data']  = self.data['data'][0][ranges]  

       
        ind = 0
        istart = datastart2.astype(int)-1
        iend = dataend2.astype(int)-1
         # remember a slice "0:n" selects data[0]...data[n-1]
        data=self.data['data'][0][istart[0]:iend[0]+1]
        
        datastart4 = datastart2
        dataend4  = dataend2
        datastart4[0] = 1
        dataend4[0] = sel_len_smp[0] + 1
        for ind in range(1,len(istart)):
            # remember a slice "0:n" selects data[0]...data[n-1]
            data = np.concatenate((data, self.data['data'][0][istart[ind]:iend[ind]+1]))
            datastart4[ind]=dataend4[ind-1]+1
            dataend4[ind] = datastart4[ind] + sel_len_smp[ind]
        matblockdata[u'data'] = data
        matblockdata[u'datastart'] = datastart4.reshape(-1, 1)
        matblockdata[u'dataend'] = dataend4.reshape(-1, 1)
       

        #following lines generate a cell array which is nice but Matlab can't mempap and index this variable
        #matblockdata[u'data'] = [self.data['data'][0][istart - 1:iend] for istart, iend in
        #                         zip(datastart2.astype(int), dataend2.astype(int))]
       

        # hdf5storage.write(matblockdata, '.', os.path.join(path, fn_out), matlab_compatible=True, oned_as='col',
        #                  format='7.3')
        hdf5storage.write(matblockdata, '.', os.path.join(path, fn_out), matlab_compatible=True, oned_as='col',
                          format='7.3')

        print(os.path.join(path, fn_out))
        print('export interval done.')
        return 1    

    def save_to_hdf5(self, filename=''):
        """
        saves file in hdf5 format
        labchart export matfile are saved in older matlab format
        which is limited in size for import into Matlab
        save_to_hdf5 converts into newer format
        it allows to import bigger files into Matlab
        """

        if len(filename) == 0:
            filename = self.filename

        path = os.path.dirname(self.filename)
        fn_out = os.path.basename(self.filename)
        fn_out = os.path.splitext(fn_out)[0] + '_hdf5.mat'

        # transpose np arrays for matlab
        # we have to transpose the np arrays because of matlab
        # if we would choose save option oned_as = 'row' then strings are messed up in matlab
        # it was impossible to find a way to avoid this
        # so we transpose the np arrays instead

        nblk = self.get_blockcount()
        self.mat_contents['datastart'] = self.mat_contents['datastart'].astype(np.float64).reshape(-1, nblk)
        self.mat_contents['dataend'] = self.mat_contents['dataend'].astype(np.float64).reshape(-1, nblk)
        self.mat_contents['firstsampleoffset'] = self.mat_contents['firstsampleoffset'].astype(np.float64).reshape(-1,
                                                                                                                   nblk)

        self.mat_contents['rangemax'] = self.mat_contents['rangemax'].astype(np.float64).reshape(-1, nblk)
        self.mat_contents['rangemin'] = self.mat_contents['rangemin'].astype(np.float64).reshape(-1, nblk)
        self.mat_contents['tickrate'] = self.mat_contents['tickrate'].astype(np.float64).reshape(-1, nblk)
        self.mat_contents['samplerate'] = self.mat_contents['samplerate'].astype(np.float64).reshape(-1, nblk)
        self.mat_contents['unittextmap'] = self.mat_contents['unittextmap'].astype(np.float64).reshape(-1, nblk)
        n = len(self.mat_contents['com'][0, :])
        self.mat_contents['com'] = self.mat_contents['com'].astype(np.float64).reshape(-1, n)

        self.mat_contents['titles'] = np.array(self.mat_contents['titles'], dtype="object").reshape(-1, 1)
        self.mat_contents['unittext'] = np.array(self.mat_contents['unittext'], dtype="object").reshape(-1, 1)
        self.mat_contents['comtext'] = np.array(self.mat_contents['comtext'], dtype="object").reshape(-1, 1)

        print('saving as hdf5 matlab file ' + fn_out + ' ...')
        hdf5storage.write(self.mat_contents, '.', os.path.join(path, fn_out), matlab_compatible=True, format='7.3')
        print('save hdf5 done.')
