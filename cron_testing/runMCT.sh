#!/bin/bash
#
# This script is a wrapper around a python script used to search for DAC zero and
# +/- 2^16 crossings in LIGO 18-bit DACs.
#
# USAGE: ./runMCT.sh [start_gps] [duration] [IFO]
#
# The default thresholds of interest set in the python script are zero and +/- 2^16.
#
# This script will automatically generate a list of SUS digital drive signals from
# raw frames given an input GPS time and pipe that list of channels into the python
# script.

source /home/detchar/opt/gwpysoft/etc/gwpy-user-env.sh

#DATE=`date +%F`
start_time=$1
duration=$2
ifo=$3

#echo ${DATE}
#echo ${start_time}
#echo ${duration}


# Grab a list of all SUS MASTER_OUT channels by grabbing one frame and piping the 
# the channel list into grep

frame=`gw_data_find -n -o ${ifo} -t ${ifo}1_R -s ${start_time} -e ${start_time} | head -n 1`

chan_list="SUS_drive_signals_${start_time}.txt"
FrChannels ${frame} | grep 'SUS' | grep 'MASTER_OUT' | grep 'DQ' | cut -d ' ' -f 1 > ${chan_list}

# execute python script using input parameters of bash script and channel list

python find_crossings.py ${chan_list} ${start_time} ${duration} ${ifo}1

