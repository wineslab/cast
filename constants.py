#!/usr/bin/env python3

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)

"""
Global constants file that is used to store all constants
"""

""" Parameters """
CODE_SEQUENCE = 1               # Code sequence used - 1: ga128; 2: glfsr; 3: ls1, 4:ls1all, 5:gold
SCENARIO_ID = '90001'            # Scenario id of the experiment
RX_FILE_ID = '10M_1_2'              # RX filename id

SAMPLE_RATE = 10                # Sampling rate [MS/s]
GAIN_USRP_TX = 15               # Gain of transmitter USRP [dB]
GAIN_USRP_RX = 15               # Gain of receiver USRP [dB]
RES_SAVE = 20000                # Resolution to save data, 1 every res_save samples
TX_READ_OFFSET = 0              # Offset of tx file to read to start from (0 for all)
TX_READ_SIZE = 0                # Overall tx file to read size (0 for all)

WRITE_FINAL = True              # Write final data information
PLOT_START = False              # Plot start frame seeking data (not recommended)
PLOT_FRAME = True               # Plot initial frames of the scenario (mostly for static scenarios)
PLOT_FINAL = True               # Plot final data
PLOT_HEATMAP = False            # Plot heatmap
PLOT_PATHLOSS = True            # Plot all pathlosses (of first tap)
PLOT_3DPDP = True               # Plot 3d map of the pdp
EXPORT_DATA = True              # Export final data structures

PDP2PLOT_OFFSET = 1210          # Offset to plot for 3d surface of pdp
PDP2PLOT_WINDOW = [-30, 240]    # Window to plot for 3d surface of pdp starting from offset

""" Filenames """
PATH_ROOT_LOCAL = ''
PATH_FOLDER_LOCAL = PATH_ROOT_LOCAL + ''
PATH_LOG_LOCAL = PATH_FOLDER_LOCAL
PATH_ROOT = '/root/'
PATH_FOLDER = PATH_ROOT + 'radio_api/'
PATH_LOG = '/logs/'
PATH_IQ = PATH_FOLDER_LOCAL + '../data/' + SCENARIO_ID + '/'
PATH_CS = 'code_sequences/'
FILENAME_IQ_END = '_' + SCENARIO_ID + '_' + RX_FILE_ID
FILENAME_CODE_TX = ['ga128_bpsk', 'glfsr_bpsk', 'ls1_bpsk', 'ls1all_bpsk', 'gold_bpsk']
FILENAME_CODE_RX = ['ga128_bpsk_sps4_rrc_usrpSource', 'glfsr_bpsk_rx', 'ls1_bpsk_rx', 'ls1all_bpsk_rx']
FILENAME_IQ_TX = PATH_CS + FILENAME_CODE_TX[CODE_SEQUENCE] + '.csv'
FILENAME_IQ_RX = PATH_IQ + FILENAME_CODE_RX[CODE_SEQUENCE] + FILENAME_IQ_END + '.iq'
FILENAME_PATH_DATA = PATH_LOG_LOCAL + 'path_data_'
FILENAME_LOG = PATH_LOG_LOCAL + 'run.log'
FILENAME_LOG_ERROR = PATH_LOG_LOCAL + 'error.log'
FILENAME_CONFIG = PATH_FOLDER_LOCAL + 'radio.conf'
FILENAME_TX = PATH_FOLDER_LOCAL + 'tx.py'
FILENAME_RX = PATH_FOLDER_LOCAL + 'rx.py'
FILENAME_CHANNEL_EST = PATH_FOLDER_LOCAL + 'channel-estimate.py'

PATH_RESULTS = 'results/'
FILENAME_PATH_CSV = PATH_RESULTS + 'path_info.csv'
FILENAME_SEEK_START_FRAME = PATH_RESULTS + 'seek_start_frame_' + SCENARIO_ID + '_' + RX_FILE_ID + '.pdf'
FILENAME_SINGLE_FRAME = PATH_RESULTS + 'single_frame_' + SCENARIO_ID + '_' + RX_FILE_ID + '.pdf'
FILENAME_ALL_1_RES_PATHS_RESULTS = PATH_RESULTS + 'all_1res_paths_' + SCENARIO_ID + '_' + RX_FILE_ID + '.pdf'
FILENAME_ALL_PATHS_RESULTS = PATH_RESULTS + 'all_paths_' + SCENARIO_ID + '_' + RX_FILE_ID + '.pdf'
FILENAME_3DPDP_RESULTS = PATH_RESULTS + '3dpdp_' + SCENARIO_ID + '_' + RX_FILE_ID + '.pdf'
PATH_RAW_DATA = PATH_RESULTS + 'raw_data/'
FILENAME_ALL_1_RES_PATHS_RAW = PATH_RAW_DATA + 'all_1res_paths.csv'
FILENAME_ALL_PATHS_RAW = PATH_RAW_DATA + 'all_paths.csv'
FILENAME_ALL_CIRS_RAW = PATH_RAW_DATA + 'all_cirs.csv'
FILENAME_ALL_PDPS_RAW = PATH_RAW_DATA + 'all_pdps.csv'
FILENAME_VARIOUS_RAW = PATH_RAW_DATA + 'various.csv'


""" GNU Radio """
TOTAL_TIME = 120    # [s] Total time between each tx-rx set of operations
TX_TIME = 80        # [s] Time for the transmitter to transmit
RX_TIME = 2         # [s] Time for the receiver to receive
RX_WAIT_TIME = 30   # [s] Wait time of the receiver before starting to receive

""" Signal correlation """
CORR_TX_START = 0                   # Start of the initial signal chunk where to search for the start frame
CORR_TX_END = 1024                  # End of the initial signal chunk where to search for the start frame
CORR_RX_START = int(1*1000000)      # Start of the initial signal chunk where to search for the start frame
CORR_RX_END = int(2*1000000)        # End of the initial signal chunk where to search for the start frame
CORR_RX_TRIALS = 100                # Number of trials to search for the start of the frame
CORR_TH_START = 0.5         # Min correlation value to look up for frame start. (Change it for different use cases?)

CORR_RX_WIN_SEEK = 100000           # Window to seek start of the frame cycle around the maximum signal value
CORR_TH_PERC = 0.8        # Correlation threshold percentage (80%). (Is this a good value?)
CORR_TO_ZERO = 25         # Correlation side points to be put to 0 to get next max
CORR_TH = 0.02            # Threshold value for max corr point. (Change it for different use cases?)


""" Colosseum system """
NUMBER_OF_SRN = 128         # Total number of SRNs
