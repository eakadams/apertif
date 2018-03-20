import libs.lib as lib
import apercal
import subs.readmirlog
import numpy as np
from matplotlib import pyplot as plt

#########################

def do_bp(cfgfile,inttime='30'):
    #function to do the bandpass solution, for given interval                   
    #inttime is the solution interval for bandpass, in minutes                  
    ccal=apercal.ccal(cfgfile)
    #change to working directory
    #workaround for long path names
    ccal.director('ch', ccal.crosscaldir)
    gainint=inttime
    gapint=inttime
    bpint=inttime
    mfcal = lib.miriad('mfcal')
    mfcal.vis = ccal.fluxcal
    print mfcal.vis
    #print mfcal.vis                                                            
    # Comment the next line out if you don't want to solve for delays           
    mfcal.options = 'delay'
    mfcal.stokes = 'XX'
    mfcal.interval = gainint + ',' + gapint + ',' + bpint
    mfcal.tol = 0.1 # Set the tolerance a bit lower. Otherwise mfcal takes a long time to finsh                                                                
    mfcal.go()
    print 'calibration finished'

##########################

def get_bpsols(cfgfile):
    #function to read solutions and return arrays of values and freqs           
    #now read solutions and put into array to return                            
    ccal=apercal.ccal(cfgfile)
    values,freqs = subs.readmirlog.get_bp(ccal.crosscaldir + '/' + ccal.fluxcal)
    #replace all zeros with nans before returning.                              
    values[values==0] = np.nan
    print 'read calibration solutions into numpy array'
    return values,freqs

###################

def freq_avg_bpsols(values,freqs,nchan=8):
    #function to take values and freqs and return frequency averaged arrays     
    #where nchan is how many channels to average together                       
    #best to stick to multiples of 64                                           
    if np.mod(64,nchan) != 0:
        print 'Warning, nchan does not divide evenly into a subband'
    #values has structure: antenna, frequency, solution interval                
    #freq has list of frequencies                                               
    #I want to reshape freqs and second axis of values                          
    #reshape and take mean:                                                     
    #reshape second axis into 2d array that has shape of totchan/nchan,nchan    
    avvalues = values.reshape(values.shape[0],-1, nchan,values.shape[2])
    #then take the mean:                                                        
    avmean = np.nanmean(avvalues,axis=2)
    #and do same for freq                                                       
    #can do reshape and average at once                                         
    avfreqs = np.nanmean(freqs.reshape(-1,nchan), axis=1)
    return avmean, avfreqs

#######################

def get_norm_bpsols(values,freqs,nchan=8,normscan=0):
    #first, average values as required
    if nchan > 1:
        avvalues,avfreqs = freq_avg_bpsols(values,freqs,nchan)
    else:
        avvalues,avfreqs = values, freqs
    #then do normalization
    #can normalize to any solution interval; default is first
    #check if the chose scan exists
    #can be positive or negative (reverse index)
    if abs(normscan) >= avvalues.shape[2]:
        print 'Scan number for normalization does not exist'
    else:
        div = np.dstack([avvalues[:,:,normscan]] * len(avvalues[0,0]))
        normvalues = avvalues/div
        return normvalues, avfreqs

#################

