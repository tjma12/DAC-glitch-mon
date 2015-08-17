#!/usr/bin/python
#
# This code is used to find times when suspension drive signals are crossing a value of zero
# or +/- 2^16. At these times, we expect glitches from the 18-bit DACs due to a calibration
# that drifts over time.
#
# USAGE:
#
# find_crossings.py CHAN_LIST.txt START_TIME DURATION IFO
#
# There are three main functions:
#
# get_data will use GWpy frame reading to pull in data for the duration of the time segment
# calc_crossings will take a time series and calculate each time the signal crosses zero or 2^16
# write_xml will write the times returned by calc_crossings and write them to XML as SnglBurst triggers
#
# The segment query uses the dqsegdb apicalls module to directly query the segment database and returns
# segments in a dictionary
#
# Author: TJ Massinger 4/2/2015

from glue.ligolw import utils, ligolw, lsctables
from glue.lal import LIGOTimeGPS
from glue import lal,datafind
from glue import segments as seg
from gwpy.timeseries import TimeSeries
from dqsegdb import apicalls
from optparse import OptionParser
import optparse
import numpy as np
import os
import sys

def read_command_line():
    parser = OptionParser(
        usage = "%prog --start_time --duration --channel_list --channel --IFO"
    )


    parser.add_option("-s","--start_time",metavar="start_time",help="GPS start time")
    parser.add_option("-d","--duration",metavar="duration",help="duration of time to run over")
    parser.add_option("-f","--chan_file",metavar="chan_file",help="list of channels to run over")
    parser.add_option("-c","--channel",metavar="channel",help="channel to run over")
    parser.add_option("-i","--ifo",metavar="ifo",help="IFO (L1 or H1)")
    parser.add_option("-o","--output-dir",metavar="output_dir",help="Output directory for triggers")
    v = optparse.Values()
    args, others = parser.parse_args(values=v)

    if 'chan_file' in args.__dict__:
        chan_file = args.chan_file
        print 'channel list is ' + str(chan_file)
        chan_list=np.loadtxt(chan_file,dtype=str)
        channel = []
    elif 'channel' in args.__dict__:
        channel = args.channel
        print 'channel is ' + str(channel)
        chan_list=[str(channel)]
    else:
        print 'No channels provided'
        sys.exit()

    start_time = int(args.start_time)
    print 'start time is ' + str(start_time)
    duration = int(args.duration)
    print 'duration is ' + str(duration)
    ifo = str(args.ifo)
    print 'IFO is ' + str(ifo)
    outdir = str(args.output_dir)

    return chan_list,start_time,duration,ifo,outdir

# function used to coalesce result of segment query
def coalesceResultDictionary(result_dict):
    out_result_dict=result_dict
    active_seg_python_list=[seg.segment(i[0],i[1]) for i in result_dict[0]['active']]
    active_seg_list=seg.segmentlist(active_seg_python_list)
    active_seg_list.coalesce()
    out_result_dict[0]['active']=active_seg_list
    known_seg_python_list=[seg.segment(i[0],i[1]) for i in result_dict[0]['known']]
    known_seg_list=seg.segmentlist(known_seg_python_list)
    known_seg_list.coalesce()
    out_result_dict[0]['known']=known_seg_list
    return out_result_dict

def find_segments(ifo,start_time,length):
    if ifo == 'H1':
        DQFlag = 'DMT-DC_READOUT_LOCKED'
    else:
        DQFlag = 'ODC-MASTER_OBS_INTENT'
    seg_dict=apicalls.dqsegdbQueryTimes('https','dqsegdb5.phy.syr.edu',ifo,DQFlag,'1','active,known,metadata',start_time,start_time+length)
    return seg_dict

def get_data(channel,start_time,length):
    connection = datafind.GWDataFindHTTPConnection()
    cache = connection.find_frame_urls('H','H1_R',start_time,start_time + length,urltype='file')
    print 'Starting data transfer for channel: ' + str(channel)
    data = TimeSeries.read(cache,channel,start=start_time,end=start_time+length)
    print "Got data for channel: " + str(channel)
    return data

# calculate crossings for a given time series and threshold
# time series that spend time in a given window will generate triggers set at the midpoint of when it enters and leaves the window
# these start and end times will be stored in a segment list

