#!/bin/bash

start_time=$1
duration=$2
basedir=$3
outdir=$4
trigger_dir=$5

basedir="${outdir}/${start_time}_${duration}"

echo "Building directory structure at ${basedir}"

mkdir -p ${basedir}
mkdir -p ${basedir}/condor_dag
mkdir -p ${basedir}/condor_dag/log_${start_time}_MCT

cp find_crossings_condor.py ${basedir}/condor_dag/find_crossings_condor.py
cp 

source /home/detchar/opt/gwpysoft/etc/gwpy-user-env.sh

frame=`gw_data_find -n -o ${ifo} -t ${ifo}1_R -s ${start_time} -e ${start_time} -u file`
chan_list="all_SUS_MASTER_OUT_chans_${start_time}"

FrChannels ${frame} | grep 'SUS' | grep 'MASTER_OUT' | grep 'DQ' | cut -d ' ' -f 1 > ${basedir}/${chan_list}

echo "Wrote list of all SUS MASTER_OUT channels to file: ${chan_list}"
















python make_sub_MCT.py ${basedir} ${start_time} ${duration} ${basedir}/${chan_list} ${ifo}1 ${trigger_dir}
python make_dag_MCT.py ${start_time} ${duration} ${basedir}





