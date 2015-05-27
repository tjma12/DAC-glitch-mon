#!/bin/bash

source /home/detchar/opt/gwpysoft/etc/gwpy-user-env.sh

# This script should be run every 8 hours by cron
# To run just after 00:00, 08:00, and 16:00 UTC, we look at the system time
# UTC:  8:20  16:20  0:20
# PST:  1:20  9:20  17:20

DATE=`date +%F`
HOUR=`date +%H`

# run at 1:20 PST to cover 0:00 - 8:00 UTC
# run at 9:20 PST to cover 8:00 - 16:00 UTC
# run at 17:20 PST to cover 16:00 - 0:00 UTC

if [ $HOUR -eq 1 ]
then
    start_time="$DATE 00:00:00"
elif [ $HOUR -eq 9 ]
then
    start_time="$DATE 08:00:00"
elif [ $HOUR -eq 17 ]
then
    start_time="$DATE 16:00:00"
fi

start_time_gps=`lalapps_tconvert $start_time`
duration=28800

#echo ${DATE}
#echo ${start_time}
#echo ${duration}


# Grab a list of all SUS MASTER_OUT channels by grabbing one frame and filtering with grep
# find the useful channels
#frame=`gw_data_find -n -o H -t H1_R -s ${start_time} -e ${start_time} | head -n 1`

# search them for SUS drive signals
chan_list="/home/tjmassin/DAC_crossing_code/DAC_scripts/SUS_drive_signals_1112054416.txt"
#FrChannels ${frame} | grep 'SUS' | grep 'MASTER_OUT' | grep 'DQ' | cut -d ' ' -f 1 > ${chan_list}

python /home/tjmassin/DAC_crossing_code/DAC_scripts/find_crossings.py ${chan_list} ${start_time_gps} ${duration} H1

