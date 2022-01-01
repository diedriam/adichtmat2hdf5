# library to handle labchart export matfiles
# labchart export matfiles are saved in older matlab format
# which is limited in size for import into Matlab
# export block converts into newer matlab 4.7  hdf format
# it allows to import bigger files into Matlab
# 
# TODO: check for input linits for each routine
#
# by Andre Diedrich
# created 2021-03-12
# last modified 2021-05-23


import hdf5storage
import os
import datetime as dt
import pandas as pd
import numpy as np


class adichtmatfile(object):


    def __init__(self, filename):
        self.filename = filename
        self.matcontents = {}
        self.data = []
        self.flg_loaded_info = False
        self.flg_loaded_data = False


    def loadmat(self):
        path = os.path.dirname(self.filename)
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
        path = os.path.dirname(self.filename)
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
                ]
        if ~self.flg_loaded_info:
            print('loading adicht matlab info ' + fn_in + ' ... ')
            self.mat_contents = hdf5storage.loadmat(self.filename, variable_names = params)
            print('loading adicht matlab info ' + fn_in + ' done. ')
            self.flg_loaded_info = True


    def loaddata(self): 
        path = os.path.dirname(self.filename)
        fn_in = os.path.basename(self.filename)  
        if ~self.flg_loaded_data:  
            print('loading adicht matlab data ' + fn_in + ' ... ')
            self.data = hdf5storage.loadmat(self.filename, variable_names = 'data')
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


    def get_blockcount(self) ->np.int64:
        return len(self.mat_contents['blocktimes'][0, :])


    def get_blocktimes(self, *indx):
        if not indx:
            indx = range(0, self.get_blockcount())
        # convert mat datenum to python datetime
        datenums = self.mat_contents['blocktimes'][0, indx]
        return [self.datenum_to_datetime(item) for item in datenums]
 

    def get_tickrates(self, *blk):
        if not blk:
            blk = range(0, self.get_blockcount())
        return self.mat_contents['tickrate'][0, blk]


    def get_samplerates(self, *indx, blk=0):
        if not indx:
            indx = range(0, self.get_sigcount())
        return self.mat_contents['samplerate'][indx, blk]


    def get_firstsampleoffset(self, *indx, blk=0):
        if not indx:
            indx = range(0, self.get_sigcount())
        return self.mat_contents['firstsanpleoffset'][indx, blk]


    def get_datastart(self, *indx, blk=0):
        if not indx:
            indx = range(0, self.get_sigcount())
        return self.mat_contents['datastart'][indx, blk]


    def get_dataend(self, *indx, blk=0):
        if not indx:
            indx = range(0, self.get_sigcount())
        return self.mat_contents['dataend'][indx, blk]


    def get_datalen_smp(self, *indx, blk=0):
        if not indx:
            indx = range(0, self.get_sigcount())
        #return self.mat_contents['dataend'][indx, blk]-self.mat_contents['datastart'][indx, blk]
        return np.concatenate(self.get_dataend(indx,blk=blk) - self.get_datastart(indx, blk=blk))      

    def get_datalen_sec(self, *indx, blk=0):
        if not indx:
            indx = range(0, self.get_sigcount())
        return np.concatenate(self.get_datalen_smp(indx, blk=blk)/self.get_samplerates(indx,blk=blk))


    def get_datalen_ticks(self, *indx, blk=0) ->np.int64:
        if not indx:
            indx = range(0, self.get_sigcount())
        return self.get_datalen_sec(indx, blk=blk) * self.get_tickrates(blk)

    def get_rangemax(self, *indx, blk=0):
        if not indx:
            indx = range(0, self.get_sigcount())
        return  self.mat_contents['rangemax'][indx, blk]
 

    def get_rangemin(self, *indx, blk=0):
        if not indx:
            indx = range(0, self.get_sigcount())
        return self.mat_contents['rangemin'][indx, blk]


    def get_sigcount(self):
        count = len(self.mat_contents['titles'])
        return count


    def get_signames(self, *indx):
        if not indx:
            indx = range(0, self.get_sigcount())
        return self.mat_contents['titles'][indx]


    def get_sigunits(self, *indx, blk=0):
        if not indx:
            indx = range(0, self.get_sigcount())
        unittextmap = self.mat_contents['unittextmap'][indx, blk]
        return self.mat_contents['unittext'][unittextmap.astype(np.int64) - 1]


    def print_signames(self):
        signame = self.get_signames()
        for i, signame in enumerate(signame):
            print("signal {}: {}".format(i + 1, signame))


    def get_comments_table(self, *blk, format='all') -> pd.DataFrame:
        # comtab: [sig_id, blk_id, tick_pos , type_id , text_id]
        # comments string = comtext[text_id]

        comtab = self.mat_contents['com']
        comtext = self.mat_contents['comtext']

        # get columns and format float to
        sig_id = comtab[:, 0].astype(np.int64)
        blk_id = comtab[:, 1].astype(np.int64)
        tick_pos = comtab[:, 2].astype(np.int64)
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
        return pd.DataFrame.from_dict(data)


    def export_comments_table(self):
        df = self.get_comments_table(format='long')
        path = os.path.dirname(self.filename)
        fn_out = os.path.basename(self.filename)
        fn_out = '{}.xlsx'.format(os.path.join(path, os.path.splitext(fn_out)[0]))
        print('export comments table {}...'.format(fn_out))
        df.to_excel(fn_out, index=False)
        print('export comments table done.')

    def export_block(self, blk=0, filename=''):

        if not self.flg_loaded_info:
            self.loadinfo()

        blocktimes = self.mat_contents['blocktimes'][blk]
        datastart = self.mat_contents.get('datastart', [])
        if len(datastart) == 0:
            return

        # transpose np arrays for matlab
        # we have to transpose the np arrays because of matlab
        # if we would choose save option oned_as = 'row' then strings are messed up in matlab
        # it was impossible to find a way to avoid this
        # so we transpose the np arrays instead

        datastart = self.mat_contents['datastart'][:, blk].astype(np.float64).reshape(-1, 1)
        dataend = self.mat_contents['dataend'][:, blk].astype(np.float64).reshape(-1, 1)
        firstsampleoffset = self.mat_contents['firstsampleoffset'][:, blk].astype(np.float64).reshape(-1, 1)
        titles = np.array(self.mat_contents['titles'], dtype="object").reshape(-1, 1)
        rangemax = self.mat_contents['rangemax'][:, blk].reshape(-1, 1).astype(np.float64)
        rangemin = self.mat_contents['rangemin'][:, blk].reshape(-1, 1).astype(np.float64)

        tickrate = self.mat_contents['tickrate'][0, blk].astype(np.float64)
        samplerate = self.mat_contents['samplerate'][:, blk].astype(np.float64).reshape(-1, 1)
        # filter unitextmap by block
        unittextmap = self.mat_contents['unittextmap'][:, blk].astype(np.float64).reshape(-1, 1)
        unittext = np.array(self.mat_contents['unittext'], dtype="object").reshape(-1, 1)

        # generate com info and comtext filtered by block
        com = self.mat_contents['com']
        # filter com table by block
        com = com[com[:, 1] == blk + 1]

        indx = com[:, 4].astype(int)
        # matlab has indx start from 1
        # ToDo generate list and index of unique text only
        comtext = self.mat_contents['comtext']
        comtext = np.array([comtext[i.astype(int) - 1] for i in indx], dtype="object").reshape(-1, 1)

        # +1 for index matlab
        com[:, 4] = range(1, len(indx) + 1)

        # set block
        com[:, 1] = 1


        if len(filename) == 0:
            filename = self.filename
            fn_out = os.path.basename(filename)
            # fn_out = '{}_blk{}_hdf5.mat'.format(os.path.splitext(fn_out)[0], blk.astype(int))
            fn_out = '{}_blk{}_hdf5.mat'.format(os.path.splitext(fn_out)[0], blk)
        else:
            fn_out = filename
        path = os.path.dirname(fn_out)

        print('export {}...'.format(fn_out))

        # create new dictionary for block export while keeping intact
        matblockdata = {}
        matblockdata[u'blocknr_orig'] = blk + 1
        matblockdata[u'blocktimes'] = blocktimes.astype(np.float64)
        matblockdata[u'datastart'] = 1+(datastart - datastart[0, 0]).astype(np.float64)
        matblockdata[u'dataend'] = 1+(dataend - datastart[0, 0]).astype(np.float64)
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
        
        if 'scaleunits' in self.mat_contents:
            matblockdata[u'scaleunits'] = self.mat_contents.get(['scaleunits'])[:, blk].astype(np.float64).reshape(-1, 1)
             matblockdata[u'scaleoffset'] = self.mat_contents['scaleoffset'][:, blk].astype(np.float64).reshape(-1, 1)
        
        if not self.flg_loaded_data:
            self.loaddata()

       
        # generate index is temporary solution
        # ToDo: using multiple slices at once would be better

        #indx = []
        #for ind in range(len(datastart)):
        #     indx += range(datastart[ind, 0].astype(int) - 1, dataend[ind, 0].astype(int))
        # indx = [indx, slice(datastart[ind, 0].astype(int) - 1, dataend[ind, 0].astype(int))]
        #indx = [slice( istart.astype(int), iend.astype(int)) for (istart , iend) in zip(datastart, dataend)]
        # matblockdata[u'data']  = self.data['data'][0][indx]

        matblockdata[u'data']  = [self.data['data'][0][istart[0]-1:iend[0]] for istart , iend in zip(datastart.astype(int),dataend.astype(int))]
        #hdf5storage.write(matblockdata, '.', os.path.join(path, fn_out), matlab_compatible=True, oned_as='col',
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
        self.mat_contents['firstsampleoffset'] = self.mat_contents['firstsampleoffset'].astype(np.float64).reshape(-1, nblk)

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
