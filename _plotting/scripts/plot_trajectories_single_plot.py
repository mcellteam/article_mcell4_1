#!/usr/bin/env python

"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to [http://unlicense.org] 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import argparse
from load_data import *
from shared import *

class Options:
    def __init__(self):
        self.mcell3_dir = None
        self.mcell4_dir = None
        self.bng_dir = None
        self.single_bng_run = False
        self.extra = None
        self.labels = None
        self.max_time = None
        self.for_membrane_localization = False
        self.output = None

        
def create_argparse():
    parser = argparse.ArgumentParser(description='MCell4 Runner')
    parser.add_argument('-m4', '--mcell4', type=str, help='mcell4 react_data directory')
    parser.add_argument('-m3', '--mcell3', type=str, help='mcell3 react_data directory')
    parser.add_argument('-b', '--bng', type=str, help='bionetgen directory')
    parser.add_argument('-s', '--single_bng_run', action='store_true', help='the bionetgen directory contains only a single .gdat file')
    parser.add_argument('-e', '--extra', type=str)
    parser.add_argument('-t', '--max-time', type=str)
    parser.add_argument('-l', '--labels', type=str)
    parser.add_argument('-x', '--membrane-localization', action='store_true', help='special option to generate plots for membrane localization model')
    parser.add_argument('-o', '--output', type=str)
    return parser


def process_opts():
    parser = create_argparse()
    args = parser.parse_args()
    opts = Options()
    
    if args.mcell4:
        opts.mcell4_dir = args.mcell4 

    if args.mcell3:
        opts.mcell3_dir = args.mcell3 

    if args.bng:
        opts.bng_dir = args.bng 

    if args.single_bng_run:
        opts.single_bng_run = args.single_bng_run 

    if args.max_time:
        opts.max_time = float(args.max_time) 

    if args.labels:
        opts.labels = args.labels
    
    if args.membrane_localization:    
        opts.for_membrane_localization = args.membrane_localization
                
    opts.extra = args.extra
    
    opts.output = args.output

    return opts

def plot_extra_data(opts, ax, labels, current_label):
    max_time = None
    if opts.max_time:
        max_time = opts.max_time 
    
    # returns a list of DFs
    if opts.extra:
        extra_dfs = load_extra_data(opts.extra)
    else:
        extra_dfs = {}

    if max_time:
        # limit extra data to maximum time 
        for i in range(len(extra_dfs)):
            df = extra_dfs[i]
            extra_dfs[i] = df[df.index <= max_time]
            

    #for k,df in extra_dfs.items():
    for i in range(len(extra_dfs)):        
        df = extra_dfs[i]
        for name, col in df.iteritems():
            line, = ax_plot(ax, df.index, col, label=name)
            if labels:
                line.set_label(labels[current_label])
                current_label += 1
            ax.legend() # TODO: what does this do?

def main():
    
    opts = process_opts()
    
    counts = load_counts(opts)

    all_observables = get_all_observables_names(counts)

    current_label = 0

    if opts.labels:
        labels = load_labels(opts.labels)
    else:
        labels = None
                        
    M4 = 'MCell4'
    names = ['MCell4', 'MCell3R', 'BNG']
    clrs = ['b', 'g', 'r'] 

    fig,ax = plt.subplots()

    linestyles = [
        'solid',
        'solid',
        'dashed', 
        'dotted', 
        'dashdot', 
        (0, (3, 1, 1, 1, 1, 1)),    # 'densely dashdotdotted', 
    ]
    
    cm = plt.get_cmap('tab10')
    NUM_COLORS = 6
    colors = [cm(i) for i in range(NUM_COLORS)]
    ax.set_prop_cycle(linestyle = linestyles, color = colors)
    


    if opts.for_membrane_localization:
        # default size is fine here
        ax.set_title('MA')
    else:
        fig.set_size_inches((14,2.5))

    
    dfs = {}
    # prepare data for 
    for obs in sorted(all_observables): 
        print("Processing observable " + obs)
        
        if opts.for_membrane_localization:
            if obs != 'MA':
                continue
        
        legend_names = []
        for i in range(len(counts)):
            if obs not in counts[i]:
                continue
            
            data = counts[i][obs]
            #print(data)
            
            df = pd.DataFrame()           
            df['time'] = data.iloc[:, 0]
            
            sim_name = names[i]
            sim_obs_name = sim_name + '_' + obs 
            
            df[sim_obs_name] = data.iloc[:, 1:].mean(axis=1)
            df[sim_obs_name + '_minus_std'] = df[sim_obs_name] - data.iloc[:, 1:].std(axis=1)
            df[sim_obs_name + '_plus_std'] = df[sim_obs_name] + data.iloc[:, 1:].std(axis=1)

            df = df.set_index('time')
            
            max_time = max(df.index)
    
            # free collected data to decrease memory consumption        
            del data
            
            if labels:
                l = labels[current_label]
                current_label += 1
            else:
                l = 'MCell4'
            
            if opts.for_membrane_localization:
                s = 'solid'
            
                if i == 0:
                    ax_plot(ax, df.index, df[sim_obs_name], label=l, linestyle=s, linewidth=2, zorder=100) #
                else:
                    ax_plot(ax, df.index, df[sim_obs_name], label=l) #

            else:            
                ax_plot(ax, df.index, df[sim_obs_name], label=l) #
                ax_fill_between(
                    ax,
                    df.index, 
                    df[sim_obs_name + '_minus_std'], df[sim_obs_name + '_plus_std'],
                    alpha=0.2, facecolor=clrs[i])
    
            

    # extra data to be plotted
    plot_extra_data(opts, ax, labels, current_label)

    plt.xlabel(X_LABEL_TIME_UNIT_S)
    plt.ylabel(Y_LABEL_N_PARAM_TIME)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(right=0.7, bottom=0.2)
    
    plt.savefig(opts.output, dpi=OUTPUT_DPI)


if __name__ == '__main__':
    main()
    
    