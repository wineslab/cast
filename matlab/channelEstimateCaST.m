% (c) 2023 Northeastern University
% Institute for the Wireless Internet of Things
% Created by Davide Villa (villa.d@northeastern.edu)

clear
close all
% clc

% Main file to automatically compute average
% pathlosses, cirs and pdps from a single capture.

tic

%% Parameters

folder_data = "results_XXX";   % Name of the data folder where the raw data are
sample_rate = 10e6;     % Sampling rate of the captured signal
code_id = 2;            % Code id - 1: ga128; 2: glfsr; 3: ls1, 4:ls1all, 5:gold
res_save = 20000;       % Resolution to save data, 1 every res_save samples
tx_read_offset = 0;     % Offset of tx file to start reading from (0 for all)
tx_read_size = 0;       % Overall size of tx file to read (0 for all)


tx_usrp_gain = 15;      % Gain of tx USRP
rx_ursp_gain = 15;      % Gain of rx USRP

plot_start = false;     % Plot start frame seeking data
plot_final = true;      % Plot final data
plot_heatmap = false;   % Plot heatmap
plot_pathloss = true;   % Plot all pathlosses (of first tap)
plot_pathloss_1 = false;% Plot all pathlosses with 1 resolution (of first tap)
plot_3dpdp = true;      % Plot 3d map of the pdp
export_data = false;    % Export final data structures


%% Load Tx

tx_folder_data = "tx_data";         % Folder data for transmitted waveform

if code_id == 1
    load(tx_folder_data + "/ga128_sps4_full.mat")
elseif code_id == 2
    load(tx_folder_data + "/glfsr_bpsk_8_0_1.mat")
elseif code_id == 3
    load(tx_folder_data + "/ls1_bpsk.mat")
elseif code_id == 4
    load(tx_folder_data + "/ls1all_bpsk.mat")
elseif code_id == 5
    load(tx_folder_data + "/gold_bpsk.mat")
end

% Rename variables
tx = data(:);
size_tx = length(tx);       % Size of the transmitted code sequence

%% Tx-Rx Node cycles and all operations

% Load rx data
rx = funLoadGnuradioTrace(folder_data + "/raw_data/rx_file_sink_0.iq", tx_read_size, tx_read_offset);

startIdx = 1e6;             % Start index to look for starting point
endIdx = 2e6;               % End index to look for starting point

if plot_start
    figure;
    hold on
    title('Received iq data', 'FontSize', 12);
    plot(real(rx)); 
    plot(imag(rx));
    % plot(abs(data));
    legend('Real', 'Imag');%,'Abs');
    grid on
    hold off

    figure;
    plot(startIdx:endIdx, real(rx(startIdx:endIdx)), 'DisplayName', 'real(rx)')
    hold on
    grid on
    plot(startIdx:endIdx, imag(rx(startIdx:endIdx)), 'DisplayName', 'imag(rx)')
    legend show
end

%% Find start of the signal

period = size_tx;                                               % Period of the signal
start_frame = funChannelStart(tx,rx,period,startIdx,endIdx);    % Start frame of the signal

%% Compute channel estimations

nsig = floor((length(rx)-start_frame)/period)-2;        % Sequences to cycle without last 1 for error

% Define data structures
all_1res_paths = zeros(1,nsig);                         % All pathlosses for current tx-rx transmission
all_paths = zeros(1,floor(nsig/res_save));              % All pathlosses with resolution for current tx-rx transmission
all_cirs = cell(1,floor(nsig/res_save));                % All cirs with resolution for current tx-rx transmission
all_pdps = cell(1,floor(nsig/res_save));                % All pdps with resolution for current tx-rx transmission

for ice = 1:nsig
    rx_tmp = rx(start_frame + (period * (ice-2))+1:start_frame + (period * (ice+2)));   % Frame rx window temp (1 behind; 2 after)
    
    [path_tmp, cir_tmp, pdp_tmp] = funChannelEstimate(tx,rx_tmp,false,sample_rate);     % Make computations
    
    % Save data
    all_1res_paths(1,ice) = path_tmp - tx_usrp_gain - rx_ursp_gain;                     % Removing usrp gains
    if mod(ice,res_save) == 0
        all_paths(1,floor(ice/res_save)) = path_tmp - tx_usrp_gain - rx_ursp_gain;      % Removing usrp gains
        all_cirs{1,floor(ice/res_save)} = cir_tmp;
        all_pdps{1,floor(ice/res_save)} = pdp_tmp - tx_usrp_gain - rx_ursp_gain;        % Removing usrp gains
    end
