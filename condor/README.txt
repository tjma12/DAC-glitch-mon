build_condor_MCT.sh builds the run directory and the condor DAG/SUB files at the indicated directory. 

Args:

build_condor_MCT.sh [gps start] [duration] [run directory] [trigger save directory] [site] [science flag]

Example call: 

bash build_condor_MCT.sh 1137196817 86400 /home/tjmassin/DAC-MCT-RUNS/ /home/tjmassin/DAC_MCT_trigs/O1/ L DMT-ANALYSIS_READY

cd /home/tjmassin/DAC-MCT-RUNS/1137196817_86400/condor_dag/

condor_submit_dag DAC_MCT_1137196817_86400.dag

