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

plt.style.use(['../../_plotting/styles/plot_averages_plot_per_observable.mplstyle','../../_plotting/styles/master.mplstyle'])

class Options:
    def __init__(self):
        self.mcell3_dir = None
        self.mcell4_dir = None
        self.bng_dir = None
        self.single_bng_run = False
        self.labels = None
        self.selected_observables = None

        
def create_argparse():
    parser = argparse.ArgumentParser(description='MCell4 Runner')
    parser.add_argument('-m4', '--mcell4', type=str, help='mcell4 react_data directory')
    parser.add_argument('-m3', '--mcell3', type=str, help='mcell3 react_data directory')
    parser.add_argument('-b', '--bng', type=str, help='bionetgen directory')
    parser.add_argument('-s', '--single_bng_run', action='store_true', help='the bionetgen directory contains only a single .gdat file')
    parser.add_argument('-l', '--labels', type=str, help='file with list of labels (used in order -m4,-m3,-b')
    parser.add_argument('-x', '--selected-observables', type=str, help='file with selected observable names')
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

    if args.labels:
        opts.labels = args.labels

    if args.selected_observables:
        opts.selected_observables = args.selected_observables

    return opts

def main():
    
    opts = process_opts()
    
    counts = load_counts(opts)

    all_observables = get_all_observables_names(counts)

    current_label = 0

    if opts.labels:
        labels = load_labels(opts.labels)
    else:
        labels = None
    
    index_names = []    
    selected_observables = []
    if opts.selected_observables:
        index_names, selected_observables = load_selected_observables(opts.selected_observables)

    clrs = ['b', 'g', 'r'] 
        
    # generate one image per iteration
    index = 0
    for obs in sorted(all_observables): 
        if selected_observables and obs not in selected_observables:
            continue
        
        #print("Processing observable " + obs)
        
        fig,ax = plt.subplots()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        #ax.set_title(obs)
        
        legend_names = []
        for i in range(len(counts)):
            if obs not in counts[i]:
                continue
            
            data = counts[i][obs]
            
            df = pd.DataFrame()           
            df['time'] = data.iloc[:, 0]
            df['means'] = data.iloc[:, 1:].mean(axis=1)
            #print(opts.labels[i], df['means'])
            df['mean_minus_std'] = df['means'] - data.iloc[:, 1:].std(axis=1)
            df['mean_plus_std'] = df['means'] + data.iloc[:, 1:].std(axis=1)
    
            # free collected data to decrease memory consumption        
            del data
                    
            ax_plot(ax, df['time'], df['means'], label=obs + "1", c=clrs[i])
            ax_fill_between(
                ax,
                df['time'], 
                df['mean_minus_std'], df['mean_plus_std'],
                alpha=0.1, facecolor=clrs[i])
    
            legend_names.append(labels[i] + " " + obs)

        plt.legend(legend_names)


        plt.xlabel(X_LABEL_TIME_UNIT_S)
        plt.ylabel(Y_LABEL_N_PARAM_TIME)

        # add_plot_index(plt, ax, index_names[index], x_offset=-0.03)
        # plt.text(.03, .95, '(' + index_names[index] + ')', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
        plt.text(.02, .98, '(' + index_names[index] + ')', horizontalalignment='left', verticalalignment='top',
                 transform=fig.transFigure)
        # plt.savefig(obs + '.png', dpi=OUTPUT_DPI) # 'dpi' now controlled by master stylesheet
        plt.savefig(obs + '.png')
        
        print("Plot " + obs + '.png' + " generated")
        index += 1



if __name__ == '__main__':
    main()
    
    
