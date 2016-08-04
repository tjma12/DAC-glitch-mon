cd ~/git/DAC-glitch-mon/dev/condor

bash build_condor_MCT.sh 1135123217 86400 /home/tjmassin/DAC_MCT_trigs/ /home/tjmassin/DAC_MCT_trigs/O1/ L DMT-ANALYSIS_READY

cd ~/DAC_MCT_trigs/1135123217_86400/condor_dag

vim DAC_MCT_1135123217_86400.sub

Put the right values into this variable in the sub file:

environment = "X509_USER_CERT=/home/tjmassin/robot_cert/DAC-glitch-mon-LHO_ldas-pcdev2.ligo-wa.caltech.edu-cert.pem X509_USER_KEY=/home/tjmassin/robot_cert/robot.key.pem LIGO_DATAFIND_SERVER=10.12.0.49:80"

Fix this:

cache = connection.find_frame_urls('H','H1_R',start_time,start_time +
length,urltype='file')

