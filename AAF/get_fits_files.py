#A script focused on the bit going from
#miriad data to subset in a fits file
#keep an eye on auto-correlations
#avoid the time consuming part of data copying


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


#Now in miriad need to use uvimage to create image cube
#Want to limit number of channels
#Want to include near 9330, 20 subbands
#Subbands start at multiples of 64
#take subbands 130-149
#channels 8320, 9599


#move to directory where data is
ccal = apercal.ccal(cfg1)
ccal.director('ch', ccal.crosscaldir)

uvimage = lib.miriad('uvimage')
uvimage.vis = ccal.target+'mir' #uvaver.out
uvimage.view = 'amplitude'
targetname = ccal.target
uvimage.out= targetname+'_amp_freq.im'
#still too much data so also select a time range
#parentheses in command so need double quote
uvimage.select="'-auto,time(11:00:00,12:00:00)'"
uvimage.line='channel,1280,8320,1'
uvimage.options = 'freq'
uvimage.mode=3
uvimage.go()

#write to fits file
fits = lib.miriad('fits')
fits.in_ = uvimage.out
fits.op = "xyout"
fits.out = targetname+'_amp_freq.fits'
fits.go()


#now do phase
uvimage.view='phase'
uvimage.out=targetname+'_phase_freq.im'
uvimage.vis = ccal.target+'mir' #uvaver.out
uvimage.select="'-auto,time(11:00:00,12:00:00)'"
uvimage.line='channel,1280,8320,1'
uvimage.options = 'freq'
uvimage.mode=3
uvimage.go()

fits.in_ = uvimage.out
fits.out = targetname+'_phase_freq.fits'
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
uvimage.out= targetname+'_amp_freq.im'
#still too much data so also select a time range
#parentheses in command so need double quote
uvimage.select="'-auto,time(04:00:00,05:00:00)'"
uvimage.line='channel,1280,8320,1'
uvimage.options = 'freq'
uvimage.mode=3
uvimage.go()

fits.in_ = uvimage.out
fits.out = targetname+'_amp_freq.fits'
fits.go()

#and phase of second source
uvimage.view='phase'
uvimage.out=targetname+'_phase_freq.im'
uvimage.view = 'amplitude'
uvimage.select="'-auto,time(04:00:00,05:00:00)'"
uvimage.line='channel,1280,8320,1'
uvimage.options = 'freq'
uvimage.mode=3
uvimage.go()

fits.in_ = uvimage.out
fits.out = targetname+'_phase_freq.fits'
fits.go()

#And that should be everything
