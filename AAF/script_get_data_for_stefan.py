#A script for getting data for Stefan
#Requested 20 subbands
#And separate fits files for phase and amplitude
#(No complex numbers)
#I will work in apercal environment as much as possible
#And access miriad routines there

import libs.lib as lib
import apercal

#I am getting two different datasets:
#180216005 (Dwingeloo 1)
#180302009 (DR21)
#Will create almost empty configuration files for both
cfg1 = '/home/adams/apertif/AAF/180216005.cfg'
cfg2 = '/home/adams/apertif/AAF/180302009.cfg'


#Prepare data using Apercal
#This copies to directory defined in cfgfile
"""
prepare = apercal.prepare(cfg1)
prepare.go()

prepare = apercal.prepare(cfg2)
prepare.go()


#Then convert the data to miriad file
convert = apercal.convert(cfg1)
convert.go()

convert = apercal.convert(cfg2)
convert.go()
"""

#Now in miriad need to use uvimage to create image cube
#Want to limit number of channels
#Want to include near 9330, 20 subbands
#Subbands start at multiples of 64
#take subbands 130-149
#channels 8320, 9599

print 'starting to get data'

uvimage = lib.miriad('uvimage')
#move to directory where data is
ccal = apercal.ccal(cfg1)
ccal.director('ch', ccal.crosscaldir)
uvimage.vis = ccal.target
print uvimage.vis
uvimage.line='channel,1280,8320,1'
uvimage.view = 'amplitude'
targetname = ccal.target[:-4]
uvimage.out= targetname+'_amp.im'
uvimage.go()

print 'got uv amp image'

#write to fits file
fits = lib.miriad('fits')
fits.in_ = uvimage.out
fits.op = "xyout"
fits.out = targetname+'_amp.fits'
fits.go()

print 'got fits image'

#now do phase
uvimage.view='phase'
uvimage.out=targetname+'_phase.im'
uvimage.go()

fits.in_ = uvimage.out
fits.out = targetname+'_phase.fits'
fits.go()

#and now do the second source
ccal = apercal.ccal(cfg2)
ccal.director('ch', ccal.crosscaldir)
uvimage.vis = ccal.target
#uvimage.line='channel,1280,8320,1'
uvimage.view = 'amplitude'
targetname = ccal.target[:-4]
uvimage.out= targetname+'_amp.im'
uvimage.go()

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
