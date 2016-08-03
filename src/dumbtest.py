from Preprocess import Preprocess, Drift_correction
import matplotlib.pyplot as plt
import tifffunc
import numpy as np
import os
import Cell_extract as CE
import glob



def main():
    # remove the comment from the line below: 
#     datapath = 'C:\username\Documents\......(fill it up)'
    hroot = '/Public/Zebrafish_ispim/'

    abspath = os.path.abspath(hroot)
    aq_date = '2016-03-21/'
    fd = abspath + aq_date
        
    im_list = glob.glob(fd+ '/*TP_*.tif') # list all the tiff files in the folder 
    
    ofst = 1
    for im_name in im_list:
        name_base = im_name[:-4]
        new_stack = np.copy(tifffunc.read_tiff(name_base))
        Drift_C = Drift_correction(new_stack, mfit = 7)
        a_stack = Drift_C.drift_correct(offset = ofst)
        name_out = name_base+'_a'
        tifffunc.write_tiff(a_stack[ofst:].astype('uint16'), name_out)


if __name__ == '__main__':
    main()

