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
import matplotlib.backends.backend_pdf
import os
import sys
import argparse
from load_data import *
from shared import *
from fontrc import configure_fonts

plt.style.use(['../../_plotting/styles/plot_multiple.mplstyle','../../_plotting/styles/master.mplstyle'])

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
    print('plot_averages_plot_per_observable.py:')
    opts = process_opts()
    configure_fonts()
    pdf = matplotlib.backends.backend_pdf.PdfPages('Fig14.pdf')
    
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

    fig = plt.figure(figsize=(6.5, 2))


    # generate one image per iteration
    index = 0
    for obs in sorted(all_observables): 
        if selected_observables and obs not in selected_observables:
            continue
        
        #print("Processing observable " + obs)
        if index == 0:
            print('  Working on subplot A - ', obs)
            ax = fig.add_subplot(141)
            
        elif  index == 1:
            print('  Working on subplot B - ', obs)
            ax = fig.add_subplot(142)

        elif index == 2:
            print('  Working on subplot C - ', obs)
            ax = fig.add_subplot(143)

        elif index == 3:
            print('  Working on subplot D - ', obs)
            ax = fig.add_subplot(144)


        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
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

        if index_names[index] == 'A':
            plt.ylabel(Y_LABEL_N_PARAM_TIME)

        elif index_names[index] == 'B':
            pass

        elif index_names[index] == 'C':
            pass

        elif index_names[index] == 'D':
            L = plt.legend(loc='upper right', bbox_to_anchor=(0, 0, .99, .96), bbox_transform=fig.transFigure)
            correct_legend_labels = ['MCell4 ', 'MCell3 ', 'NFSim '] #orig
            # correct_legend_labels = ['NFSim ', 'MCell3 ','MCell4 ']
            L.get_texts()[0].set_text(correct_legend_labels[0])
            L.get_texts()[1].set_text(correct_legend_labels[1])
            L.get_texts()[2].set_text(correct_legend_labels[2])


        plt.xlabel(X_LABEL_TIME_UNIT_S)
        # plt.ylabel(Y_LABEL_N_PARAM_TIME)

        ax.title.set_text(obs)

        plt.subplots_adjust(top=.80, bottom=.22, left=.07, right=.89, wspace=.25)
        plt.text(-.26, 1.23, index_names[index], weight="bold", horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
        print("  Plot " + obs + " generated")
        index += 1

    plt.savefig('Fig14.png')
    pdf.savefig()
    pdf.close()
    print_summary(fig, 'Figure 14')


if __name__ == '__main__':
    main()
    
    
