#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)
#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Channel Sounding Mix of Tx and Rx
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


class txrx(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Tx-Rx")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 10e6
        self.glfsr = glfsr = (1,-1,1,1,-1,-1,-1,1,1,1,1,-1,1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,-1,-1,1,-1,-1,-1,-1,1,-1,1,-1,-1,1,1,1,1,1,-1,1,-1,1,-1,1,-1,1,1,1,-1,-1,-1,-1,-1,1,1,-1,-1,-1,1,-1,1,-1,1,1,-1,-1,1,1,-1,-1,1,-1,1,1,1,1,1,1,-1,1,1,1,1,-1,-1,1,1,-1,1,1,1,-1,1,1,1,-1,-1,1,-1,1,-1,1,-1,-1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,1,1,-1,-1,1,1,1,-1,-1,1,1,1,1,-1,-1,-1,1,1,-1,1,1,-1,-1,-1,-1,1,-1,-1,-1,1,-1,1,1,1,-1,1,-1,1,1,1,1,-1,1,1,-1,1,1,1,1,1,-1,-1,-1,-1,1,1,-1,1,-1,-1,1,1,-1,1,-1,1,1,-1,1,1,-1,1,-1,1,-1,-1,-1,-1,-1,1,-1,-1,1,1,1,-1,1,1,-1,-1,1,-1,-1,1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,1,-1,-1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1)
        self.full_signal_len = full_signal_len = 255
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
        self.uhd_usrp_source_0.set_subdev_spec('A:0', 0)
        self.uhd_usrp_source_0.set_time_source('external', 0)
        self.uhd_usrp_source_0.set_clock_source('external', 0)
        self.uhd_usrp_source_0.set_center_freq(freq, 0)
        self.uhd_usrp_source_0.set_gain(float(sys.argv[4]), 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_unknown_pps(uhd.time_spec())
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
            ",".join(('', '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0_0.set_subdev_spec('B:0', 0)
        self.uhd_usrp_sink_0_0.set_time_source('external', 0)
        self.uhd_usrp_sink_0_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0_0.set_gain(float(sys.argv[3]), 0)
        self.uhd_usrp_sink_0_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_0.set_time_unknown_pps(uhd.time_spec())
        self.blocks_vector_source_x_1 = blocks.vector_source_f(glfsr, True, 1, [])
        self.blocks_null_source_1 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_gr_complex*1, '/root/results/raw_data/rx_file_sink_' + str(sys.argv[5]) + '.iq', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.blocks_null_source_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_vector_source_x_1, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_file_sink_0_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_glfsr(self):
        return self.glfsr

    def set_glfsr(self, glfsr):
        self.glfsr = glfsr
        self.blocks_vector_source_x_1.set_data(self.glfsr, [])

    def get_full_signal_len(self):
        return self.full_signal_len

    def set_full_signal_len(self, full_signal_len):
        self.full_signal_len = full_signal_len

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0_0.set_center_freq(self.freq, 0)
        self.uhd_usrp_source_0.set_center_freq(self.freq, 0)





def main(top_block_cls=txrx, options=None):
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
    write_log("GNU Radio starting mix-tx-rx")
    tb = txrx()
    tb.start()
    # tb.show()
    # The flowgraph is now running independently
    if sys.argv[1] == "0":  # Interactive reservation
        try:
            input('Press Enter to quit: ')
        except EOFError:
            pass
    else:  # Batch reservation
        time.sleep(float(sys.argv[1]))  # Run for X seconds
    tb.stop()
    tb.wait()  # Good practice on putting the wait in case to restart
    write_log("GNU Radio ending mix-tx-rx")

