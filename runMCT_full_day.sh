#!/bin/bash

source /home/detchar/opt/gwpysoft/etc/gwpy-user-env.sh

DATE=`date +%F`
start_time=`lalapps_tconvert ${DATE}`
duration=86400

#echo ${DATE}
#echo ${start_time}
#echo ${duration}


# Grab a list of all SUS MASTER_OUT channels by grabbing one frame and filtering with grep
# find the useful channels
frame=`gw_data_find -n -o H -t H1_R -s ${start_time} -e ${start_time} | head -n 1`

# search them for SUS drive signals
chan_list="SUS_drive_signals_${start_time}.txt"
FrChannels ${frame} | grep 'SUS' | grep 'MASTER_OUT' | grep 'DQ' | cut -d ' ' -f 1 > ${chan_list}

python find_crossings.py ${chan_list} ${start_time} ${duration} H1