def plot_bp_per_ant(values,freqs,tnames,nchan=8,nx=3,norm=True,normscan=0,offset=0.1,ymin=0,ymax=0,xs=3,ys=3):
    #input values and freqs, then average and normalize as desired
    #need list of telescope names explicitly; this is not in data
    #how to offset solutions from each other
    #number of plots in x direction (y automatically computed)
    if len(tnames) <1:
        print 'there are no antennas in tnames!'
    if norm == True:
        plotvals,plotfreqs = get_norm_bpsols(values,freqs,nchan=nchan,normscan=normscan)        
    elif nchan > 1:
        plotvals,plotfreqs = freq_avg_bpsols(values,freqs,nchan)
    else:    
        plotvals, plotfreqs = values, freqs

    #now setup the plotting environment
    #total number of plots is
    nplots = len(tnames)
    ny = int(np.ceil(nplots/float(nx)))
    #and set up size that I will want
    #say 3 inches per plot
    xsize = nx*xs
    ysize = ny*ys
    #and I want global limits, for best comparison
    #this could potentially change
    #will have a total offset of 
    totoffset = (plotvals.shape[2]-1)*offset
    if ymin == 0:
        ymin = np.nanmin(plotvals) - offset
    if ymax == 0:
        ymax = np.nanmax(plotvals) + totoffset + offset
    xmin = np.nanmin(plotfreqs)
    xmax = np.nanmax(plotfreqs)
    
    #create figure object
    #this is what I return from program
    fig= plt.figure(figsize=(xsize,ysize))
    plt.xlim(xmin,xmax) # Limit the plot to the minimum and maximum frequencies
    plt.suptitle('Bandpass', fontsize='large')


    for a in range(len(plotvals[:])):
        plt.subplot(ny, nx, a+1)
        for sol in range(plotvals.shape[2]):
            plt.plot(plotfreqs, (plotvals[a,:,sol] + np.full(plotvals.shape[1],offset*sol)))
        plt.title(tnames[a])
        plt.xlim(xmin,xmax) # Limit the plot to the minimum and maximum frequencies
        plt.ylim(ymin,ymax)
           
    
    return fig

###################

def plot_bp_one_ant(values,freqs,antind,antname,nchan=8,norm=True,normscan=0,offset=0.1,ymin=0,ymax=0,plotsize=8):
    #input values and freqs, then average and normalize as desired
    #antind is idex value of antenna
    #antname is its name
    #could make that nicer for the user, but i'm lazy
    #how to offset solutions from each other
    #number of plots in x direction (y automatically computed)
    if norm == True:
        plotvals,plotfreqs = get_norm_bpsols(values,freqs,nchan=nchan,normscan=normscan)        
    elif nchan > 1:
        plotvals,plotfreqs = freq_avg_bpsols(values,freqs,nchan)
    else:    
        plotvals, plotfreqs = values, freqs

    
    
    #now setup the plotting environment
    xsize = plotsize
    ysize = plotsize
    #and I want global limits, for best comparison
    #this could potentially change
    #will have a total offset of 
    totoffset = (plotvals.shape[2]-1)*offset
    if ymin == 0:
        ymin = np.nanmin(plotvals) - offset
    if ymax == 0:
        ymax = np.nanmax(plotvals) + totoffset + offset
    xmin = np.nanmin(plotfreqs)
    xmax = np.nanmax(plotfreqs)
    
    #create figure object
    #this is what I return from program
    #make it as subplots initially
    #share axes for best comparison
    fig= plt.figure(figsize=(xsize,ysize))
    plt.xlim(xmin,xmax) # Limit the plot to the minimum and maximum frequencies
    plt.suptitle('Bandpass', fontsize='large')
    for sol in range(plotvals.shape[2]):
            plt.plot(plotfreqs, (plotvals[antind,:,sol] + np.full(plotvals.shape[1],offset*sol)))
    plt.title(antname)
    plt.xlim(xmin,xmax) # Limit the plot to the minimum and maximum frequencies
    plt.ylim(ymin,ymax)
    
    return fig

