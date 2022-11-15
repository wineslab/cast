#!/usr/bin/env python3

# (c) 2022 Northeastern University
# Created by Davide Villa (villa.d@northeastern.edu)


import constants as const
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import math
import sys
import os
import glob
import csv

from utils import *


def build_rx_files():
    """
    Split the rx file if too big in smaller chunks not to go in overflow
    Return the list of files split to be processed
    """

    # Check if rx file exists
    if not os.path.isfile(const.FILENAME_IQ_RX_DEFAULT):
        write_log_error('', "Rx file not found: " + const.FILENAME_IQ_RX_DEFAULT)
        return np.array([])

    # Split the file in smaller chunks with the unix split command
    os.system("split -d -b 4G " + const.FILENAME_IQ_RX_DEFAULT + " " + const.FILENAME_IQ_RX_SPLIT +
              " --additional-suffix=" + const.FILENAME_IQ_SUFFIX)

    # Retrieve list of rx split files created sorted by created time
    rx_files = sorted(glob.glob(const.FILENAME_IQ_RX_SPLIT + "*"), key=os.path.getmtime)

    # Return rx files split correctly
    write_log("Split rx files in smaller chunks correctly")
    return rx_files


def get_rx_start_period(tx, rx, rxi, all_start_frame, all_rx_sizes):
    """
    Get start frame index and period of the receiving signal data
    If not the first run, retrieve the start from the previous one
    """

    # Get period of the signal from the tx length
    period = tx.size

    # Retrieve start frame from previous one if possible
    if rxi > 0 and all_start_frame[rxi-1] > -1:     # Valid previous start frame
        exceed_rx = all_rx_sizes[rxi-1] - (math.floor(all_rx_sizes[rxi-1] / period) * period)   # Exceed of current rx
        start_frame_tmp = all_start_frame[rxi-1]
        while start_frame_tmp > period:                                     # Retrieve remaining values of the frame
            start_frame_tmp = start_frame_tmp - period
        start_frame = period - (exceed_rx - start_frame_tmp) + period*2     # Compute new start_frame

        # Return start frame and period correctly computed from previous one
        write_log("Computed start frame and period from previous correctly")
        return start_frame, period

    # Get window and seek for start frame cycle point
    for i in range(const.CORR_RX_TRIALS):
        # print("Trial:" + str(i))
        tmp_start = const.CORR_RX_START + const.CORR_RX_START*i
        tmp_end = const.CORR_RX_END + const.CORR_RX_END*i
        if tmp_start > rx.size:             # Check for limits (should not happen)
            tmp_start = 0
        if tmp_end > rx.size:               # Check for limits
            tmp_end = rx.size
        rx4start = rx[tmp_start:tmp_end]

        corr, lags = xcorr(tx, rx4start)    # Compute correlation
        corr = np.flip(corr)                # Flip array to maintain consistency since xcorr flips it
        abs_corr = abs(corr)                # Get absolute value

        max_corr_idx = abs_corr.argmax()
        max_abs_corr = abs_corr[max_corr_idx]
        if max_abs_corr < const.CORR_TH_START:          # Rx signal did not correlate well with the tx
            # print("Max abs corr:" + str(max_abs_corr))
            continue

        if const.PLOT_START:
            plt.figure()
            plt.stem(lags, abs_corr)
            plt.title('CIR to seek for start frame')
            plt.xlabel('Lags')
            plt.ylabel('CIR')
            plt.grid()
            plt.savefig(const.FILENAME_SEEK_START_FRAME)
            # plt.show()

        start_frame_tmp = max_corr_idx + tmp_start      # Start of the higher correlation by adding initial offset
        backing_idx = (start_frame_tmp//period) - 2     # Number of backward computations
        if backing_idx < 0:                             # Check for limits
            backing_idx = 0

        start_frame = start_frame_tmp - (backing_idx * period)      # Actual start by going backwards

        # Return start frame and period correctly
        write_log("Found start frame and period correctly")
        return start_frame, period

    # No start frame found
    write_log("Start frame not found")
    return -1, -1


def pathloss_estimate(tx, rx):
    """
    Estimate the channel loss of the given rx frame against the tx data
    """

    # Pathloss computation
    corr, lags = xcorr(tx, rx)
    max_corr_idx = (abs(corr)).argmax()                 # Get max correlation index
    max_corr = corr[max_corr_idx]                       # Max correlation value
    if abs(max_corr) < const.CORR_TH:                   # Rx signal did not correlate well with the tx
        return 0, 0, 0
    rescale_factor = max_corr / (tx@tx)                 # Compute rescale factor
    pathloss = 20 * np.log10(abs(rescale_factor))       # Convert magnitude to decibel [dB]

    # CIR and PDP computations
    corrI, lagsI = xcorr(tx, rx.real)
    corrI = corrI/tx.size

    corrQ, lagsQ = xcorr(tx, rx.imag)
    corrQ = corrQ/tx.size

    corrI = corrI**2
    corrQ = corrQ**2
    corrIQ = np.array([x + y for x, y in zip(corrI, corrQ)])
    cir = np.sqrt(corrIQ)                               # Channel Impulse Response

    pdpIQ = abs(cir)
    pdp = 20 * np.log10(pdpIQ, where=pdpIQ > 0)         # Power Delay Profile

    return pathloss, cir, pdp


def compute_complete_estimate_start(tx, rx_files):
    """
    Compute pathloss channel estimation of the whole signal received through start frame and period method
    """

    # Define data structures
    all_1res_paths = []     # All pathlosses for current tx-rx transmission
    all_paths = []          # All pathlosses with resolution for current tx-rx transmission
    all_cirs = []           # All cirs with resolution for current tx-rx transmission
    all_pdps = []           # All pdps with resolution for current tx-rx transmission
    all_start_frame = []    # All start of the rx frame for each chunk
    period = -1             # Period of the tx
    all_rx_sizes = []       # All rx sizes for each chunk

    for rxi in range(len(rx_files)):

        filename = rx_files[rxi]        # Get current rx filename to compute

        if os.path.isfile(filename):    # Check if rx filename exists
            rx = load_gnuradio_trace(filename)  # Load rx data
            all_rx_sizes.append(rx.size)        # Store rx size

            start_frame, period = get_rx_start_period(tx, rx, rxi, all_start_frame, all_rx_sizes)   # Start_frame-period
            all_start_frame.append(start_frame)                                                     # Store start_frame

            if start_frame == -1:  # No correlation between the current tx-rx
                write_log("No correlation between the current tx and rx")
                continue

            n_sig = math.floor(
                ((rx.size - start_frame) // period)) - 2  # Sequences to cycle without last and 1 for error

            # Channel estimation computation cycle
            for i in range(n_sig):
                rx_tmp = rx[start_frame + (period * (i - 2)) + 1:start_frame + (
                            period * (i + 2))]  # Frame rx (1 behind; 2 after)
                path_tmp, cir_tmp, pdp_tmp = pathloss_estimate(tx, rx_tmp)  # Make computations

                # Save data
                all_1res_paths.append(path_tmp - const.GAIN_USRP_TX - const.GAIN_USRP_RX)  # Remove USRP gains
                if i % const.RES_SAVE == 0:  # Save data with selected resolution
                    all_paths.append(path_tmp - const.GAIN_USRP_TX - const.GAIN_USRP_RX)  # Remove USRP gains
                    all_cirs.append(cir_tmp)
                    all_pdps.append(pdp_tmp - const.GAIN_USRP_TX - const.GAIN_USRP_RX)  # Remove USRP gains

    # Convert to np arrays for easier computations
    all_1res_paths = np.array(all_1res_paths)
    all_paths = np.array(all_paths)
    all_cirs = np.array(all_cirs)
    all_pdps = np.array(all_pdps)
    all_start_frame = np.array(all_start_frame)
    write_log("Finished all channel estimation computations")

    if all_1res_paths.size == 0:  # There wasn't any correlation between the tx and all rx
        write_log("No correlation between the tx and all rx files")
    write_log("Computed all estimation operations")

    return all_1res_paths, all_paths, all_cirs, all_pdps, all_start_frame, period


def create_results_dir():
    """
    Create results directory and its sub-directories if it doesn't exist
    """

    # Check if directories exist
    if not os.path.exists(const.PATH_RAW_RESULTS):
        os.makedirs(const.PATH_RAW_RESULTS)


def rename_results_dir():
    """
    Rename results directory and its sub-directories to make it unique if bash interactive reservation
    The format will be: results_{SCENARIO_ID}_{SOUNDING_LINK}_{TIMESTAMP}/
    """

    # Check if directory exists
    if os.path.exists(const.PATH_RESULTS) and sys.argv[1] == "0":
        unique_time = datetime.now().strftime('%Y_%m_%d-%H_%M')                                 # Get unique timestamp
        results_name = const.PATH_RESULTS[:-1] + "_" + sys.argv[2] + "_" + sys.argv[3] + unique_time   # Build name
        os.rename(const.PATH_RESULTS[:-1], results_name)                                               # Rename
        write_log("Renamed results directory in " + results_name)


def write_data(all_1res_paths):
    """
    Write into a csv file information about path gains
    """

    ndig = 5        # Number of digits to show for the results
    path0s = np.where(all_1res_paths == 0)[0]               # Find index of paths 0s (no correlation found)
    all_1res_paths_no0 = np.delete(all_1res_paths, path0s)  # All paths with no 0s

    # Compute mean, min, max, standard deviation path information
    mean_path = str(round(np.average(all_1res_paths_no0), ndig))
    min_path = str(round(np.min(all_1res_paths_no0), ndig))
    max_path = str(round(np.max(all_1res_paths_no0), ndig))
    std_path = str(round(np.std(all_1res_paths_no0), ndig))

    print('Mean: ' + mean_path + ' dB ### Min: ' + min_path + ' dB ### Max: ' +
          max_path + ' dB ### SD: ' + std_path + ' dB')

    # Write data into a csv
    path_fields = ['Average [dB]', 'Min [dB]', 'Max [dB]', 'SD']    # Field names
    path_data = [[mean_path, min_path, max_path, std_path]]         # Data
    path_csv_filename = const.FILENAME_PATH_CSV
    with open(path_csv_filename, 'w') as csv_file:
        csvwriter = csv.writer(csv_file)                            # Creating a csv writer object
        csvwriter.writerow(path_fields)                             # Writing the fields
        csvwriter.writerows(path_data)                              # Writing the data

    write_log("Written path data successfully in: " + path_csv_filename)


def plot_data(all_1res_paths, all_paths, all_cirs, all_pdps, all_start_frame, period):
    """
    Print in the command line and write into a csv file information about path gains
    """

    # Plot heatmap path gain
    # if const.PLOT_HEATMAP:
    # Not important in this file

    # Plot first pdp frames (more meaningful for static scenarios)
    if const.PLOT_FRAME:
        # Prepare data to plot
        frame2plot = all_pdps[0]

        frame_time = list(range(frame2plot.size))       # Create time for the plot
        frame_time = [i * ((1 / const.SAMPLE_RATE) * period) for i in frame_time]
        plt.figure()
        plt.plot(frame_time, frame2plot)
        plt.title('Sample frame')
        plt.xlabel('ToA [\u03bcs]')
        plt.ylabel('Path Gain [dB]')
        plt.grid()
        plt.savefig(const.FILENAME_SINGLE_FRAME)
        # plt.show()

    # Plot path gains information
    if const.PLOT_PATHLOSS:
        # Plot all path gains information with 1 resolution
        path_1res_time = list(range(all_1res_paths.size))       # Create time for the plot
        path_1res_time = [i * ((1/(const.SAMPLE_RATE*(10**6)))*period) for i in path_1res_time]
        plt.figure()
        plt.plot(path_1res_time, all_1res_paths)
        plt.title('All path gains with 1 resolution')
        plt.xlabel('Time [s]')
        plt.ylabel('Path Gain [dB]')
        plt.grid()
        plt.savefig(const.FILENAME_ALL_1_RES_PATHS_RESULTS)
        # plt.show()

        # Plot all path gains information
        path_time = list(range(all_paths.size))                 # Create time for the plot
        path_time = [i * (((1/(const.SAMPLE_RATE*(10**6)))*const.RES_SAVE)*period) for i in path_time]
        plt.figure()
        plt.plot(path_time, all_paths)
        plt.title('All path gains')
        plt.xlabel('Time [s]')
        plt.ylabel('Path Gain [dB]')
        plt.grid()
        plt.savefig(const.FILENAME_ALL_PATHS_RESULTS)
        # plt.show()

    # Plot 3d surface of the power delay profile
    if const.PLOT_3DPDP:
        # Prepare data to plot by choosing a certain window
        if const.PDP2PLOT_OFFSET == 0:
            pdp2plot = all_pdps
        else:
            pdp2plot = all_pdps[:, (const.PDP2PLOT_OFFSET + const.PDP2PLOT_WINDOW[0]):
                                   (const.PDP2PLOT_OFFSET + const.PDP2PLOT_WINDOW[1])]

        # Create X time for the plot - Single frame time
        x_3dpdp = list(range(pdp2plot.shape[1]))
        x_3dpdp = [i * (1/(const.SAMPLE_RATE * (10 ** 6))) * (10**6) for i in x_3dpdp]

        # Create Y time for the plot - Whole scenario time
        y_3dpdp = list(range(pdp2plot.shape[0]))
        y_3dpdp = [i * (((1/(const.SAMPLE_RATE*(10**6)))*const.RES_SAVE)*period) for i in y_3dpdp]

        x_3dpdp, y_3dpdp = np.meshgrid(x_3dpdp, y_3dpdp)

        # Plot the surface
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(x_3dpdp, y_3dpdp, pdp2plot, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        # ax.zaxis.set_major_formatter('{x:.02f}')
        ax.set_xlabel('ToA [\u03bcs]')
        ax.set_ylabel('Time [s]')
        ax.set_zlabel('Path Gain [dB]')
        fig.colorbar(surf, shrink=0.5, aspect=5)        # Add color bar
        plt.savefig(const.FILENAME_3DPDP_RESULTS)
        # plt.show()

    write_log("Saved plots successfully in: " + const.PATH_RESULTS)


def export_data(all_1res_paths, all_paths, all_cirs, all_pdps, all_start_frame, period):
    """
    Export all raw data into csv files
    """

    # Write data into csv files
    np.savetxt(const.FILENAME_ALL_1_RES_PATHS_RAW, all_1res_paths, delimiter=",")
    np.savetxt(const.FILENAME_ALL_PATHS_RAW, all_paths, delimiter=",")
    np.savetxt(const.FILENAME_ALL_CIRS_RAW, all_cirs, delimiter=",")
    np.savetxt(const.FILENAME_ALL_PDPS_RAW, all_pdps, delimiter=",")
    np.savetxt(const.FILENAME_ALL_START_FRAME_RAW, all_start_frame, delimiter=",")

    # Write other data into a csv
    path_fields = ['Period', 'Resolution save']  # Field names
    path_data = [[period, const.RES_SAVE]]       # Data
    path_csv_filename = const.FILENAME_VARIOUS_RAW
    with open(path_csv_filename, 'w') as csv_file:
        csvwriter = csv.writer(csv_file)                        # Creating a csv writer object
        csvwriter.writerow(path_fields)                         # Writing the fields
        csvwriter.writerows(path_data)                          # Writing the data

    write_log("Written data successfully in: " + path_csv_filename)


def main():
    """
    Main operations to load data and generate pathloss array for all nodes
    """

    # Load csv Tx data
    iq_tx = load_csv_trace(const.FILENAME_IQ_TX)

    # Create rx filenames
    rx_files = build_rx_files()

    # All main estimate operations
    all_1res_paths, all_paths, all_cirs, all_pdps, all_start_frame, period = \
        compute_complete_estimate_start(iq_tx, rx_files)

    # Create results directories
    create_results_dir()

    # Print and write path gains information
    if const.WRITE_FINAL:
        write_data(all_1res_paths)

    # Plot and print final data
    if const.PLOT_FINAL:
        plot_data(all_1res_paths, all_paths, all_cirs, all_pdps, all_start_frame, period)

    # Plot and print final data
    if const.EXPORT_DATA:
        export_data(all_1res_paths, all_paths, all_cirs, all_pdps, all_start_frame, period)

    # Rename results directory
    rename_results_dir()

    write_log("Exiting start.py")


if __name__ == '__main__':
    """
    Main
    """
    try:
        main()
    except Exception as e_main:
        write_log_error(e_main, "__main__channel-estimate")
