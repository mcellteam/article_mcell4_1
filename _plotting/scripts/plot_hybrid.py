import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import matplotlib.backends.backend_pdf
import numpy as np
import pandas as pd
import sys
import os
from io import StringIO
from hybrid_get_peaks import prepare_data
from shared import *
from fontrc import configure_fonts

plt.style.use(['../../_plotting/styles/plot_multiple.mplstyle','../../_plotting/styles/master.mplstyle'])

particle_D10 = {
'A_first': (0.01292041015625, 0.0009311716138931673),
'A_second': (0.07806904296875, 0.009939225324979456),
'R_first': (0.0439923828125, 0.0032844728737789768),
'R_second': (0.10175634765625, 0.01007365051712571),
#wavelengthA: (0.0651486328125, 0.009805095633254197),
#wavelengthR: (0.05776396484375, 0.009266395224267674),
#lag_time1: (0.031071972656250002, 0.0028195598082764745),
#lag_time2: (0.0236873046875, 0.009283681378756242),
}

hybrid_D10 = {
'A_first': (0.012889941406250001, 0.0008715030086692894),
'A_second': (0.08842421875, 0.00871410129969741),
'R_first': (0.04270078125, 0.00223957984098025),
'R_second': (0.1139828125, 0.00982322230639918),
#wavelengthA: (0.07553427734375, 0.008493865698930644),
#wavelengthR: (0.07128203125, 0.009523904656041067),
#lag_time1: (0.02981083984375, 0.0017704563857977686),
#lag_time2: (0.02555859375, 0.005109072716499823),
}

particle_D1000 = {
'A_first': (0.01331298828125, 0.0009399763187567205),
'A_second': (0.1074794921875, 0.010879388950910706),
'R_first': (0.04133095703125, 0.001976249165597621),
'R_second': (0.13312890625, 0.011149581232355389),
#wavelengthA: (0.09416650390625, 0.010850965923371543),
#wavelengthR: (0.09179794921875001, 0.011025809306508929),
#lag_time1: (0.028017968749999997, 0.0013102533371181049),
#lag_time2: (0.0256494140625, 0.0012868990396521307),
}

hybrid_D1000 = {
'A_first': (0.013311914062500001, 0.000892049519092794),
'A_second': (0.107695703125, 0.011775862994309704),
'R_first': (0.0413341796875, 0.0018761307990409334),
'R_second': (0.13339716796875, 0.01200956940808676),
#wavelengthA: (0.0943837890625, 0.01170519392857754),
#wavelengthR: (0.09206298828124998, 0.01183557055892894),
#lag_time1: (0.028022265625, 0.0012663755686562895),
#lag_time2: (0.02570146484375, 0.0012651999802265157),
}

nfsim = {
'A_first': (0.0133009765625, 0.0009118954422481034),
'A_second': (0.10742314453125, 0.011697155308093971),
'R_first': (0.0413306640625, 0.00199248763803441),
'R_second': (0.13313662109375002, 0.01199618449886365),
#wavelengthA: (0.09412216796875, 0.011599305048245669),
#wavelengthR: (0.09180595703125001, 0.011792659448742138),
#lag_time1: (0.0280296875, 0.0013660731729956833),
#lag_time2: (0.025713476562499997, 0.001269598663288346),
}

ssa = {
'A_first': (0.0133234375, 0.0009217993687599999),
'A_second': (0.1070228515625, 0.011053455171801792),
'R_first': (0.041262109374999995, 0.0019458530091670484),
'R_second': (0.13263349609375003, 0.011392754685309115),
#wavelengthA: 0.09369941406250001, 0.010952303044694862
#wavelengthR: 0.09137138671875, 0.011171326917322944
#lag_time1: 0.027938671875, 0.0013354291667416
#lag_time2: 0.025610644531250004, 0.0012833446856625665
}

ode = {
'A_first': (0.0131, 0),
'A_second': (0.1098, 0),
'R_first': (0.0412, 0),
'R_second': (0.1354, 0),
#wavelengthA: (0.0967, 0),
#wavelengthR: (0.09419999999999999, 0),
#lag_time1: (0.0281, 0),
#lag_time2: (0.025599999999999998, 0),
}
data = [
    (1, particle_D10, 'r', 'particle D=$10^{-7} \, cm^2/s$'),
    (2, hybrid_D10, 'b', 'hybrid D=$10^{-7} \, cm^2/s$'),
    (3, particle_D1000, 'g', 'particle D=$10^{-5} \, cm^2/s$'),
    (4, hybrid_D1000, 'm', 'hybrid D=$10^{-5} \, cm^2/s$'),
    (5, nfsim, 'c', 'NFSim'),
    (6, nfsim, 'y', 'SSA'),
    (7, ode, 'k', 'ODE')
]

def load_gdat_file(file):
    print("Loading " + file)
    wholefile = open(file).read()
    df = pd.read_csv(StringIO(wholefile[1:]), index_col=0, skipinitialspace=True, delim_whitespace=True)
    return df

