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
import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import os
import sys
import argparse
import math
from load_data import *
from shared import *
from fontrc import configure_fonts
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
from matplotlib.gridspec import GridSpec



class Options:
    def __init__(self):
        self.mcell3_dir = None
        self.mcell4_dir = None
        self.bng_dir = None
        self.single_bng_run = False
        self.extra = None
        self.labels = None
        self.index_name = None
        self.max_time = None
        self.for_autoph = False
        self.for_membrane_localization = False
        self.for_camkii = False
        self.for_snare = False
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
    parser.add_argument('-a', '--autophosphorylation', action='store_true', help='special option to generate plots for autophosporylaion ')
    parser.add_argument('-x', '--membrane-localization', action='store_true', help='special option to generate plots for membrane localization model')
    parser.add_argument('-c', '--camkii', action='store_true', help='special option to generate plots for camkii model')
    parser.add_argument('-n', '--snare', action='store_true', help='special option to generate plots for snare complex model')
    parser.add_argument('-i', '--index-name', type=str)
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

    if args.index_name:
        opts.index_name = args.index_name
    
    if args.autophosphorylation:    
        opts.for_autoph = args.autophosphorylation

    if args.membrane_localization:    
        opts.for_membrane_localization = args.membrane_localization

    if args.camkii:    
        opts.for_camkii = args.camkii

    if args.snare:    
        opts.for_snare = args.snare
                
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
            # ax.legend()

import inspect
def main():
    plt.style.use(['../../_plotting/styles/plot_single.mplstyle', '../../_plotting/styles/master.mplstyle'])

    print('plot_fig13:')
    opts = process_opts()
    configure_fonts()
    pdf = matplotlib.backends.backend_pdf.PdfPages('Fig13.pdf')

    fig = plt.figure(figsize=(6.5, 4))
    gs = GridSpec(2, 4, figure=fig, width_ratios=[.05, 1, 1, 1], height_ratios=[1.8, 1])

    ax = fig.add_subplot(gs[0, 1:])
    ax.set_anchor('W')

    img = mpimg.imread('../snare_complex_rxn_diagram_mod.png')
    plt.imshow(img)
    
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(labelbottom=False, labelleft=False)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.text(0.07, 0.98, 'A', weight="bold", horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)

    counts = load_counts(opts)
    all_observables = get_all_observables_names(counts)
    current_label = 0

    if opts.labels:
        labels = load_labels(opts.labels)
    else:
        labels = None
                        
    M4 = 'MCell4'
    names = ['MCell4', 'MCell3R', 'BNG']

    linestyles = [
        'solid',
        'solid',
        'dashed', 
        'dotted', 
        'dashdot', 
        (0, (3, 1, 1, 1, 1, 1)),    # 'densely dashdotdotted', 
    ]

    cm = plt.cm.get_cmap('tab10')
    NUM_COLORS = len(names)
    NUM_COLORS = 10
    colors = [cm(i) for i in range(NUM_COLORS)]
    # ax.set_prop_cycle(linestyle=linestyles, color=colors)
    ax.set_prop_cycle(color=colors)


    # clrs = ['b', 'b', 'r', 'r', 'g', 'g'] #original
    # clrs = [colors[1], colors[1], colors[3], colors[3], colors[5], colors[5]]
    clrs = [colors[1], colors[1], colors[3], colors[3], 'darkblue', 'darkblue']
    # ax.set_prop_cycle(color=clrs)

    '''
    labels:
    BNGL ODE SNARE_async
    MCell4 SNARE_async
    BNGL ODE SNARE_sync
    MCell4 SNARE_sync
    BNGL ODE V release
    MCell4 V release
    '''
    
    dfs = {}
    color_index = 0
    for obs in sorted(all_observables):

        if obs == 'SNARE_sync':
            ax = fig.add_subplot(gs[1, 1])
            # plt.text(-.30, 1.20, 'B', weight="bold", horizontalalignment='left', verticalalignment='top',transform=ax.transAxes)
            plt.text(0.07, 0.45, 'B', weight="bold", horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
            ax.set_ylim([0, 9])
            ax.set_yticks([0, 3, 6, 9])

        elif obs == 'SNARE_async':
            ax = fig.add_subplot(gs[1, 2])
            # plt.text(-.30, 1.20, 'C', weight="bold", horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
            plt.text(0.37, 0.45, 'C', weight="bold", horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
            ax.yaxis.label.set_visible(False)
            ax.set_ylim([0, 21])
            ax.set_yticks([0, 8, 16, 24])

        elif obs == 'V_release':
            ax = fig.add_subplot(gs[1, 3])
            # plt.text(-.30, 1.20, 'D', weight="bold", horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
            plt.text(0.67, 0.45, 'D', weight="bold", horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
            ax.yaxis.label.set_visible(False)
            ax.set_ylim([0, 60])
            ax.set_yticks([0, 20, 40, 60])

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)


        legend_names = []

        for i in range(len(counts)):
            # loops 3x

            if obs not in counts[i]:
                continue
            
            data = counts[i][obs]
            #print(obs)
            
            df = pd.DataFrame()           
            df['time'] = data.iloc[:, 0]
            
            sim_name = names[i]
            sim_obs_name = sim_name + '_' + obs 
            
            df[sim_obs_name] = data.iloc[:, 1:].mean(axis=1)
            

            df[sim_obs_name + '_minus_std'] = df[sim_obs_name] - data.iloc[:, 1:].std(axis=1)
            df[sim_obs_name + '_plus_std'] = df[sim_obs_name] + data.iloc[:, 1:].std(axis=1)
                

            df = df.set_index('time')
            
            if opts.max_time:
                df = df[df.index <= opts.max_time]
    
            # free collected data to decrease memory consumption        
            del data
            
            if labels:
                l = labels[current_label]
                current_label += 1
            else:
                l = 'MCell4'
            

            if i == 0:
                # first file
                s = 'solid'
            else:
                s = '--'


            ax_plot(ax, df.index, df[sim_obs_name], label=l, linestyle=s, c=clrs[color_index])
            # ax_plot(ax, df.index, df[sim_obs_name], label=l, linestyle=s)

            color_index += 1

        # extra data to be plotted
        plot_extra_data(opts, ax, labels, current_label)
        ax.set_xlim([0, 1])
        ax.set_xticks([0, .2, .4, .6, .8, 1])
        plt.xlabel(X_LABEL_TIME_UNIT_S)
        plt.ylabel(Y_LABEL_N_PARAM_TIME)
        plt.legend(loc='upper left', bbox_to_anchor=(0.08, 1.02), prop={'size': 7})

            
    plt.subplots_adjust(wspace=.35)
    plt.subplots_adjust(hspace=.16)
    plt.subplots_adjust(top=.98)
    plt.subplots_adjust(bottom=0.12)
    plt.subplots_adjust(left=.05, right=0.96)

    plt.savefig('Fig13.png')
    pdf.savefig()
    pdf.close()
    print_summary(fig, 'Figure 13')


if __name__ == '__main__':
    main()
    
    
