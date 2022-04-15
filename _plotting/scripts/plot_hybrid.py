import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import os
import matplotlib.patches as mpatches
from io import StringIO
from matplotlib.lines import Line2D
from hybrid_get_peaks import prepare_data

from shared import *

plt.style.use(['../../_plotting/styles/plot_hybrid.mplstyle','../../_plotting/styles/master.mplstyle'])

INDEX_NAME_OFFSET=0.02

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
        
# used in plot_peaks_error_bars        
data = [
    (1, particle_D10, 'r', 'particle D=1e-7'),
    (2, hybrid_D10, 'b', 'hybrid D=1e-7'),
    (3, particle_D1000, 'g', 'particle D=1e-5'),
    (4, hybrid_D1000, 'm', 'hybrid D=1e-5'),
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
                
    plt.grid(axis="x")
    border = 0.007857
    plt.xlim([0 - border, 0.16 + border])
    
    fig.set_size_inches((14,2.5))                
    # plt.savefig(out, dpi=600) # 'dpi' now controlled by master stylesheet
    plt.savefig(out)
    print("Plot " + out + " generated")

def plot_averages(dir, index_name):
    
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
            
    fig, ax = plt.subplots()
    legend = []
    first = True
    for name,df in data.items():
        df = df.truncate(after = 0.16)  
        df = df.rename({'A_mean': 'A (mean)', 'R_mean': 'R (mean)'}, axis='columns')
        yA = df['A (mean)']
        yR = df['R (mean)']
        
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
            name = 'hybrid D=1e-5'
        elif name == 'particle_D1000':
            name = 'particle D=1e-5'
        elif name == 'hybrid_D10':
            name = 'hybrid D=1e-7'
        elif name == 'particle_D10':
            name = 'particle D=1e-7'
        
        legend.append(name + ' - A (mean)')
        legend.append(name + ' - R (mean)')
    
    # plt.legend(legend) #original
    plt.legend(legend, loc='center left', bbox_to_anchor=(1, 0.5))
    # print('dir = ', str(dir))
    # print('index_name = ', str(index_name))
    plt.ylabel(Y_LABEL_N_PARAM_TIME)
    
    # add_plot_index(plt, ax, index_name, x_offset=INDEX_NAME_OFFSET)
    plt.text(.02, .95, '(' + index_name + ')', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
    
    finalize_and_save_plot("hybrid_" + os.path.basename(dir) + ".png", fig)
        
def plot_low_pass(out, nfsim_seed, index_name):
    fig, ax = plt.subplots()
    
    # load base data
    df_nfsim = load_gdat_file('../nfsim/bng/nf_' + str(nfsim_seed).zfill(5) + '/test.gdat')
    
    df_nfsim_plot = df_nfsim.truncate(after = 0.16)
    if True:
        ax_plot(ax, df_nfsim_plot.index, df_nfsim_plot['A'], label='A')
        ax_plot(ax, df_nfsim_plot.index, df_nfsim_plot['R'], label='R')

    # must use full data for filter
    df_lowpass = df_nfsim.copy()
    df_lowpass = prepare_data(df_lowpass, 'A')
    df_lowpass = prepare_data(df_lowpass, 'R')

    df_lowpass = df_lowpass.truncate(after = 0.16)  
    #print(df_lowpass)

    ax_plot(ax, df_lowpass.index, df_lowpass['A'], label='A', c = 'b')
    ax_plot(ax, df_lowpass.index, df_lowpass['R'], label='R', c = 'r')

    # plt.legend(['A', 'R', 'A (low pass)', 'R (low pass)']) #original
    plt.legend(['A', 'R', 'A (low pass)', 'R (low pass)'], loc='center left', bbox_to_anchor=(1, 0.5))
    plt.ylabel(Y_LABEL_N_PARAM_TIME)
    
    # add_plot_index(plt, ax, index_name, x_offset=INDEX_NAME_OFFSET)
    plt.text(.02, .95, '(' + index_name + ')', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)

    
    finalize_and_save_plot(out, fig)
            

def plot_peaks_error_bars(out, index_name):
    fig, ax = plt.subplots()
    
    # plt.legend(['A (low pass)', 'R (low pass)']) #original
    plt.legend(['A (low pass)', 'R (low pass)'], loc='center left', bbox_to_anchor=(1, 0.5))
    
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
            
            ax_errorbar(ax, x, y, xerr=xerr, fmt='|', capsize=3, c=c)
            
            # 0.007
            #  + 2.5
            # plt.text(0 - 0.0068, y - 3, d[3], c='k')
            # plt.text(0-0.0068, y - 3, d[3], c='k', font={'size': 9})
            plt.text(0-0.0068, y - 3, d[3],  font={'size': 9})
    
    plt.yticks([])

    red_patch = Line2D([0], [0], color='blue', label='A (low pass peaks)')
    blue_patch = Line2D([0], [0], color='red', label='R (low pass peaks)')
    # plt.legend(handles=[red_patch, blue_patch]) #original
    plt.legend(handles=[red_patch, blue_patch], loc='center left', bbox_to_anchor=(1, 0.5))

    # add_plot_index(plt, ax, index_name, x_offset=INDEX_NAME_OFFSET)
    plt.text(.05, .95, '(' + index_name + ')', horizontalalignment='left', verticalalignment='top',transform=fig.transFigure)
    
    finalize_and_save_plot(out, fig)


if __name__ == '__main__':
    
    #for s in range(1, 20):
    #    plot_low_pass("hybrid_low_pass_nfsim" + str(s).zfill(5) + ".png", s)
    
    # NFSim seed 14 quite nicely matches the averages 
    plot_low_pass("hybrid_low_pass_nfsim.png", 14, "A")
    
    plot_peaks_error_bars("hybrid_peaks.png", "B")
    
    plot_averages("averages_fast", "C")
    plot_averages("averages_hybrid_slow", "D")
    plot_averages("averages_particle_slow", "E")
    
    
    