def load_csv(file):
    print("Loading " + file)
    df = pd.read_csv(file)
    df = df.set_index('time')
    return df        

# shared function to store plots
def finalize_and_save_plot(out, fig):
    plt.xlabel("time [s]")
    plt.savefig(out)
    print("Plot " + out + " generated")

def plot_averages(dir, index_name):
    if index_name == 'A':
    # if 1:
        global ax3
        ax = ax3 = fig.add_subplot(311)
        ax.set_xlim([0, .16])
        ax.set_xticks([0, .02, .04, .06, .08, .10, .12, .14, .16])
        ax.set_ylim([0, 2000])
        ax.set_yticks([0, 1000, 2000])
        ax.xaxis.grid(True, which='major', alpha=0.6, linestyle='--')
        ax.yaxis.grid(False, which='major')  # ensure only vertical lines are plotted
    elif index_name == 'B':
        global ax4
        ax = ax4 = fig.add_subplot(312)
        ax.xaxis.set_tick_params(labelbottom=False)
        ax.xaxis.grid(True, which='major', alpha=0.6, linestyle='--')
        ax.yaxis.grid(False, which='major')  # ensure only vertical lines are plotted
    elif index_name == 'C':
        global ax5
        ax = ax5 = fig.add_subplot(313)
        # plt.yticks([0, 500, 1000, 1500])
        plt.xlabel(X_LABEL_TIME_UNIT_S)
        ax.xaxis.grid(True, which='major', alpha=0.6, linestyle='--')
        ax.yaxis.grid(False, which='major')  # ensure only vertical lines are plotted


    # load all .csv files in directory passed as the first argument
    data = {}

    file_list = os.listdir(dir)
    for file in file_list:
        file_path = os.path.join(dir, file)
        if os.path.isfile(file_path):
            name_ext = os.path.splitext(file)
            if name_ext[1] == '.gdat':
                data[name_ext[0]] = load_gdat(file_path)
            elif name_ext[1] == '.csv':
                data[name_ext[0]] = load_csv(file_path)

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    legend = []
    first = True
    for name,df in data.items():
        df = df.truncate(after = 0.16)
        df = df.rename({'A_mean': 'A', 'R_mean': 'R'}, axis='columns')
        yA = df['A']
        yR = df['R']

        if first:
            ax_plot(ax, df.index, yA, c = 'b')
            ax_plot(ax, df.index, yR, c = 'r')

            first = False
        else:
            ax_plot(ax, df.index, yA)
            ax_plot(ax, df.index, yR)

        if name == 'nfsim':
            name = 'NFSim'
        elif name == 'ssa':
            name = 'SSA'
        elif name == 'hybrid_D1000':
            name = 'hybrid D = $10^{-5} \, cm^2/s$'
        elif name == 'particle_D1000':
            name = 'particle D = $10^{-5} \, cm^2/s$'
        elif name == 'hybrid_D10':
            name = 'hybrid D = $10^{-7} \, cm^2/s$'
        elif name == 'particle_D10':
            name = 'particle D = $10^{-7} \, cm^2/s$'

        legend.append(name + ' - A')
        legend.append(name + ' - R')

    if index_name == 'A':
        leg = plt.legend(legend, loc='upper right', bbox_to_anchor=(0, 0, 1, 1.06), fontsize=7, ncol = 4, frameon=1)
        frame = leg.get_frame()
        frame.set_color('white')
        frame.set_alpha(None)
    else:
        leg = plt.legend(legend, loc='upper right', bbox_to_anchor=(0, 0, 1, 1.06), fontsize=7, ncol = 1, frameon=1)
        frame = leg.get_frame()
        frame.set_color('white')
        frame.set_alpha(None)

    plt.ylabel(Y_LABEL_N_PARAM_TIME)

    plt.text(-.10, 1.06, index_name,  fontweight="bold", transform=ax.transAxes)
        
def plot_low_pass(out, nfsim_seed, index_name):
    # fig, ax = plt.subplots()
    if index_name == 'A':
        global ax1
        ax = ax1 = fig.add_subplot(211)
        ax.xaxis.set_tick_params(labelbottom=False)
        ax.set_xlim([0, .16])
        ax.set_xticks([0, .02, .04, .06, .08, .10, .12, .14, .16])
        ax.set_ylim([0, 2000])
        ax.set_yticks([0, 1000, 2000])

    else:
        ax = fig.add_subplot()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # load base data
    df_nfsim = load_gdat_file('../nfsim/bng/nf_' + str(nfsim_seed).zfill(5) + '/test.gdat')
    
    df_nfsim_plot = df_nfsim.truncate(after = 0.16)
    if True:
        # ax_plot(ax, df_nfsim_plot.index, df_nfsim_plot['A'], label='A', linewidth=linewidth)
        # ax_plot(ax, df_nfsim_plot.index, df_nfsim_plot['R'], label='R', linewidth=linewidth)
        ax_plot(ax, df_nfsim_plot.index, df_nfsim_plot['A'], label='A')
        ax_plot(ax, df_nfsim_plot.index, df_nfsim_plot['R'], label='R')

    # must use full data for filter
    df_lowpass = df_nfsim.copy()
    df_lowpass = prepare_data(df_lowpass, 'A')
    df_lowpass = prepare_data(df_lowpass, 'R')

    df_lowpass = df_lowpass.truncate(after = 0.16)  

    ax_plot(ax, df_lowpass.index, df_lowpass['A'], label='A', c='b')
    ax_plot(ax, df_lowpass.index, df_lowpass['R'], label='R', c='r')

    leg = plt.legend(['A', 'R', 'A (low pass)', 'R (low pass)'], loc='upper right', bbox_to_anchor=(0, 0, 1.00, 1.05),fontsize=7, ncol=2, frameon = 1)
    frame = leg.get_frame()
    frame.set_color('white')
    frame.set_alpha(None)

    plt.ylabel(Y_LABEL_N_PARAM_TIME)
    plt.text(-.22, 1.06, index_name,  fontweight="bold", transform=ax.transAxes)

    ax.xaxis.grid(True, which='major', alpha=0.6, linestyle='--') ###
    ax.yaxis.grid(False, which='major')  # ensure only vertical lines are plotted ###


