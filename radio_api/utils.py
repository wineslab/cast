#!/usr/bin/env python3

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)

"""
Utils file containing support functions
"""

import configparser
import constants as const
import numpy as np
import scipy.signal as signal
from datetime import datetime


def load_gnuradio_trace(filename):
    """
    Generate iq complex data loading from the gnuradio trace file
    """

    try:
        fid = open(filename, 'rb')          # read (r) and Big-Endian (b) opening
        values = np.fromfile(fid, dtype='float32')
    except Exception as e:
        write_log_error(e, "load_gnuradio_trace")
        return []

    i = values[::2]                     # get even indexes
    q = values[1::2]                    # get odd indexes
    iq = i + 1j*q                       # complex iq values
    # iq = iq.tolist()
    t = list(range(0, len(iq)))         # time vector
    write_log("Loaded rx data")

    return iq


def load_csv_trace(filename):
    """
    Load data from csv file
    """

    try:
        data = np.genfromtxt(filename, delimiter=",")
    except Exception as e:
        write_log_error(e, "load_csv_trace")
        return []
    write_log("Loaded csv tx data")

    return data


def load_config():
    """
    Load general ini config file of a batch job
    """

    try:
        config = configparser.ConfigParser()
        config.read(const.FILENAME_CONFIG)
        write_log("Loaded ini config file")
    except Exception as e:
        write_log_error(e, "load_config")
        return []

    return config


def xcorr(sig1, sig2):
    """
    Perform cross-correlation between the two given signals
    """

    corr = signal.correlate(sig1, sig2, mode="full")        # correlation between tx and rx
    lags = signal.correlation_lags(len(sig1), len(sig2), mode="full")

    return corr, lags


def write_log(msg=""):
    """
    Write logs to a log file
    """

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f = open(const.FILENAME_LOG, 'a')
    f.write("[" + current_time + "] " + msg + '\n')
    f.close()


def write_log_error(e, msg=""):
    """
    Write error logs to a log error file
    """

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    f = open(const.FILENAME_LOG_ERROR, 'a')
    f.write("[" + current_time + "] Exception " + msg + ": ")
    f.write(str(e) + '\n')
    f.close()