end


%% Printing some pathloss information

path0s = find(all_1res_paths==0);       % Index of pathloss 0s (no correlation found)
all_paths_no0 = all_1res_paths;         % Pathloss without 0s 
all_paths_no0(path0s) = nan;            % Marking 0 pathloss with NaN to skip them                         

mean_path = mean(all_1res_paths);       % Average pathloss value
min_path = min(all_1res_paths);         % Min pathloss value
max_path = max(all_1res_paths);         % Max pathloss value
std_path = std(all_1res_paths);         % Std pathloss value

fprintf("Mean: " + mean_path + " dB ### Total 0s: " + length(path0s) + " ### Min: " + min_path + " dB ### Max: " + max_path + " dB ### Std: " + std_path + " dB\n")


%% Plot final data

if plot_final
    
    % Plot heatmap pathloss (useful for multiple tx and rx)
    if plot_heatmap
        all_mean_path_heatmap = all_mean_path;
        all_mean_path_heatmap(find(all_mean_path_heatmap==0)) = NaN;
        heatmap_xvalues = num2str(srns);
        heatmap_yvalues = num2str(srns);
        f = figure;
        h = heatmap(heatmap_xvalues, heatmap_yvalues, all_mean_path_heatmap,'MissingDataColor','1.00,1.00,1.00','FontSize',11);%,'Colormap',cool);
        hxp = struct(h);                        % Generate a warning
        hxp.Axes.XAxisLocation = 'top';         % Force x label to the top
        h.XLabel = 'Rx node id';
        h.YLabel = 'Tx node id';
        saveas(h, dirname + "heatmap.eps")
        saveas(h, dirname + "heatmap.pdf")
    end
    
    % Plot pathloss
    if plot_pathloss
        f = figure;
        plot((1:length(all_paths))*((1/sample_rate)*res_save)*period, all_paths);
        hold on
        title('All pathlosses')
        grid on
        xlabel('Time [s]')
        ylabel('Path Gain [dB]')
        set(gca,'FontSize',15);
    end
    
    if plot_pathloss_1
        f = figure;
        plot((1:length(all_1res_paths))*(1/sample_rate)*period, all_1res_paths);
        hold on
        title('All pathlosses with 1 resolution')
        grid on
        xlabel('Time [s]')
        ylabel('Path Gain [dB]')
        set(gca,'FontSize',15);
    end


    % Plot 3d map of pdp (useful for mobile and multitap scenarios)
    if plot_3dpdp
        pdp4plot = zeros(length(all_pdps),length(all_pdps{1,1}));       % Build surface matrix
        for i=1:length(all_pdps)
            for j=1:length(all_pdps{1,1})
                pdp4plot(i,j) = all_pdps{1,i}(1,j);
            end
        end
        pdp2plotoffset = 1210;
        if pdp2plotoffset == 0
            pdp2plot = pdp4plot;
        else
            pdp2plot = pdp4plot(:,pdp2plotoffset-30:pdp2plotoffset+240);
        end
        f = figure;
        surfh = surf((1:size(pdp2plot,2))*(1/sample_rate)*1e6,(1:size(pdp2plot,1))*((1/sample_rate)*res_save)*period,pdp2plot);   % Plot surface
        xlabel("ToA [\mus]")
        ylabel("Time [s]")
        zlabel("Path Gain [dB]")
        set(surfh,'LineStyle','none')                                   % Set line to none otherwise all black
        colorbar
    end
    

end


%% Exporting files

if export_data
    save("scenario_data/" + folder_data + ".mat", 'all_1res_paths', 'all_paths', 'all_cirs', 'all_pdps', 'sample_rate', 'res_save', 'period')
    % save(dirname + "path_data.txt", 'all_mean_path', '-ascii')
    % writematrix(all_mean_path, dirname + "path_data.txt")
end

toc