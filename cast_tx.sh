#!/usr/bin/env bash

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)

# cast_tx.sh - This is the file that allows to run the CaST transmitter node to sound a scenario in Colosseum.
# This file is ready-to-use and can be simply calling by running in the reservation node terminal that should
# act as a transmitter node: ./run_tx_sounding.sh

echo "Starting transmitter CaST sounding..."


### Sounding parameters

## Get scenario frequency
while true; do
  read -p "What is the scenario frequency in Hz to sound (should be the same as the rx node)?: " -r

  if [[ $REPLY =~ ^([1-9][0-9]{6,9})$ ]]   # Scenario id valid
  then
    SCENARIO_FREQ=$REPLY
    break
  fi

  echo 'Scenario frequency not valid. It must contain between 7 and 10 digits (e.g. 1000000000).'
done


### Start tx node

## Flash fpga
echo 'Flashing FPGA.'
colosseumcli usrp flash -f usrp_x310_fpga_HG.bit || { echo 'FPGA flash failed.'; exit 1; }

SECONDS=0  # Bash builtin timer
until colosseumcli usrp info | grep -q "'status': 'IDLE'"; do
    (( SECONDS > 120 )) && { echo 'FPGA flash failed.'; exit 1; }
    sleep 1
done

echo 'FPGA flash completed.'


## Start tx

# Calling parameters: ./tx.py tx_time frequency gain
# If the tx_time is 0, it will run indefinitely
./radio_api/tx.py 0 "$SCENARIO_FREQ" 15
