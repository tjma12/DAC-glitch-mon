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
print >> fP,"getenv=true"
print >> fP,"Queue 1"

fP.close()


