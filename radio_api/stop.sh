#!/usr/bin/env bash

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)

# v0.5.0
# stop.sh - This script is called by the Colosseum to tell the radio the match is ending.
# No input is accepted.
# STDOUT and STDERR may be logged, but the exit status is always checked.
# The script should return 0 to signify successful execution.

# Check if there is an input argument
case $# in
     0)   # Zero inputs
          echo "[`date`] Run stop.sh" >> ../logs/run.log

          # Copy iq files to /logs/
          echo "[`date`] Moving iq files to logs" >> ../logs/run.log
          mv ./*.iq /logs/

          # Copy journalctl to /logs/
          echo "[`date`] Exporting journalctl to logs" >> ../logs/run.log
          journalctl --since="1 hours ago" > ../logs/journalctl.log

          # Copy all logs to /logs/
          echo "[`date`] Exporting all logs and files to logs" >> ../logs/run.log
          mv ../logs/* /logs/

          # Exiting
          echo "[`date`] Exiting stop.sh successfully" >> ../logs/run.log
          exit 0    # Exit successfully
          ;;

     *)   # One or more input arguments
          exit 64   # Exit with an error
          ;;
esac