# checking for crossing of a value is done by time shifting the data by one sample and doing a point-by-point comparison. A trigger is generated when consecutive data points straddle or land exactly on a threshold 
def calc_crossings(channel,data,start_time,length,thresh):
    trig_segs = seg.segmentlist()
    if (thresh == 15) or (thresh == 16):
        positives = data.value >= 2.**thresh
        negatives = data.value < 2.**thresh
        positives2 = data.value >= -2.**thresh
        negatives2 = data.value < -2.**thresh
        crossings = np.logical_not(np.logical_xor(positives[1:], negatives[:-1]))
        crossings2 = np.logical_not(np.logical_xor(positives2[1:], negatives2[:-1]))
        all_crossings = np.logical_xor(crossings,crossings2)
    elif thresh == 0:
        positives = data.value >= 0
        negatives = data.value < 0
        all_crossings = np.logical_not(np.logical_xor(positives[1:], negatives[:-1]))
    elif thresh == 'window':
        all_crossings = np.logical_and(data.value >= ((2.**16) - 800),data.value <= ((2.**16) + 800))
        for i in np.arange(0,len(all_crossings)):
            if all_crossings[i]:
                trig_segs |= seg.segmentlist([seg.segment(data.times[i],data.times[i]+(1./data.sample_rate.value))])
        trig_segs = trig_segs.coalesce()
    else:
        print "Threshold must be 0, 15, 16, or window"
        sys.exit()


    if thresh == 'window':
        times = []
        for entry in trig_segs:
            times.append((entry[1]+entry[0])/2.)
    else: 
        times = np.array(data.times[all_crossings])

# if times are found, write them into a sngl_burst_table XML in the directories defined below
    if len(times):
        trig_times = map(LIGOTimeGPS,map(float,times))
        freqs = np.empty(np.size(trig_times))
        freqs.fill(100)
        snrs = np.empty(np.size(trig_times))
        snrs.fill(10)
    else:
        raise ValueError 

    return trig_times,freqs,snrs

def write_xml(trig_times,freqs,snrs,channel,start_time,length,thresh,outdir):
    if len(trig_times):
        print 'number of triggers is ' + str(len(trig_times))
        print 'trigger rate is ' + str(float(len(trig_times))/length)
        if (float(len(trig_times))/length > 16):
            print 'Trigger rate too high, skipping channel'
            return
        sngl_burst_table = lsctables.New(lsctables.SnglBurstTable, ["peak_time", "peak_time_ns","peak_frequency","snr"])

        for t,f,s in zip(trig_times, freqs, snrs):
            row = sngl_burst_table.RowType()
            row.set_peak(t)
            row.peak_frequency = f
            row.snr = s
            sngl_burst_table.append(row)
    
        xmldoc = ligolw.Document()
        xmldoc.appendChild(ligolw.LIGO_LW())
        xmldoc.childNodes[0].appendChild(sngl_burst_table)
# define trigger directory
        trig_dir = (outdir  + channel[:2] + '/' + 
        channel[3:] + '_' + str(thresh)  + '_DAC/' + str(start_time)[:5] + '/')

        if not os.path.exists(trig_dir):
            os.makedirs(trig_dir)

# create filename string
        utils.write_filename(xmldoc, trig_dir + channel[:2] + "-" + channel[3:6] +
        "_" + channel[7:] + "_" + str(thresh) + "_DAC-" + str(start_time) + "-" + str(length) +
        ".xml.gz", gz=True)

        print 'wrote XML for channel: ' + str(channel)
        print 'number of triggers: ' + str(np.size(trig_times))
    else:
        print 'No triggers found for channel: ' + str(channel)  


if __name__=="__main__":
#Usage: find_crossings.py [CHANNEL LIST] [START GPS] [DURATION] 
    thresh_vec=[0,16]
    chan_list,start_time,length,ifo,outdir=read_command_line()
    getSegs=find_segments(ifo,start_time,length) 
    DQsegs=coalesceResultDictionary(getSegs)
    if not DQsegs[0]['active']:
        print 'No analysis segments found'
        sys.exit()
    for channel in chan_list:
        print 'Fetching data for channel: ' + str(channel)
        for segment in DQsegs[0]['active']:
            print 'Processing segment ' + str(segment[0]) + ' - ' + str(segment[1])
            stride = segment[1] - segment[0]
            data = get_data(channel,segment[0],stride)
            for thresh in thresh_vec:
                print 'Generating triggers for channel ' + str(channel) + ' and threshold ' + str(thresh)
                try:
                    trig_times,freqs,snrs=calc_crossings(channel,data,segment[0],stride,thresh)
                except ValueError:
                    print 'No triggers found'
                    continue
                write_xml(trig_times,freqs,snrs,channel,segment[0],stride,thresh,outdir) 
