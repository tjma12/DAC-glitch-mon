import sys

basedir=str(sys.argv[1])
st=str(sys.argv[2])
len=str(sys.argv[3])
chan_list=str(sys.argv[4])

subname = basedir + "/condor_dag/DAC_MCT_" + st + "_" + len + ".sub"

fP=open(subname,'w')

print >> fP,"Executable = DAC_condor_exe"
print >> fP,"Universe = vanilla"
print >> fP,"Arguments = $(macrojobnumber) %s %s %s" % (st,len,chan_list)
print >> fP,"Error = log_%s_DAC/err.$(macrojobnumber)" %(st)
print >> fP,"Output = log_%s_DAC/out.$(macrojobnumber)" %(st)
print >> fP,"Log = log_%s_DAC/log.$(macrojobnumber)" %(st)
print >> fP,"Notification = never"
print >> fP,'environment = "X509_USER_CERT=/home/tjmassin/robot_cert/DAC-glitch-mon-LHO_ldas-pcdev2.ligo-wa.caltech.edu-cert.pem X509_USER_KEY=/home/tjmassin/robot_cert/robot.key.pem LIGO_DATAFIND_SERVER=10.12.0.49:80"'
print >> fP,"accounting_group = ligo.dev.o1.detchar.explore.test"
print >> fP,"Queue 1"

fP.close()


