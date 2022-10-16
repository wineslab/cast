#!/usr/bin/env bash

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)

# v0.5.0
# start.sh - This script is called by the Colosseum to tell the radio the match is starting.
# No input is accepted.
# STDOUT and STDERR may be logged, but the exit status is always checked.
# The script should return 0 to signify successful execution.

# Check if there is an input argument for radio configuration
case $# in
     0)   #zero inputs
          echo "[`date`] Starting start.sh" >> /logs/run.log
          echo "[`date`] Setting UHD_RFNOC_DIR environment variable" >> /logs/run.log
          export UHD_RFNOC_DIR=/usr/share/uhd/3.15.0/rfnoc/
          echo "[`date`] Flashing fpga" >> /logs/run.log
          /root/flash_fpga_x310.sh    # flash fpga
          # apt install gnuradio gir1.2-gtk-3.0     # install gnuradio
          echo "[`date`] Starting start.py" >> /logs/run.log
          python3 /root/radio_api/start.py
          echo "[`date`] Exiting start.sh successfully" >> /logs/run.log
          exit 0                # Exit successfully
          ;;

     *)   # More than zero input argument
          echo "Exiting start.sh with an error" >> /logs/run.log
          exit 64               # Exit with an error
          ;;
esac
