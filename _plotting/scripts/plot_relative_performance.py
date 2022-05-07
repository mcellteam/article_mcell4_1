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
import textwrap
import csv
from shared import *
from fontrc import configure_fonts


def create_argparse():
    parser = argparse.ArgumentParser(description='MCell4 Runner')
    parser.add_argument('-d', '--data', type=str, help='cvs file with benchmark results')
    parser.add_argument('-l', '--labels', type=str)
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-i', '--index-name', type=str)
    return parser


def main():
    print('plot_relative_performance.py:')
    configure_fonts()
    plt.style.use(
        ['../../_plotting/styles/plot_relative_performance.mplstyle','../../_plotting/styles/master.mplstyle'])
    dataA = '../smaller_ratio.csv'
    dataB = '../larger_ratio.csv'
    datas = [dataA, dataB]
    pdf = matplotlib.backends.backend_pdf.PdfPages('Fig17.pdf')
    fig = plt.figure()

    # fig = plt.figure(figsize=(3.5, 3.5))
    # fig.set_figwidth(3.5)


    # FOR USE WITH CLI OPTIONS, RATHER THAN PRECONFIGURED
    # parser = create_argparse()
    # args = parser.parse_args()
    # if not args.data:
    #     sys.exit("Input file must be set with -d.")
    #
    # print("Loading " + args.data)
    # filename, file_extension = os.path.splitext(args.output)
    # pdf_name = filename + '.pdf'
    # pdf = matplotlib.backends.backend_pdf.PdfPages(pdf_name)
    # df = pd.read_csv(args.data)  # 'df' type: <class 'pandas.core.frame.DataFrame'>
    #
    # # df = df.sort_values(by=['Benchmark'])

    for data in datas:

        '''
        df =
    
           Benchmark                            MCell3        MCell4       MCell3/MCell4
        0  Synaptic Ca Homeostasis Presynaptic  16.333400     14.80580     1.103176
        1  Rat Neuromuscular Junction           13.547004     8.67851      1.560983
        2  Neuropil - full model                29.591750     38.34210     0.771782
        3  Neuropil - with simplified geometry  29.731443     11.06660     2.686592
        4  Mitochondria Presynaptic             19.295052     13.50510     1.428723
        5  Membrane Localization                7192.579639   4412.44000   1.630069
        6  Auto-phosphorylation                 980.279276    844.11200    1.161314
                                                                           ^ this data is plotted
        df =
    
            Benchmark                           MCell3        MCell4       MCell3/MCell4
        0   CaMKII Holoenzyme                   53625.778073  17193.5000   3.118900 
        1   CaMKII Monomer                      224.550784    21.3375      10.52376
        2   SynGAP with TARP                    487.276863    13.8517      35.178127
                                                                           ^ this data is plotted   
    
        '''

        # NOTE: matplotlib pyplot.subplot is a wrapper for Figure.add_subplot which provides additional behavior when
        # working with the implicit API
        # https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.pyplot.subplot.html

        if data == dataA:
            print('Working on subplot A')
            # ax = fig.add_subplot(121)
            # ax = fig.add_subplot(211)
            # ax = plt.subplot2grid((7, 2), (0, 0), rowspan=7)
            ax = plt.subplot2grid((21, 2), (0, 0), rowspan=21)
        elif data == dataB:
            print('Working on subplot B')
            # ax = fig.add_subplot(122)
            # ax = fig.add_subplot(212)
            # ax = plt.subplot2grid((7, 2), (0, 1), rowspan=3)
            ax = plt.subplot2grid((21, 2), (0, 1), rowspan=10)


        # df['MCell3/MCell4'].plot(kind="barh", width = .8)

        # df = pd.read_csv(args.data)
        df = pd.read_csv(data)

        dict = df.to_dict()
        names = list(dict['Benchmark'].values())
        results = list(dict['MCell3/MCell4'].values())

        '''
        original group/index names:
        ['Synaptic Ca Homeostasis Presynaptic', 'Rat Neuromuscular Junction', 'Neuropil - full model', 'Neuropil - with simplified geometry', 'Mitochondria Presynaptic', 'Membrane Localization', 'Auto-phosphorylation']
        and,
        ['CaMKII Holoenzyme', 'CaMKII Monomer', 'SynGAP with TARP']

        '''
        if data == dataA:
            names = ['Synaptic Ca Homeostasis Presynaptic', 'Rat NMJ', 'Neuropil             (full model)',
                     'Neuropil          (simple geometry)', 'Mitochondria Presynaptic', 'Membrane          Localization',
                     'Auto-    phosphorylation']
        elif data == dataB:
            names = ['CaMKII              Holoenzyme', 'CaMKII Monomer', 'SynGAP +      TARP']

        # df1 = pd.read_csv(dataA)
        # dict1 = df1.to_dict()
        # names1 = list(dict1['Benchmark'].values())
        # results1 = list(dict1['MCell3/MCell4'].values())

        # df2 = pd.read_csv(dataB)
        # dict2 = df2.to_dict()
        # names2 = list(dict1['Benchmark'].values())
        # results2 = list(dict1['MCell3/MCell4'].values())

        # df = df.sort_values(by=['Benchmark'])



        # cm = plt.get_cmap('tab10')
        cm = plt.cm.get_cmap('tab10')
        NUM_COLORS = len(names)
        colors = [cm(i) for i in range(NUM_COLORS)]  # type is list
        # ax.set_prop_cycle(linestyle=linestyles, color=colors)
        ax.set_prop_cycle(color=colors)
        bars = plt.barh(names, results, color='b', align='center', height=1, linewidth = .8)
        # bars = plt.barh(names, results, color=colors[0],align='center', height=1, linewidth = .8)
        # bars = plt.barh(names, results, color=colors[5], align='center', height=1, linewidth=.8)
        # bars = plt.barh(names, results, color='b', align='edge', height=1)

        # rects = ax.barh(range(len(names)), results, color=colors)


        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        # ax.spines['left'].set_visible(False)
        # ax.annotate('1', (1, len(names)-1), color='red')
        ax.yaxis.set_tick_params(length=0) # hide ticks but keep tiok labels
        ax.tick_params(width=.8) # thickness of ticks

        if max(results) < 3:
            ax.xaxis.set_ticks(np.arange(0, 4, 1))
        if max(results) > 3:
            ax.xaxis.set_ticks(np.arange(0, 50, 10))

        ax.set_xlabel('Rel. Performance')
        # ax.margins(x=0, y=0)
        # ax.margins(0.05)

        for bar in bars:
            width = bar.get_width()
            # ylabel_pos = bar.get_y() + bar.get_height() / 2
            ylabel_pos = bar.get_y() +.45
            ylabel_valign = 'center'

            # original offsets: 1.05, .05, .65
            if width < 1:
                # plt.annotate("{:.2f}".format(width), xy=(1.07, ylabel_pos), ha='left', va=ylabel_valign)
                plt.annotate("{:.2f}".format(width), xy=(1.07, ylabel_pos), ha='left', va=ylabel_valign)
            else:
                # plt.annotate("{:.2f}".format(width), xy=(width+.07, ylabel_pos), ha='left', va=ylabel_valign)
                if data == dataA:
                    plt.annotate("{:.2f}".format(width), xy=(width+.07, ylabel_pos), ha='left', va=ylabel_valign)
                elif data == dataB:
                    # plt.annotate("{:.2f}".format(width), xy=(width + .65, ylabel_pos), ha='left', va=ylabel_valign)
                    plt.annotate("{:.2f}".format(width), xy=(width + .95, ylabel_pos), ha='left', va=ylabel_valign)



        #plt.subplots_adjust(wspace=1.3)
        index_name = '(?)'
        if data == dataA:
            index_name = '(A)'
            # plt.text(-2, 1.1, index_name, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
            # plt.text(.1, .9, index_name, horizontalalignment='left', verticalalignment='top', transform=fig.transSubfigure)
            # plt.text(0, 1, index_name, horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
            plt.yticks(names, [textwrap.fill(name, 21) for name in names], linespacing=.9)

            # plt.axvline(x=1, ymin=0, ymax=1, color='r', linestyle='--', linewidth=1)
            # plt.axvline(x=1, ymin=.04, ymax=.96, color='r', linestyle='--', linewidth=1)
            plt.axvline(x=1, ymin=.04, color='r', linestyle='--', linewidth=1.0)

            # ax.margins(x=0,y=0)


        elif data == dataB:
            index_name = '(B)'
            # plt.text(-2, 1.1, index_name, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
            # plt.text(.5, .9, index_name, horizontalalignment='left', verticalalignment='top', transform=fig.transSubfigure)
            # plt.text(.5, 1, index_name, horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
            plt.yticks(names, [textwrap.fill(name, 13) for name in names], linespacing=.9)

            # ylim = ax.get_ylim()
            # print('\n\nold ylim = \n\n', str(ylim))
            # figs = list(map(plt.figure, plt.get_fignums()))
            # dataA_ylim = (dataA_ylim[0] + 4, dataA_ylim[1] + 4)
            # print("new ylim = %s\n\n" % str(dataA_ylim))

            # plt.axvline(x=1, ymin=0, ymax=4 / 7, color='r', linestyle='--')
            # plt.axvline(x=1, ymin=0, ymax=1, color='r', linestyle='--', linewidth=1)
            plt.axvline(x=1, color='r', linestyle='--', linewidth=1.0)
            ax.margins(y=.05*(7/3))

        # plt.subplots_adjust(wspace=1.4, left=0.25, bottom=0.15, top=0.9)
        # plt.subplots_adjust(wspace=1.1, left=0.25, right=.95, bottom=0.15, top=0.9)
        # plt.text(.01, .98, '(A)', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
        # plt.text(0.51, .98, '(B)', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
        plt.subplots_adjust(wspace=1.0, left=0.26, right=.92, bottom=0.15, top=0.94)
        plt.text(.01, .98, '(A)', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
        plt.text(0.51, .98, '(B)', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)

    # print('Getting figures list..')
    # figs = list(map(plt.figure, plt.get_fignums()))
    # print('len(figs) =', len(figs))
    # print('type(figs[0]) = ', type(figs[0]))
    # pdf.savefig(figs[0])
    # pdf.savefig(figs[1])

    # plt.savefig('Fig17.tiff')
    plt.savefig('Fig17.png')
    pdf.savefig()
    pdf.close()
    print_summary(fig, 'Figure 17')


if __name__ == '__main__':
    main()
