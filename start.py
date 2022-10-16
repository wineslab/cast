#!/usr/bin/env python3

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)


import constants as const
import time
import os

from utils import load_config, write_log


def main():
    """
    Main operations
    """

    config = load_config()                              # load radio.conf file
    test = config['test']
    max_nodes = test['max_nodes']
    node_id = test['node_id']

    for n in range(int(max_nodes)):
        if int(node_id) == (n+1):                       # slot time for TX
            start_time = time.time()                    # save time of start to compute elapsed time
            write_log("Starting TX with n: " + str(n+1))
            os.system(const.FILENAME_TX + " " + str(const.TX_TIME) + " " + node_id)
            elapsed_time = time.time() - start_time     # elapsed time for transmit operations
            time.sleep(const.TOTAL_TIME - round(elapsed_time, 3))     # sleep to sync with other nodes (ms precision)
            write_log("Finishing TX with elapsed time: " + str(elapsed_time))

        else:                                           # slot time for RX
            initial_sleep = const.RX_WAIT_TIME
            time.sleep(initial_sleep)                   # initial sleep
            start_time = time.time()                    # save time of start to compute elapsed time
            write_log("Starting RX with n: " + str(n))
            os.system(const.FILENAME_RX + " " + str(const.RX_TIME) + " " + str((n+1)))
            elapsed_time = time.time() - start_time     # elapsed time for receive operations
            time.sleep((const.TOTAL_TIME - initial_sleep) - round(elapsed_time, 3))     # sleep to sync with others
            write_log("Finishing RX with elapsed time: " + str(elapsed_time))

    write_log("Starting channel-estimate operations")
    os.system(const.FILENAME_CHANNEL_EST + " " + max_nodes + " " + node_id)   # Execute operations to compute pathloss
    write_log("Exiting start.py")


if __name__ == '__main__':
    main()
