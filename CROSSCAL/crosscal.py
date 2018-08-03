#python "module" for tests and inventories related to
#confirming the ability and calculating appropriate scaling
#for transfering solutions from central beam to other beams

#define a class that is used for specifying the scans to be investigated

class ScanSpecification(object):
    def __init__(self):
        #set all attributes to empty strings to initialize
        #that way I can check for what is set later
        self.startdate=''
        self.enddate=''
        self.beam=''
        self.startscan=''
        self.endscan=''
        self.nscan=''
    def setstartdate(self,sd):
        #want to do some checking that startdate is in the right format
        #turn into a string
        sdstr=str(sd)
        if len(sdstr) != 8:
            print "Startdate must be  of format 'YYYYMMDD'"
        elif sdstr[0:3] != '201':
            print "Startdate must be a string of format 'YYYYMMDD', starting from 2010"
        else:
            self.startdate=sdstr
    def setenddate(self,ed):
        edstr=str(ed)
        if len(edstr) != 8:
            print "Enddate must be of format 'YYYYMMDD'"
        elif edstr[0:3] != '201':
            print "Enddate must be of format 'YYYYMMDD', starting from 2010"
        else:
            self.enddate = edstr
    def setbeam(self,bm):
        bmstr=str(bm)
        if len(bmstr) == 1:
            newbmstr = '{0}{1}'.format(0,bmstr)
            self.beam = newbmstr
        elif float(bmstr) != int(float(bmstr)):
            print "Beam must be an integer"
        elif len(bmstr) != 2:
            print "Beam must be of format 'NN'"
        elif float(bmstr) >39 or float(bmstr) <0:
            print "Beam must be an integer between 0 and 39"
        else:
            self.beam = bmstr
    def setstartscan(self,stsc):
        scstr = str(stsc)
        #Assume format is YYMMDDXXX 
        #this is valid from Feb 2018
        #Jan and earlier had only two scan numbers
        #I think just focusing on that date range (at least to start) is okay
        if len(scstr) != 9:
            print "Start scan must be of format 'YYMMDDXXX'"
        elif scstr[0:2] != '18': #can add more years later if need be
            print "Start scan must be of format 'YYMMDDXXX', with a year of 18"
        else:
            self.startscan = scstr
    def setendscan(self,edsc):
        scstr = str(edsc)
        #Assume format is YYMMDDXXX 
        #this is valid from Feb 2018
        #Jan and earlier had only two scan numbers
        #I think just focusing on that date range (at least to start) is okay
        if len(scstr) != 9:
            print "Start scan must be of format 'YYMMDDXXX'"
        elif scstr[0:2] != '18': #can add more years later if need be
            print "Start scan must be of format 'YYMMDDXXX', with a year of 18"
        else:
            self.endscan = scstr    
    def setnscan(self,ns):
        nsstr = str(ns)
        #want to check if it is a number
        #but doesn't work how I expect
        try:
            float(nsstr)
            if float(nsstr) == int(float(nsstr)):
                self.nscan = nsstr
            else:
                new_ns = str(int(float(nsstr)))
                self.nscan = new_ns
        except ValueError:
            print 'nscan must be a number'

            
"""

scandict = {'startdate':"", 'enddate':"",'beam':"",
            'startscan':"",'endscan':"",'nscan':""}


        
def add_end_date(scandict,ed):
    #add enddate
    if type(sd) is str:
        #good, check length
        if len(sd) != 8:
            print "Enddate must be a string of format 'YYYYMMDD'"
        elif sd[0:2] != '201':
            print "Enddate must be a string of format 'YYYYMMDD'"
        else:
            scandict["enddate"] = ed
    else:
        print "Enddate must be a string of format 'YYYYMMDD'"
"""

"""    
def add_beam():
    #add beam
    
def add_start_scan():
    #adds tart scan
    
def add_end_scan():
    #add last scan
    
def add_n_scan():
    #add number of scans


def get_scan_list():
    #pass a dictionary with keywords that define what mode I will operate in
    #all keywords in dictionary, but not all filled in
    #I want to have two modes of operation:
    #(1) Give a start scan and end (or total number) to get a series of beams
    #(2) Give a date range and beam to give all scans 
    #this function will generate a list of scans I care about
    #It will be a full directory path list, and will include the
    #appropriate beam where the source is
    #Or, I may need the beam list separately - works better w/ Apercal
    #Would like to exclude long scans - read MS
    
    return scan_list,beam_list,time_list
    
def copy_scans():
    #This will use the output of get_scan_list 
    #to copy the data to where I want it to be
    #do manually. start w/ happili, expand to ALTA later

def flag_scans():
    #This will use output of get_scan_list
    #plus apercal.preflag() to flag the data
    #Note that this likely will not work until the preflag error is fixed
    #So I probably won't use it at first    

def convert_scans():
    #Convert to miriad format
    
def calibrate_scans():
    #This iwll use scan_list,beam_list from get_scan_list
    #plus apercal.ccal to calibrate the data
    #HAVE TO CHANGE SOURCE NAME!
    


def get_time_sequence_for_beam():
    #Get a series of scans for single beam
    
def compare_scan_solution_amp():
    #This will compare scan solutions to reference (given) for amplitude
    #will return an array that is amp solution for each scan divided by reference
    #these scans can be separated by time or beam
    
def compare_scan_solution_phase():
    #This will compare scan solutions to reference (given) for phase
    #will return an array that is phase solution for each scan divided by reference
    
def compare_scan_solution_bp_phase():
    #This will compare scan BP solutions to reference (given) for phase
    #will return a 2-D array (freq, scan) 
    #that is BP phase solution for each scan divided by reference 
        
def compare_scan_solution_bp_amp():
    #This will compare scan BP solutions to reference (given) for amp
    #will return a 2-D array (freq, scan)
    #that is BP amp solution for each scan divided by reference
    
def plot_compare_beam_amp():
    #this will generate plots that show comparison in amplitude solution
    #between different scans, labelled/plotted as function of beam
    
def plot_compare_beam_phase():
    #this will generate plots that show comparison in phase solution
    #between different scans, labelled/plotted as function of beam
    
def plot_compare_beam_bp_amp():
    #this will generate plots that show comparison in BP amplitude solution
    #between different scans, labelled/plotted as function of beam
    
def plot_compare_beam_bp_phase():
    #this will generate plots that show comparison in BP phase solution
    #between different scans, labelled/plotted as function of beam
    
def plot_compare_time_amp():
    #this will generate plots that show comparison in amplitude solution
    #between different scans, labelled/plotted as function of time
    
def plot_compare_time_phase():
    #this will generate plots that show comparison in phase solution
    #between different scans, labelled/plotted as function of time
    
def plot_compare_time_bp_amp():
    #this will generate plots that show comparison in BP amplitude solution
    #between different scans, labelled/plotted as function of time
    
def plot_compare_time_bp_phase():
    #this will generate plots that show comparison in BP phase solution
    #between different scans, labelled/plotted as function of time
    
"""
        