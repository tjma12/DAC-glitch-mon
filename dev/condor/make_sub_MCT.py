import sys
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--basedir', type=str, required=True,
        help='Build directory for condor logging')
parser.add_argument('--start-time-gps', type=str, required=True,
        help='Start GPS time')
parser.add_argument('--duration', type=str, required=True,
        help='Duration over which to run')
parser.add_argument('--chan-list', type=str, required=True,
        help='Channel list')
parser.add_argument('--ifo', type=str, required=True,
        help='IFO, L1 or H1')
parser.add_argument('--trigger-dir', type=str, required=True,
        help='Directory to store output triggers')
parser.add_argument('--science-flag', type=str, required=True,
        help='Data quality flag to define science time')
args = parser.parse_args()

subname = args.basedir + "/condor_dag/DAC_MCT_" + args.start_time_gps + "_" + args.duration + ".sub"

fP=open(subname,'w')

print >> fP,"Executable = MCT_condor_exe"
print >> fP,"Universe = vanilla"
print >> fP,"Arguments = $(macrojobnumber) %s %s %s %s %s %s" % (args.start_time_gps,args.duration,
        args.chan_list,args.ifo,args.trigger_dir,args.science_flag)
print >> fP,"Error = log_%s_MCT/err.$(macrojobnumber)" %(args.start_time_gps)
print >> fP,"Output = log_%s_MCT/out.$(macrojobnumber)" %(args.start_time_gps)
print >> fP,"Log = log_%s_MCT/log.$(macrojobnumber)" %(args.start_time_gps)
print >> fP,"Notification = never"
print >> fP,'environment = "X509_USER_CERT=/home/tjmassin/robot_cert/DAC-glitch-mon-LHO_ldas-pcdev2.ligo-wa.caltech.edu-cert.pem X509_USER_KEY=/home/tjmassin/robot_cert/robot.key.pem LIGO_DATAFIND_SERVER=10.12.0.49:80"'
print >> fP,"accounting_group = ligo.dev.o1.detchar.explore.test"
print >> fP,"Queue 1"

fP.close()


