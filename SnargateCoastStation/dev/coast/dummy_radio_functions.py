# Dummy radio functions....

def set_mode(mode):
    
    
    return "Set Mode Success"
    

def set_dial_lock():
    
    return 

# we always need to set "DIGI" mode on the IC-7200 to ensure the internal USB soundcard is used as the
# modulation source.
def set_digi():
    
    
    return 
            
# get current dial frequency - only used in the Server "Watchdog" function to detect
# a radio failure - if we can't get the frequency then the radio is not available.
def get_freq():
   
    freq = 12345.67
    return "%.3f" % freq

# set new dial frequency - the frequency supplied in kHz is 1.7kHz below the nominal 
# DSC centre frequency
def set_freq(freq):
    
    
    return "Set Freq success"
  
    
        


# Turn Icom TX PTT on - the IC7200 has CiV controlled PTT which simplifies the PTT operation
# For Coast Station : we set mode to "usb" and set the radio to "digi" on each PTT_ON - to 
# ensure consistent operation, even if someone has changed settings manually on the radio
def ptt_on():


    return

# Turn Icom TX PTT off    
def ptt_off():
    
   
    return
    
    
