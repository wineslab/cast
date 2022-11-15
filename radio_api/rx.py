#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)
#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Channel Sounding Rx
# GNU Radio version: 3.8.2.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time

from utils import write_log


class rx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Rx")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10e6
        self.num_disp_points = num_disp_points = 2048
        self.freq = freq = float(sys.argv[2])

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(('', '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(float(sys.argv[3]), 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/root/results/raw_data/rx_file_sink_' + str(sys.argv[4]) + '.iq', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_file_sink_0_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_num_disp_points(self):
        return self.num_disp_points

    def set_num_disp_points(self, num_disp_points):
        self.num_disp_points = num_disp_points

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)


def main(top_block_cls=rx, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    # main()
    write_log("GNU Radio starting rx")
    tb = rx()
    tb.start()
    # tb.show()
    # The flowgraph is now running independently
    if sys.argv[1] == "0":    # Interactive reservation
        try:
            input('Press Enter to quit: ')
        except EOFError:
            pass
    else:                   # Batch reservation
        time.sleep(float(sys.argv[1]))      # Run for Y seconds
    tb.stop()
    tb.wait()                           # Good practice on putting the wait in case to restart
    write_log("GNU Radio ending rx")
