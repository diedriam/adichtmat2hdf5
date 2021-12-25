import adichtmat
import os

filename= '/Users/diedriam/DATA/DATA_Local/tmp/2020-03-29_080000_LawB_AD043P_Day0_tilt.mat'

ad = adichtmat.adichtmatfile(filename)
ad.loadinfo()
ad.export_block()
