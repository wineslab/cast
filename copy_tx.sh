#!/bin/bash

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)

# Check for input argument
if [ $# -ne 2 ];
  then
    echo "ERROR: Wrong number of arguments. Please call as: sh copy_tx.sh source_srn dest_srn, ex: ./copy_tx.sh 003 001"
    exit 1
fi

source_srn=${1}
dest_srn=${2}
password='sound123'

# sshpass -p ${password} scp neu-test-team-1-"${source_srn}":/root/single_api/ga128_bpsk_sps4_full.iq ga128_tx_tmp.iq
# sshpass -p ${password} scp ga128_tx_tmp.iq neu-test-team-1-"${dest_srn}":/root/single_api/ga128_bpsk_sps4_full.iq
# rm ga128_tx_tmp.iq
# sshpass -p ${password} scp neu-test-team-1-"${source_srn}":/root/single_api/ga128_bpsk_sps4_full.iq ../data/glfsr_bpsk_tx.iq
sshpass -p ${password} scp neu-test-team-1-"${dest_srn}":/root/single_api/ga128_bpsk_sps4_rrc_usrpSource.iq ../data/glfsr_bpsk_rx.iq
# sshpass -p ${password} scp neu-test-team-1-"${dest_srn}":/root/single_api/*.iq ../data/

echo "Done!"