##################
def plot_last_bp_per_ant(values,freqs,tnames,nchan=8,nx=3,ymin=0,ymax=0,plotsize=4):
    #input values and freqs, then average and normalize as desired
    #have to normalize, to first scan, because I am plotting last scan here 
    #want to see how stable it is
    #need list of telescope names explicitly; this is not in data
    #number of plots in x direction (y automatically computed)
    if len(tnames) <1:
        print 'there are no antennas in tnames!'
    plotvals,plotfreqs = get_norm_bpsols(values,freqs,nchan=nchan,normscan=0)        

    #now setup the plotting environment
    #total number of plots is
    nplots = len(tnames)
    ny = int(np.ceil(nplots/float(nx)))
    #and set up size that I will want
    #say 3 inches per plot
    xsize = nx*plotsize
    ysize = ny*plotsize
    #and I want global limits, for best comparison
    #this could potentially change
    #will have a total offset of 
    if ymin == 0:
        ymin = np.nanmin(plotvals)
    if ymax == 0:
        ymax = np.nanmax(plotvals)
    xmin = np.nanmin(plotfreqs)
    xmax = np.nanmax(plotfreqs)
    
    #create figure object
    #this is what I return from program
    fig= plt.figure(figsize=(xsize,ysize))
    plt.xlim(xmin,xmax) # Limit the plot to the minimum and maximum frequencies
    plt.suptitle('Bandpass', fontsize='large')


    for a in range(len(plotvals[:])):
        plt.subplot(ny, nx, a+1)
        plt.plot(plotfreqs, plotvals[a,:,-1])
#        for sol in range(plotvals.shape[2]):
#            plt.plot(plotfreqs, (plotvals[a,:,sol] + np.full(plotvals.shape[1],offset*sol)))
        plt.title(tnames[a])
        plt.xlim(xmin,xmax) # Limit the plot to the minimum and maximum frequencies
        plt.ylim(ymin,ymax)
           
    
    return fig

####################

def get_data_mult_bp(scanlist,sourcename,beamnum,targetbasedir):
    #this takes a scanlist
    #assumes you are on local machine
    #takes source name
    #plus beam number
    #and targetbasedir where you want data; will put in proper Apercal substructure below
    #iterate through the scans:
    for i,scan in enumerate(scanlist):
        targetdir = targetbasedir+'_'+str(i)+'/00/raw/'
        targetfile = targetdir+sourcename+'.MS'
        sourcedir = '/data/apertif/'+str(scan)+'_'+sourcename+'_sw_'+str(beamnum)+'/'
        #format source file name based on if beam is 1 or 2 digits:
        if beamnum <=9:
            sourcefile = sourcedir+'WSRTA'+str(scan)+'_B00'+str(beamnum)+'.MS'
        if beamnum >=10:
            sourcefile = sourcedir+'WSRTA'+str(scan)+'_B0'+str(beamnum)+'.MS'
        #now do checks and start copying data
        if os.path.exists(sourcefile):
            print 'data exists for scan '+str(scan)
        #if data is there, make sure it has a place to be copied to:
            if os.path.exists(targetdir):
                pass
            else:
                os.makedirs(targetdir)
            #then copy the data over
            #first check that you haven't already copied it
            #if so, assume user knows what they're doing and remove it first and re-copy
            if os.path.exists(targetfile):
                shutil.rmtree(targetfile)
                shutil.copytree(sourcefile,targetfile)
                print 'copying data for scan '+str(scan)
            else:
                shutil.copytree(sourcefile,targetfile)
                print 'copying data for scan '+str(scan)
        else:
            #if data isn't there, print that
            print "data does not exist for scan " +str(scan)+" and cannot be copied"


#########################

def flag_mult_bp(scanlist,cfgfile,basedir,flagbadchans=True,nchannel=11008):
    #read in cfg file; 
    #but define directory explicitly, so can use for different beams
    #this means I overwrite basedir in cfg file, so that's not important
    preflag = apercal.preflag(cfgfile)
    if flagbadchans == True:
        #flag channels with ghosts and subband edges
        # Make lists of the channels which are affected
        a = range(0, nchannel, 64) # the subband edges
        b = range(1, nchannel, 64)
        c = range(63, nchannel, 64)
        d = range(16, nchannel, 64) # the two ghosts
        e = range(48, nchannel, 64)
        # Combine the channel list into one list and convert to a string
        l = a + b + c + d + e
        preflag.preflag_manualflag_channel = ';'.join(str(ch) for ch in l)
        
        #now go through the scans and flag
    for i,scan in enumerate(scanlist):
        print i,scan
        preflag.basedir = basedir+'_'+str(i)+'/'
        print preflag.basedir
        #check that data directory exists and only run preflag if it does
        #i'm going to try and run all the preflag steps in a row in a single step
        if os.path.exists(preflag.basedir):
            #do manual flags no matter what; set above if there are bad channels or not
            preflag.manualflag()
            #now I also want to do rfi flagging but I have problems with the errors
            #will try again
            """try:
                preflag.aoflagger_bandpass()
            except TypeError:
                #try catching the error thrown by this and see what happens
                pass"""
            #am skipping for now
            #will try just flagging without bandpass
            #otherwise, I could skip all together
            preflag.aoflagger_flag()
            
        else:
            #if directory doesn't exist, pass
            pass



