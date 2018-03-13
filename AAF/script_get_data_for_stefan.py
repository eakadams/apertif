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
cfg1 = '180216005.cfg'
cfg2 = '180302009.cfg'


#Prepare data using Apercal
#This copies to directory defined in cfgfile




#Need Galactic HI channels
#These are: 