def plot_peaks_error_bars(out, index_name):
    # fig, ax = plt.subplots()
    if index_name == 'B':
        global ax2
        ax = ax2 = fig.add_subplot(212)
        plt.xlabel(X_LABEL_TIME_UNIT_S)
    else:
        ax = fig.add_subplot()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # plt.legend(['A (low pass)', 'R (low pass)'], loc='center left', bbox_to_anchor=(1, 0.5)) #***
    
    base = 1350/10
    step = 200/len(data)
    
    for d in data[:-1]:
        for v in ['A_first', 'A_second', 'R_first', 'R_second']:
            # example data
            x = d[1][v][0] #np.arange(0.1, 0.2, 0.05)
            xerr = d[1][v][1] 
            y = base + d[0] * step
            
            # error bar values w/ different -/+ errors that
            # also vary with the x-position
            c = 'b' if 'A' in v else 'r'
            
            # ax_errorbar(ax, x, y, xerr=xerr, fmt='|', capsize=3, c=c)
            ax_errorbar(ax, x, y, xerr=xerr, fmt='o', capsize=2, c=c, markersize=2)

            plt.text(-0.002, y - 3, d[3],  font={'size': 7}, horizontalalignment='right', linespacing=None)
    


    red_patch = Line2D([0], [0], color='blue', label='A (low pass peaks)')
    blue_patch = Line2D([0], [0], color='red', label='R (low pass peaks)')
    # plt.legend(['A (low pass)', 'R (low pass)'])
    # plt.legend(handles=[red_patch, blue_patch])
    # leg = plt.legend(handles=[red_patch, blue_patch],loc='upper right', bbox_to_anchor=(0, 0, .98, 1.02), fontsize=6)

    plt.text(-.22, 1.06, index_name,  fontweight="bold", transform=ax.transAxes)

    ax.xaxis.grid(True, which='major', alpha=0.6, linestyle='--')
    ax.yaxis.grid(False, which='major') # ensure only vertical lines are plotted
    ax.set_yticklabels([])
    plt.yticks(visible=True)

    for tick in ax.xaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)

    for tick in ax.yaxis.get_major_ticks():
        tick.tick1line.set_visible(False)
        tick.tick2line.set_visible(False)

    ax.set_xticks(np.arange(0, .16, 0.02))


if __name__ == '__main__':
    print('plot_hybrid.py:')

    configure_fonts()
    pdf = matplotlib.backends.backend_pdf.PdfPages('Fig22.pdf')
    fig = plt.figure(figsize=(6.5, 2))

    print('Working on Fig 22 subplot A')
    plot_low_pass("hybrid_low_pass_nfsim", 14, "A")

    print('Working on Fig 22 subplot B')
    plot_peaks_error_bars("hybrid_peaks", "B")

    figs = list(map(plt.figure, plt.get_fignums()))
    plt.subplots_adjust(top=.90, bottom=.17, left=.18, right=.96, hspace=.30)
    ax2.sharex(ax1)

    plt.savefig('Fig22.png')
    pdf.savefig()
    pdf.close()
    print_summary(fig, 'Figure 22')

    pdf = matplotlib.backends.backend_pdf.PdfPages('Fig23.pdf')
    fig = plt.figure(figsize=(7.5, 3))

    print('Working on Fig 23 subplot A')
    plot_averages("averages_fast", "A")

    print('Working on Fig 23 subplot B')
    plot_averages("averages_hybrid_slow", "B")

    print('Working on Fig 23 subplot C')
    plot_averages("averages_particle_slow", "C")

    plt.subplots_adjust(top=.95, bottom=.12, left=.10, right=.96, hspace=.35)

    ax4.sharex(ax3)
    ax5.sharex(ax3)
    ax4.sharey(ax3)
    ax5.sharey(ax3)

    plt.savefig('Fig23.png')
    pdf.savefig()
    pdf.close()

    print_summary(fig, 'Figure 23')




    
    
    