###########################

def convert_mult_bp(scanlist,cfgfile,basedir):
    convert = apercal.convert(cfgfile)
    for i,scan in enumerate(scanlist):
        print i,scan
        convert.basedir = basedir+'_'+str(i)+'/'
        print convert.basedir
        #convert.show()
        if os.path.exists(convert.basedir):
            convert.go()

######################


def cal_mult_bp(scanlist,cfgfile,basedir,sourcename,gainint='60',gapint='60',bpint='60'):
    #now do the bandpass solutions - the point of all of this!
    #define intervals by default
    #numbers don't matter overly much - will be full solution of short scan
    #sourcename is important! Make sure it's a recognized calibrator format!!!!
    
    #read cfgfile, not sure this will actually matter here since I set basedir manually
    ccal = apercal.ccal(cfgfile)

    #set-up utilities for bandpass calibration
    mfcal = lib.miriad('mfcal')
    # Comment the next line out if you don't want to solve for delays
    mfcal.options = 'delay'
    mfcal.stokes = 'XX'
    mfcal.interval = gainint + ',' + gapint + ',' + bpint
    mfcal.tol = 0.1 # Set the tolerance a bit lower. Otherwise mfcal takes a long time to finsh
    
    #IMPORTANT! source names have beam number, need to make sure miriad canrecongize
    #these parts are global, and I do specific scans below
    puthd=lib.miriad('puthd')
    puthd.value=sourcename
    #Now iterate and 
    # Execute the bandpass calibration
    #reading into different arrays
    
    #now iterate through scans and do calibration

    for i,scan in enumerate(scanlist):
        print i,scan
        ccal.basedir = basedir+'_'+str(i)+'/'
        ccal.crosscaldir = ccal.basedir + '00/crosscal/'
        #print ccal.basedir
        #print ccal.fluxcal
        #print ccal.crosscaldir
        puthdstring = ccal.crosscaldir+sourcename+'.mir/source'
        #print puthdstring
        puthd.in_ = puthdstring #extra underscore because python has a global in
        puthd.go()
        #convert.show()
        #print ccal.crosscaldir
        if os.path.exists(ccal.crosscaldir):
            print 'doing calibration'
            mfcal.vis = ccal.crosscaldir+ccal.fluxcal
            mfcal.go()

        
############################

def get_bp_sols_mult_bp(scanlist,cfgfile,basedir):
    ccal = apercal.ccal(cfgfile)
    all_values = []
    for i,scan in enumerate(scanlist):
        print i,scan
        ccal.basedir = basedir+'_'+str(i)+'/'
        ccal.crosscaldir = ccal.basedir + '00/crosscal/'
        #print ccal.basedir
        #print ccal.fluxcal
        #print ccal.crosscaldir
        #convert.show()
        #print ccal.crosscaldir
        if os.path.exists(ccal.crosscaldir):
            #print ccal.crosscaldir  + ccal.fluxcal
            values, freqs = subs.readmirlog.get_bp(ccal.crosscaldir  + ccal.fluxcal)
            #create master array
            if len(all_values)==0:
                all_values=np.copy(values)
            else:
                all_values=np.append(all_values,values,axis=2)
                
    return all_values

############################
