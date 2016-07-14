# ----------- Author: Dan Xie ------------------------
"""
This file deblurrs the in-plane image and deblurrs each image from its adjacent stacks 
"""

import tifffunc
import numpy as np
from skimage import filters
import pyfftw

class Preprocess(object):
    def __init__(self, impath, sig = 25):
        self.raw_stack = tifffunc.read_tiff(impath).astype('float') # load a raw image and convert to float type 
        self.cell_list = []
        self.current = 0 # just using an index
        self.new_stack = np.copy(self.raw_stack)
        self.Nslice = self.raw_stack.shape[0] # number of slices 
        self.px_num = self.raw_stack.shape[1:] # the number of pixels in x and y for each slice
        self.status = -1* np.ones(self.Nslice) # the status 
        self.sig = sig
        
        
        """
        status = -1: the slices are raw
        status = 0: current slice deblurred and aligned 
        status = 1: current slice deblurred but not aligned 
        """
    
    
    
    def image_high_trunc_inplane(self):
    # the idea comes from Nature-scientific reports,  3:2266.
    # im0: image 0 
    # method: filter method
    # ext: extension of the filter 
    # sig: width of the Gaussian filter
        sig = self.sig
        im0 = self.raw_stack[self.current]
        ifilt = filters.gaussian(im0, sigma=sig)
        iratio = im0/ifilt
        nmin = np.argmin(iratio) 
        gmin_ind = np.unravel_index(nmin, im0.shape) # global mininum of the index    
        sca =im0[gmin_ind]/(ifilt[gmin_ind])
        print(sca)
        im0 -= (ifilt*sca*0.98) # update the background-corrected image
        return im0


    def image_high_trunc_adjacent(self):
        sig = 3*self.sig
        # Should this be done after the in-plane deblurring is accomplished, or before that? 
        if self.current > 0 and self.current < (self.Nslice-1):
            i_mid = self.raw_stack[self.current]
            i_up = self.raw_stack[self.current-1]
            i_down = self.raw_stack[self.current+1]
            ifilt_up = filters.gaussian(i_up, sigma = sig)
            ifilt_down = filters.gaussian(i_down, sigma = sig)
            
            up_ratio = i_mid/ifilt_up
            down_ratio = i_mid/ifilt_down
            nmin_up = np.argmin(up_ratio)
            nmin_down = np.argmin(down_ratio)
            
            gind_up = np.unravel_index(nmin_up, self.px_num)
            gind_down = np.unravel_index(nmin_down, self.px_num)
            print(gind_up, gind_down)
            sca_up = i_mid[gind_up]/ifilt_up[gind_up]
            sca_down = i_mid[gind_down]/ifilt_down[gind_down]
            
            print('%.6f' %sca_up, '%.6f' %sca_down)
            
            i_mid -= 0.40*(sca_up*ifilt_up+sca_down*ifilt_down) # Pay attention: it means self.raw_stack changes!
            return i_mid
        else: 
            pass    
            # only the slices not on the border are corrected  
        
        
        # truncate image from neighbors

    def stack_high_trunc(self):
    # run stack_high_trunc for a whole stack 
        for ii in np.arange(self.Nslice):
            self.current = ii
            self.image_high_trunc_adjacent()
            self.image_high_trunc_inplane()
            
        
        self.new_stack = np.copy(self.raw_stack).astype('uint16')
        return self.new_stack
        



class Drift_correction(object):
    def __init__(self, raw_stack):
        self.stack = raw_stack
        self.nslices = raw_stack.shape[0]
        # have a raw stack
   
   
    def __pair_correct__(self,im1, im2):
        # correct a pair of images 
        ft_im = pyfftw.FFTW(im1, im2)
        
            
        
        
    def drift_correct_linear(self):
        im_ref = self.stack[0]
        for ii in np.arange(1, self.nslices):
            im_corr = self.stack[ii]
            

            im_ref = im_corr
            # do some correction 
            
            
            
        
        
    def drift_correct_gaussian(self):
        pass    
        



""" below are some shared functions
"""        