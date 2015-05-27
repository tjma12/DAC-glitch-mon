import sys

st = str(sys.argv[2])
len = str(sys.argv[3])
basedir=str(sys.argv[4])

dagname = basedir + "/condor_dag/DAC_MCT_" + st + "_" + len + ".dag"
subname = "DAC_MCT_" + st + "_" + len + ".sub"

fP = open(dagname,'w')

job_number = 0
for i in range(int(sys.argv[1])):
  print >> fP,'JOB %d %s\nRETRY %d 2\nVARS %d macrojobnumber="%d"' %(job_number,subname,job_number,job_number,job_number)
  job_number += 1

fP.close()
