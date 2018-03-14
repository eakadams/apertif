#A script for getting data for Stefan
#Requested 20 subbands
#And separate fits files for phase and amplitude
#(No complex numbers)
#I will work in apercal environment as much as possible
#And access miriad routines there

import libs.lib as lib
import apercal

#start a log
lib.setup_logger('info', logfile='/home/adams/apertif/AAF/get_data.log')

#I am getting two different datasets:
#180216005 (Dwingeloo 1)
#180302009 (DR21)
#Will create almost empty configuration files for both
cfg1 = '/home/adams/apertif/AAF/180216005.cfg'
cfg2 = '/home/adams/apertif/AAF/180302009.cfg'


#Prepare data using Apercal
#This copies to directory defined in cfgfile
prepare = apercal.prepare(cfg1)
prepare.go()

prepare = apercal.prepare(cfg2)
prepare.go()


#Then convert the data to miriad file
convert = apercal.convert(cfg1)
convert.go()

convert = apercal.convert(cfg2)
convert.go()

#Now in miriad need to use uvimage to create image cube
#Want to limit number of channels
#Want to include near 9330, 20 subbands
#Subbands start at multiples of 64
#take subbands 130-149
#channels 8320, 9599


#move to directory where data is
ccal = apercal.ccal(cfg1)
ccal.director('ch', ccal.crosscaldir)

"""
#First use uvaver to select channels
#uvimage complains about too much data otherwise
uvaver = lib.miriad('uvaver')
uvaver.line='channel,1280,8320,1'
uvaver.vis = ccal.target+'mir'
uvaver.select='-auto'
uvaver.out=ccal.target+'tmp.mir'
uvaver.go()
"""

uvimage = lib.miriad('uvimage')
uvimage.vis = ccal.target+'mir' #uvaver.out
uvimage.view = 'amplitude'
targetname = ccal.target
uvimage.out= targetname+'_amp.im'
#still too much data so also select a time range
#parentheses in command so need double quote
uvimage.select="'-auto,time(11:00:00,12:00:00)'"
uvimage.line='channel,1280,8320,1'
uvimage.go()

#write to fits file
fits = lib.miriad('fits')
fits.in_ = uvimage.out
fits.op = "xyout"
fits.out = targetname+'_amp.fits'
fits.go()


#now do phase
uvimage.view='phase'
uvimage.out=targetname+'_phase.im'
uvimage.go()

fits.in_ = uvimage.out
fits.out = targetname+'_phase.fits'
fits.go()

#and now do the second source
#move directory
ccal = apercal.ccal(cfg2)
ccal.director('ch', ccal.crosscaldir)

#get subset of data
uvimage = lib.miriad('uvimage')
uvimage.vis = ccal.target+'mir' #uvaver.out
uvimage.view = 'amplitude'
targetname = ccal.target
uvimage.out= targetname+'_amp.im'
#still too much data so also select a time range
#parentheses in command so need double quote
uvimage.select="'-auto,time(04:00:00,05:00:00)'"
uvimage.line='channel,1280,8320,1'
uvimage.go()

fits.in_ = uvimage.out
fits.out = targetname+'_amp.fits'
fits.go()

#and phase of second source
uvimage.view='phase'
uvimage.out=targetname+'_phase.im'
uvimage.go()

fits.in_ = uvimage.out
fits.out = targetname+'_phase.fits'
fits.go()

#And that should be everything
