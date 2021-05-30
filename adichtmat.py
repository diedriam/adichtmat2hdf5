import hdf5storage
import os
import datetime as dt
import pandas as pd
import numpy as np


class adichtmatfile(object):

    def __init__(self, filename):
        self.filename = filename
        self.matcontents = []

    def loadmat(self):
        path = os.path.dirname(self.filename)
        fn_in = os.path.basename(self.filename)
        print('loading adicht matlab file ' + fn_in + ' ... ')
        self.mat_contents = hdf5storage.loadmat(self.filename)

        # reformat txt from char array to  string array as a on char array
        self.mat_contents[u'titles'] = self.strip_nparray_txt(self.mat_contents[u'titles'])
        self.mat_contents[u'unittext'] = self.strip_nparray_txt(self.mat_contents[u'unittext'])
        self.mat_contents[u'comtext'] = self.strip_nparray_txt(self.mat_contents[u'comtext'])

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

    def get_firstsampleoffset(self, *indx, blk=1):
        if not indx:
            values = self.mat_contents['firstsampleoffset'][:, blk]
        else:
            values = self.mat_contents['firstsanpleoffset'][indx, blk]
        return values

    def get_datastart(self, *indx, blk=1):
        if not indx:
            values = self.mat_contents['datastart'][:, blk]
        else:
            values = self.mat_contents['datastart'][indx, blk]
        return values

    def get_dataend(self, *indx, blk=1):
        if not indx:
            values = self.mat_contents['dataend'][:, blk]
        else:
            values = self.mat_contents['dataend'][indx, blk]
        return values

    def get_rangemax(self, *indx, blk=1):
        if not indx:
            values = self.mat_contents['rangemax'][:, blk]
        else:
            values = self.mat_contents['rangemax'][indx, blk]
        return values

    def get_rangemim(self, *indx, blk=1):
        if not indx:
            values = self.mat_contents['rangemin'][:, blk]
        else:
            values = self.mat_contents['rangemin'][indx, blk]
        return values

    def get_tickrates(self, *indx):
        if not indx:
            values = self.mat_contents['tickrate'][0, :]
        else:
            values = self.mat_contents['tickrate'][0, indx]
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

    def get_sigunits(self, *indx, blk=1):
        if not indx:
            unittextmap = self.mat_contents['unittextmap'][:, blk].astype('int')
        else:
            unittextmap = self.mat_contents['unittextmap'][indx, blk].astype('int')

        unittext = self.mat_contents['unittext'][unittextmap - 1]

        return unittext

    def print_signames(self):
        signame = self.get_signames()
        for i, signame in enumerate(signame):
            print("signal {}: {}".format(i + 1, signame))

    def get_comments_table(self, *blk, format='all'):
        # comtab: [sig_id, blk_id, tick_pos , type_id , text_id]
        # comments string = comtext[text_id]

        comtab = self.mat_contents['com']
        comtext = self.mat_contents['comtext']

        # get columns and format float to
        sig_id = comtab[:, 0].astype('int')
        blk_id = comtab[:, 1].astype('int')
        tick_pos = comtab[:, 2].astype('long')
        type_id = comtab[:, 3].astype('int')
        text_id = comtab[:, 4].astype('int')

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

        return df

    def export_comments_table(self):
        df = self.get_comments_table(format='long')
        path = os.path.dirname(self.filename)
        fn_out = os.path.basename(self.filename)
        fn_out = '{}.xlsx'.format(os.path.join(path, os.path.splitext(fn_out)[0]))
        print('export comments table {}...'.format(fn_out))
        df.to_excel(fn_out, index=False)
        print('export comments table done.')

    def export_block(self, blk=0, filename=''):
        blocktimes = self.mat_contents['blocktimes'][0, blk]
        datastart=self.mat_contents.get('datastart',[])
        if len(datastart) == 0:
            return

        # transpose row and columns for matlab
        datastart = self.mat_contents['datastart'][:,blk].astype('int').reshape(-1,1)
        dataend = self.mat_contents['dataend'][:,blk].astype('int').reshape(-1,1)
        firstsampleoffset = self.mat_contents['firstsampleoffset'][:, blk].astype('int').reshape(-1,1)
        titles = np.array(self.mat_contents['titles'], dtype="object").reshape(-1,1)
        rangemax = self.mat_contents['rangemax'][:, blk].reshape(-1,1)
        rangemin = self.mat_contents['rangemin'][:, blk].reshape(-1,1)
        tickrate = self.mat_contents['tickrate'][0, blk]
        samplerate = self.mat_contents['samplerate'][:, blk].reshape(-1,1)
        # filter unitextmap by block
        unittextmap = self.mat_contents['unittextmap'][:, blk].reshape(-1,1)
        unittext = np.array(self.mat_contents['unittext'], dtype="object").reshape(-1,1)

        # generate com info and comtext filtered by block
        com = self.mat_contents['com']
        # filter com table by block
        com = com[com[:, 1] == blk + 1]
        indx = com[:,4].astype('int')
        # matlab has indx start from 1
        # ToDo generate list and index of unique text only
        comtext = self.mat_contents['comtext']
        comtext = np.array([comtext[i-1] for i in indx],dtype="object").reshape(-1, 1)

        # +1 for index matlab
        com[:, 4] = range(1, len(indx) + 1)

        # set block
        com[:, 1] = 1

        data = self.mat_contents.get('data', [])
        # if len(data) > 0:

        # generate index is temporary solution
        # ToDo: using multiple slices at once would be better

        indx = []
        for ind in range(len(datastart)):
            indx += range(datastart[ind,0] - 1, dataend[ind,0])

        if len(filename) == 0:
            filename = self.filename
            fn_out = os.path.basename(filename)
            fn_out = '{}_blk{}_hdf5.mat'.format(os.path.splitext(fn_out)[0],blk)
        else:
            fn_out = filename
        path = os.path.dirname(fn_out)

        print('export {}...'.format(fn_out))

        # create new dictionary for block export while keeping intact
        matblockdata = {}
        matblockdata[u'blocknr_orig'] = blk + 1
        matblockdata[u'blocktimes'] = blocktimes
        matblockdata[u'datastart'] = datastart - datastart[0,0]
        matblockdata[u'dataend'] = dataend - datastart[0,0]
        matblockdata[u'firstsampleoffset'] = firstsampleoffset
        matblockdata[u'titles'] = titles
        matblockdata[u'tickrate'] = tickrate
        matblockdata[u'samplerate'] = samplerate
        matblockdata[u'rangemax'] = rangemax
        matblockdata[u'rangemin'] = rangemin
        matblockdata[u'unittextmap'] = unittextmap
        matblockdata[u'unittext'] = unittext
        matblockdata[u'com'] = com
        matblockdata[u'comtext'] = comtext
        matblockdata[u'data'] = data[0][indx]
        # hdf5storage.write(matblockdata, '.', os.path.join(path,fn_out), matlab_compatible=True, oned_as='column', format='7.3')
        hdf5storage.write(matblockdata, '.', os.path.join(path, fn_out), matlab_compatible=True, oned_as='col',
                          format='7.3')
        print('export block done.')
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

        print('saving as hdf5 matlab file ' + fn_out + ' ...')
        hdf5storage.write(self.mat_contents, '.', os.path.join(path,fn_out), matlab_compatible=True, oned_as='column', format='7.3')
        print('save hdf5 done.')