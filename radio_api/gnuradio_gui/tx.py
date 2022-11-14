#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Tx
# Author: root
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import gr
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio.qtgui import Range, RangeWidget

from gnuradio import qtgui

class tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Tx")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Tx")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "tx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.tx_gain_slider = tx_gain_slider = 15
        self.samp_rate = samp_rate = 10e6
        self.num_disp_points = num_disp_points = 2048
        self.ls2 = ls2 = (1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1)
        self.ls1_all = ls1_all = (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,1,-1,1,1,-1,1,1,1,1,-1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,-1,1,-1,-1,-1,1,1,1,-1,1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,1,1,1,-1,1,-1,-1,-1,1,1,1,1,-1,1,1,1,-1,-1,-1,1,-1,1,1,-1,1,1,1,1,-1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,1,-1,1,1,-1,1,1,1,1,-1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,-1,1,-1,-1,-1,1,1,1,-1,1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,1,1,1,-1,1,1,-1,1,1,1,-1,1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,-1,1,-1,-1,-1,1,1,1,-1,1,-1,-1,1,-1,-1,-1,-1,1,-1,-1)
        self.ls1 = ls1 = (1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,-1,-1,1,-1,1,1,1,-1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,1,1,-1,1,1,1,1,-1,1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1)
        self.glfsr_0s = glfsr_0s = (1,-1,1,1,-1,-1,-1,1,1,1,1,-1,1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,-1,-1,1,-1,-1,-1,-1,1,-1,1,-1,-1,1,1,1,1,1,-1,1,-1,1,-1,1,-1,1,1,1,-1,-1,-1,-1,-1,1,1,-1,-1,-1,1,-1,1,-1,1,1,-1,-1,1,1,-1,-1,1,-1,1,1,1,1,1,1,-1,1,1,1,1,-1,-1,1,1,-1,1,1,1,-1,1,1,1,-1,-1,1,-1,1,-1,1,-1,-1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,1,1,-1,-1,1,1,1,-1,-1,1,1,1,1,-1,-1,-1,1,1,-1,1,1,-1,-1,-1,-1,1,-1,-1,-1,1,-1,1,1,1,-1,1,-1,1,1,1,1,-1,1,1,-1,1,1,1,1,1,-1,-1,-1,-1,1,1,-1,1,-1,-1,1,1,-1,1,-1,1,1,-1,1,1,-1,1,-1,1,-1,-1,-1,-1,-1,1,-1,-1,1,1,1,-1,1,1,-1,-1,1,-1,-1,1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,1,-1,-1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        self.glfsr150 = glfsr150 = (1,-1,1,1,-1,-1,-1,1,1,1,1,-1,1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,-1,-1,1,-1,-1,-1,-1,1,-1,1,-1,-1,1,1,1,1,1,-1,1,-1,1,-1,1,-1,1,1,1,-1,-1,-1,-1,-1,1,1,-1,-1,-1,1,-1,1,-1,1,1,-1,-1,1,1,-1,-1,1,-1,1,1,1,1,1,1,-1,1,1,1,1,-1,-1,1,1,-1,1,1,1,-1,1,1,1,-1,-1,1,-1,1,-1,1,-1,-1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,1,1,-1,-1,1,1,1,-1,-1,1,1,1,1,-1,-1,-1,1,1,-1,1,1,-1,-1,-1)
        self.glfsr = glfsr = (1,-1,1,1,-1,-1,-1,1,1,1,1,-1,1,-1,-1,-1,-1,1,1,1,1,1,1,1,1,-1,-1,1,-1,-1,-1,-1,1,-1,1,-1,-1,1,1,1,1,1,-1,1,-1,1,-1,1,-1,1,1,1,-1,-1,-1,-1,-1,1,1,-1,-1,-1,1,-1,1,-1,1,1,-1,-1,1,1,-1,-1,1,-1,1,1,1,1,1,1,-1,1,1,1,1,-1,-1,1,1,-1,1,1,1,-1,1,1,1,-1,-1,1,-1,1,-1,1,-1,-1,1,-1,1,-1,-1,-1,1,-1,-1,1,-1,1,1,-1,1,-1,-1,-1,1,1,-1,-1,1,1,1,-1,-1,1,1,1,1,-1,-1,-1,1,1,-1,1,1,-1,-1,-1,-1,1,-1,-1,-1,1,-1,1,1,1,-1,1,-1,1,1,1,1,-1,1,1,-1,1,1,1,1,1,-1,-1,-1,-1,1,1,-1,1,-1,-1,1,1,-1,1,-1,1,1,-1,1,1,-1,1,-1,1,-1,-1,-1,-1,-1,1,-1,-1,1,1,1,-1,1,1,-1,-1,1,-1,-1,1,-1,-1,1,1,-1,-1,-1,-1,-1,-1,1,1,1,-1,1,-1,-1,1,-1,-1,-1,1,1,1,-1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1)
        self.ga128 = ga128 = (1,1,-1,-1,-1,-1,-1,-1,-1,1,-1,1,1,-1,-1,1,1,1,-1,-1,1,1,1,1,-1,1,-1,1,-1,1,1,-1,-1,-1,1,1,1,1,1,1,1,-1,1,-1,-1,1,1,-1,1,1,-1,-1,1,1,1,1,-1,1,-1,1,-1,1,1,-1,1,1,-1,-1,-1,-1,-1,-1,-1,1,-1,1,1,-1,-1,1,1,1,-1,-1,1,1,1,1,-1,1,-1,1,-1,1,1,-1,1,1,-1,-1,-1,-1,-1,-1,-1,1,-1,1,1,-1,-1,1,-1,-1,1,1,-1,-1,-1,-1,1,-1,1,-1,1,-1,-1,1)
        self.full_signal_len = full_signal_len = 255
        self.freq = freq = 1000000000

        ##################################################
        # Blocks
        ##################################################
        self._tx_gain_slider_range = Range(0, 31.5, 0.5, 15, 200)
        self._tx_gain_slider_win = RangeWidget(self._tx_gain_slider_range, self.set_tx_gain_slider, 'tx_gain_slider', "counter_slider", float)
        self.top_grid_layout.addWidget(self._tx_gain_slider_win)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
            ",".join(('', '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            '',
        )
        self.uhd_usrp_sink_0_0.set_time_source('external', 0)
        self.uhd_usrp_sink_0_0.set_clock_source('external', 0)
        self.uhd_usrp_sink_0_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0_0.set_gain(tx_gain_slider, 0)
        self.uhd_usrp_sink_0_0.set_antenna('TX/RX', 0)
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_0.set_time_unknown_pps(uhd.time_spec())
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
            num_disp_points, #size
            samp_rate, #samp_rate
            "", #name
            1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            num_disp_points, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            freq, #fc
            samp_rate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            num_disp_points, #size
            "", #name
            1 #number of inputs
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_win)
        self.blocks_vector_source_x_1 = blocks.vector_source_f(glfsr, True, 1, [])
        self.blocks_null_source_1 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.blocks_null_source_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_vector_source_x_1, 0), (self.blocks_float_to_complex_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_gain_slider(self):
        return self.tx_gain_slider

    def set_tx_gain_slider(self, tx_gain_slider):
        self.tx_gain_slider = tx_gain_slider
        self.uhd_usrp_sink_0_0.set_gain(self.tx_gain_slider, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)

    def get_num_disp_points(self):
        return self.num_disp_points

    def set_num_disp_points(self, num_disp_points):
        self.num_disp_points = num_disp_points

    def get_ls2(self):
        return self.ls2

    def set_ls2(self, ls2):
        self.ls2 = ls2

    def get_ls1_all(self):
        return self.ls1_all

    def set_ls1_all(self, ls1_all):
        self.ls1_all = ls1_all

    def get_ls1(self):
        return self.ls1

    def set_ls1(self, ls1):
        self.ls1 = ls1

    def get_glfsr_0s(self):
        return self.glfsr_0s

    def set_glfsr_0s(self, glfsr_0s):
        self.glfsr_0s = glfsr_0s

    def get_glfsr150(self):
        return self.glfsr150

    def set_glfsr150(self, glfsr150):
        self.glfsr150 = glfsr150

    def get_glfsr(self):
        return self.glfsr

    def set_glfsr(self, glfsr):
        self.glfsr = glfsr
        self.blocks_vector_source_x_1.set_data(self.glfsr, [])

    def get_ga128(self):
        return self.ga128

    def set_ga128(self, ga128):
        self.ga128 = ga128

    def get_full_signal_len(self):
        return self.full_signal_len

    def set_full_signal_len(self, full_signal_len):
        self.full_signal_len = full_signal_len

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.freq, self.samp_rate)
        self.uhd_usrp_sink_0_0.set_center_freq(self.freq, 0)





def main(top_block_cls=tx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
