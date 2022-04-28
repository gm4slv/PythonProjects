# header
preamble = "\xfe"
controller = "\xe0"

# commands/requests
set_freq_cmd = "\x05"
set_mode_cmd = "\x06"
get_freq_cmd = "\x03"
get_mode_cmd = "\x04"
get_smeter_cmd = "\x15" + "\x02"
get_swr_cmd = "\x15" + "\x12"
get_pwrmtr_cmd = "\x15" + "\x11"

digi_off_cmd = "\x1a" + "\x04" + "\x00" + "\x00"
digi_on_cmd = "\x1a" + "\x04" + "\x01" + "\x03"
get_dig_cmd = "\x1a" + "\x04"

set_pre_cmd = "\x16" + "\x02"

set_pre_off = "\x00"
set_pre_on = "\x01"

set_att_cmd = "\x11"
set_att_on = "\x20"
set_att_off = "\x00"

ptt_on_cmd = "\x1c" + "\x00" + "\x01"
ptt_off_cmd = "\x1c" + "\x00" + "\x00"

pwr_cmd = "\x14" + "\x0a"

bw_cmd = "\x1a" + "\x02"

set_nb_cmd = "\x16" + "\x22"
set_nb_on = "\x01"
set_nb_off = "\x00"

set_nr_cmd = "\x16" + "\x40"
set_nr_on = "\x01"
set_nr_off = "\x00"
nr_level_cmd = "\x14" + "\x06"

set_anf_cmd = "\x16" + "\x41"
set_anf_on = "\x01"
set_anf_off = "\x00"


# end of message
eom = "\xfd"

# controller responses
ack = "\xfb"
nak = "\xfa"

a1 = "\x76"
n1 = "IC-7200"
cal1 = ( 25, 1, 36, 47, 31, 18, 34, 35 )
radio_address = "\x76"
#cal = ( 25, 1, 36, 47, 31, 18, 34, 35 )
