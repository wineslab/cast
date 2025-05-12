#!/usr/bin/env bash

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)

# cast_rx.sh - This is the main file that allows to start the receiver and sound a scenario in Colosseum.
# This file will guide the user on defining the required parameters to perform the sounding of CaST.
# The default Rx node will be the current one where the script is executed.

echo "Starting receiver CaST sounding..."


### Sounding parameters

## Get scenario ID
while true; do
  read -p "What is the scenario ID to sound?: " -r

  if [[ $REPLY =~ ^([0-9]{4,5})$ ]]   # Scenario id valid
  then
    SCENARIO_ID=$REPLY
    break
  fi

  echo 'Scenario ID not valid. It must contain 4 or 5 digits (e.g. 1009).'
done


## Get scenario frequency
while true; do
  read -p "What is the scenario frequency in Hz to sound?: " -r

  if [[ $REPLY =~ ^([1-9][0-9]{6,9})$ ]]   # Scenario id valid
  then
    SCENARIO_FREQ=$REPLY
    break
  fi

  echo 'Scenario frequency not valid. It must contain between 7 and 10 digits (e.g. 1000000000).'
done


## Get total number of scenario nodes
while true; do
  read -p "What is the total number of nodes in the scenario?: " -r

  if [[ $REPLY =~ ^([1-9][0-9]{0,1})$ ]]   # Scenario nodes number valid [1-99]
  then
    SCENARIO_NODES=$REPLY
    break
  fi

  echo 'Number of nodes not valid. It must contain 1 or 2 digits (e.g. 10).'
done

## Get Rx node id
RX_ID=$(ifconfig col0 | grep -Eo '(172.30.[0-9]+.[0-9]+)' | awk -v s=100 '{print substr($1,length($1)-2)-s }')
printf 'The current node will be used as Rx: %d\n' "$RX_ID"

## Get Tx node id
while true; do
  read -p "What is the SRN node ID of the reservation acting as the tx (e.g. 3)?: " -r

  if [[ $REPLY =~ ^([1-9][0-9]{0,2})$ ]]   # Tx node id valid
  then
    TX_ID=$REPLY
    break
  fi

  echo 'Tx SRN ID not valid. It must contain 3 digits (e.g. 12).'
done

## Ensure the tx node is running
while true; do
  read -p "Is the tx node running with the same frequency (y/n)?: " -r

  if [[ $REPLY =~ ^(y|Y)(es)?$ ]]   # Y y Yes yes
  then
    break
  fi

  echo 'Start the tx node by running in its terminal window: ./run_tx_sounding.sh'
done

## Get sounding duration
while true; do
  read -p "What is the desired sounding duration in seconds?: " -r

  if [[ $REPLY =~ ^([1-9][0-9]{0,2})$ ]]   # Sounding duration should be between [1-999]
  then
    SOUNDING_DURATION=$(echo "$REPLY" | awk '{print $1 + 0}' )
    break
  fi

  echo 'Sounding duration not valid. It must be between [1-999] seconds.'
done

## Get sounding link
while true; do
  read -p "What is the scenario link tx-rx to sound (e.g. 1-2)?: " -r

  if [[ $REPLY =~ ^([1-9]{1,2}-[0-9]{1,2})$ ]]   # Sounding link [1-2]
  then
    SOUNDING_LINK=$REPLY
    IFS=- read -r SOUNDING_TX_ID SOUNDING_RX_ID <<< "$SOUNDING_LINK"   # Split tx and rx
    break
  fi

  echo 'Sounding link not valid. It must be in the format: tx-rx (e.g. tx 1 and rx 4 is: 1-4).'
done

## Get scenario offset [TO-DO]


## Print configuration values
echo '
########## CONFIGURATION VALUES ##########
SCENARIO ID: '"$SCENARIO_ID"'
SCENARIO FREQUENCY: '"$SCENARIO_FREQ"' Hz
SCENARIO NODES: '"$SCENARIO_NODES"'
TX NODE ID: '"$TX_ID"'
RX NODE ID: '"$RX_ID"'
SOUNDING DURATION: '"$SOUNDING_DURATION"' seconds
SOUNDING LINK: '"$SOUNDING_LINK"'
##########################################
'

## Export configuration values [TO-DO]


echo 'Sounding configuration completed.'


### Sounding operations

echo 'Starting sounding operations...'

## Flash fpga
echo 'Flashing FPGA.'
colosseumcli usrp flash -f usrp_x310_fpga_HG_c36.bit || { echo 'FPGA flash failed.'; exit 1; }

SECONDS=0  # Bash builtin timer
until colosseumcli usrp info | grep -q "'status': 'IDLE'"; do
    (( SECONDS > 120 )) && { echo 'FPGA flash failed.'; exit 1; }
    sleep 1
done

echo 'FPGA flash completed.'

## Set scenario radio map

echo 'Setting scenario radio map.'
# Remove extra 0s before number
TX_ID_SCEN=$(echo "$TX_ID" | awk '{print $1 + 0}' )
RX_ID_SCEN=$(echo "$RX_ID" | awk '{print $1 + 0}' )

# Remove previous radio map file
rm -f radio_api/radio_map.json

# Define empty json variable
SCEN_JSON='{}'

# Populate json variable with all none values
for ((i=1;i<=SCENARIO_NODES;i++)); do
  SCEN_JSON="$(echo "$SCEN_JSON" | jq '. + {"Node '"$i"'": "None"}')"
done

# Set tx and rx nodes in the radio map variable
SCEN_JSON="$(echo "$SCEN_JSON" | jq '. + {"Node '"$SOUNDING_TX_ID"'":{"SRN":'"$TX_ID_SCEN"',"RadioA":1,"RadioB":2}}')"
SCEN_JSON="$(echo "$SCEN_JSON" | jq '. + {"Node '"$SOUNDING_RX_ID"'":{"SRN":'"$RX_ID_SCEN"',"RadioA":1,"RadioB":2}}')"

# Export variable into a json file
echo "$SCEN_JSON" >> radio_api/radio_map.json


## Create results folder
echo 'Creating results folder.'
mkdir -p /root/results/raw_data


## Stop possible running scenario
echo 'Stopping previous running scenario.'
colosseumcli rf stop


## Start scenario
printf 'Starting scenario %d.\n' "$SCENARIO_ID"
colosseumcli rf start "$SCENARIO_ID" -c -m radio_api/radio_map.json


## Wait to sync for scenario time
echo 'Waiting to sync.'
sleep 15


## Start rx

echo 'Starting rx.'
# Calling parameters: ./rx.py tx_time frequency gain file_sink_ext
./radio_api/rx.py "$SOUNDING_DURATION" "$SCENARIO_FREQ" 15 0


## Perform sounding operations

echo 'Performing sounding operations.'
# Calling parameters: ./channel-estimate.py 0
# If the first argument is 0, it will take the default rx file from this interactive sounding
./radio_api/channel-estimate.py 0 "$SCENARIO_ID" "$SOUNDING_LINK"

echo 'CaST sounding completed.'
