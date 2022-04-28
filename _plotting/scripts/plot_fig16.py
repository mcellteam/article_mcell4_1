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
import math
import pickle
from load_data import *
from shared import *

plt.style.use(['../../_plotting/styles/master.mplstyle'])


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
    parser.add_argument('-s', '--single_bng_run', action='store_true',
                        help='the bionetgen directory contains only a single .gdat file')
    parser.add_argument('-e', '--extra', type=str)
    parser.add_argument('-t', '--max-time', type=str)
    parser.add_argument('-l', '--labels', type=str)
    parser.add_argument('-a', '--autophosphorylation', action='store_true',
                        help='special option to generate plots for autophosporylaion ')
    parser.add_argument('-x', '--membrane-localization', action='store_true',
                        help='special option to generate plots for membrane localization model')
    parser.add_argument('-c', '--camkii', action='store_true', help='special option to generate plots for camkii model')
    parser.add_argument('-n', '--snare', action='store_true',
                        help='special option to generate plots for snare complex model')
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

    # for k,df in extra_dfs.items():
    for i in range(len(extra_dfs)):
        df = extra_dfs[i]
        for name, col in df.iteritems():
            line, = ax_plot(ax, df.index, col, label=name)
            if labels:
                line.set_label(labels[current_label])
                current_label += 1
            # ax.legend()  # TODO: what does this do? #0426


