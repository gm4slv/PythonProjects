"""
GM4SLV Icom CiV Command Configuration

    Copyright (C) 2015  John Pumford-Green

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# header
preamble = "\xfe"
controller = "\xe0"

# commands/requests
set_freq_cmd = "\x05"
set_mode_cmd = "\x06"
get_freq_cmd = "\x03"
get_mode_cmd = "\x04"
get_smeter_cmd = "\x15\x02"
get_swr_cmd = "\x15\x12"
digi_off_cmd = "\x1a\x04\x00\x00"
set_mod_a_cmd = "\x1a\x03\x23\x01"
set_mod_am_cmd = "\x1a\x03\x23\x02"

set_vfo_mode = "\x07"

set_pre_cmd = "\x16\x02"

set_pre_off = "\x00"
set_pre_on = "\x01"

set_att_cmd = "\x11"
set_att_on = "\x20"
set_att_off = "\x00"

ptt_on_cmd = "\x1c\x00\x01"
ptt_off_cmd = "\x1c\x00\x00"

pwr_cmd = "\x14\x0a"

dspnr_on_cmd = "\x16\x40\x01"
dspnr_off_cmd = "\x16\x40\x00"

dspanf_on_cmd = "\x16\x41\x01"
dspanf_off_cmd = "\x16\x41\x00"

nb_on_cmd = "\x16\x22\x01"
nb_off_cmd = "\x16\x22\x00"

comp_on_cmd = "\x16\x44\x01"
dial_lock_on_cmd = "\x16\x50\x01"
dial_lock_off_cmd = "\x16\x50\x00"
backlight_off_cmd = "\x1a\x03\x11\x00"
backlight_on_cmd = "\x1a\x03\x11\x01"

filter_wide_cmd = "\x1a\x02\x40"
filter_normal_cmd = "\x1a\x02\x32"
filter_narrow_cmd = "\x1a\x02\x20"

# end of message
eom = "\xfd"

# controller responses
ack = "\xfb"
nak = "\xfa"

# a/n/cal values for Icom Radios - used to instantiate an Icom object
# example : r1 = Icom(n1,a1,cal1)
# a = CiV hex address of required Icom radio
# n = model number/name
# cal = s-meter calibration values (model specific - should be determined by measurement) 
#
a1 = "\x76"
n1 = "IC-7200"
cal1 = ( 25, 1, 36, 47, 31, 18, 34, 35 )

