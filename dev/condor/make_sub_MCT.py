import sys

basedir=str(sys.argv[1])
st=str(sys.argv[2])
len=str(sys.argv[3])
chan_list=str(sys.argv[4])
ifo=str(sys.argv[5])
outdir=str(sys.argv[6])
subname = basedir + "/condor_dag/DAC_MCT_" + st + "_" + len + ".sub"

fP=open(subname,'w')

print >> fP,"Executable = MCT_condor_exe"
print >> fP,"Universe = vanilla"
print >> fP,"Arguments = $(macrojobnumber) %s %s %s %s %s" % (st,len,chan_list,ifo,outdir)
print >> fP,"Error = log_%s_MCT/err.$(macrojobnumber)" %(st)
print >> fP,"Output = log_%s_MCT/out.$(macrojobnumber)" %(st)
print >> fP,"Log = log_%s_MCT/log.$(macrojobnumber)" %(st)
print >> fP,"Notification = never"
print >> fP,'environment = "X509_USER_CERT=/home/tjmassin/robot_cert/DAC-glitch-mon-LHO_ldas-pcdev2.ligo-wa.caltech.edu-cert.pem X509_USER_KEY=/home/tjmassin/robot_cert/robot.key.pem LIGO_DATAFIND_SERVER=10.12.0.49:80"'
print >> fP,"accounting_group = ligo.dev.o1.detchar.explore.test"
print >> fP,"Queue 1"

fP.close()