def main():
    print('plot_fig16:')

    pdf = matplotlib.backends.backend_pdf.PdfPages('Fig16.pdf')

    fig_names = []

    '''
    python ../../_plotting/scripts/plot_trajectories_single_plot.py --autophosphorylation -m3 react_data_mcell3/ -t 20 -e extra_mcell.txt -l labels_mcell3.txt -o mcell3 -i B
    python ../../_plotting/scripts/plot_trajectories_single_plot.py --autophosphorylation -m4 react_data_mcell4/ -e extra_mcell.txt -t 20 -l labels_mcell.txt -o mcell4 -i A
    python ../../_plotting/scripts/plot_trajectories_single_plot.py --autophosphorylation -b nfsim -e extra_nfsim.txt -t 20 -l labels_nfsim.txt -o nfsim -i C
    '''

    fig = plt.figure()
    fig.set_figwidth(7)

    for i in range(3):

        opts = Options()

        if i == 0:
            ax = fig.add_subplot(311)
            opts.for_autoph = True
            opts.mcell3_dir = 'react_data_mcell3/'
            opts.output = 'mcell3'
            opts.max_time = float(20)
            opts.index_name = 'A'
            opts.extra = 'extra_mcell.txt'
            labels = load_labels('labels_mcell3.txt')
        elif i == 1:
            ax = fig.add_subplot(312)
            opts.for_autoph = True
            opts.mcell4_dir = 'react_data_mcell4/'
            opts.output = 'mcell4'
            opts.max_time = float(20)
            opts.index_name = 'B'
            opts.extra = 'extra_mcell.txt'
            labels = load_labels('labels_mcell.txt')
        elif i == 2:
            ax = fig.add_subplot(313)
            opts.for_autoph = True
            opts.output = 'nfsim'
            opts.max_time = float(20)
            opts.index_name = 'C'
            opts.extra = 'extra_nfsim.txt'
            labels = load_labels('labels_nfsim.txt')
            opts.bng_dir = 'nfsim'

        print('  plot_fig16.py: Working on subplot %s - %s' % (opts.index_name, opts.output))

        # opts = process_opts()

        counts = load_counts(opts)

        all_observables = get_all_observables_names(counts)

        current_label = 0

        # if opts.labels:
        #     labels = load_labels(opts.labels)
        # else:
        #     labels = None

        M4 = 'MCell4'
        names = ['MCell4', 'MCell3R', 'BNG']

        # fig,ax = plt.subplots() #original

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        linestyles = [
            'solid',
            'solid',
            'dashed',
            'dotted',
            'dashdot',
            (0, (3, 1, 1, 1, 1, 1)),  # 'densely dashdotdotted',
        ]

        if opts.for_autoph:
            # fig.set_size_inches((14, 2.5)) #jy

            cm = plt.get_cmap('tab10')
            NUM_COLORS = 6
            colors = [cm(i) for i in range(NUM_COLORS)]
            ax.set_prop_cycle(linestyle=linestyles, color=colors)

            clrs = [None] * 10
        elif opts.for_snare:
            clrs = ['b', 'b', 'r', 'r', 'g', 'g']
        else:
            clrs = ['b', 'g', 'r']

        if opts.for_camkii:
            ax.set_ylim([0, 0.5])

        dfs = {}
        color_index = 0
        # prepare data for
        for obs in sorted(all_observables):
            # print("Processing observable " + obs)

            if opts.for_membrane_localization:
                if obs != 'MA':
                    continue

            if opts.for_camkii:
                if obs not in ['pKCaM2C', 'pKCaM_tot', 'pKCam4Ca']:
                    continue

            legend_names = []
            for i in range(len(counts)):
                if obs not in counts[i]:
                    continue

                data = counts[i][obs]
                # print(obs)

                df = pd.DataFrame()
                df['time'] = data.iloc[:, 0]

                sim_name = names[i]
                sim_obs_name = sim_name + '_' + obs

                df[sim_obs_name] = data.iloc[:, 1:].mean(axis=1)

                if opts.for_camkii:
                    df[sim_obs_name + '_minus_std'] = df[sim_obs_name] - data.iloc[:, 1:].sem(axis=1)
                    df[sim_obs_name + '_plus_std'] = df[sim_obs_name] + data.iloc[:, 1:].sem(axis=1)
                else:
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

                if opts.for_membrane_localization:
                    s = 'solid'

                    if i == 0:
                        ax_plot(ax, df.index, df[sim_obs_name], label=l, linestyle=s, linewidth=2, zorder=100,
                                c=clrs[color_index])  #
                    else:
                        ax_plot(ax, df.index, df[sim_obs_name], label=l, c=clrs[color_index])  #

                elif opts.for_snare:
                    if i == 0:
                        # first file
                        s = 'solid'
                    else:
                        s = '--'
                    ax_plot(ax, df.index, df[sim_obs_name], label=l, linestyle=s, c=clrs[color_index])

                elif opts.for_camkii:
                    ax_plot(ax, df.index, df[sim_obs_name], label=l, color=clrs[color_index])  #
                    ax_fill_between(
                        ax,
                        df.index,
                        df[sim_obs_name + '_minus_std'], df[sim_obs_name + '_plus_std'],
                        alpha=0.2,
                        color=clrs[color_index])

                elif opts.for_autoph:
                    ax_plot(ax, df.index, df[sim_obs_name], label=l)  #
                    ax_fill_between(
                        ax,
                        df.index,
                        df[sim_obs_name + '_minus_std'], df[sim_obs_name + '_plus_std'],
                        alpha=0.2)
                else:
                    sys.exit("Must select plot type")

                color_index += 1

        # extra data to be plotted
        plot_extra_data(opts, ax, labels, current_label)

        plt.xlabel(X_LABEL_TIME_UNIT_S)
        plt.ylabel(Y_LABEL_N_PARAM_TIME)

        if i == 0 or i == 1:
            xlabel_i.set_visible(False)


        # if opts.output in {'mcell4', 'mcell3', 'nfsim'}:
        if opts.output in {'mcell3'}:
            plt.legend(loc='upper left', bbox_to_anchor=(1.05, 0, 0.3, 1.0), fontsize=11)

        plt.subplots_adjust(top=.93, bottom=.10, left=.12, right=.70, wspace=.5, hspace=.65)
        plt.text(-.19, 1.22, '(' + opts.index_name + ')', horizontalalignment='left', verticalalignment='top',
                 transform=ax.transAxes)

        pickle_name = opts.output + '.pickle'
        print('plot_fig16.py: pickling %s ...' % pickle_name)
        pickle.dump((fig, ax), open(pickle_name, 'wb'))

    plt.savefig('Fig16.png')
    pdf.savefig()
    pdf.close()


if __name__ == '__main__':
    main()


