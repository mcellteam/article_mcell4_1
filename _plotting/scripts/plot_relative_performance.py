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
import textwrap



def create_argparse():
    parser = argparse.ArgumentParser(description='MCell4 Runner')
    parser.add_argument('-d', '--data', type=str, help='cvs file with benchmark results')
    parser.add_argument('-l', '--labels', type=str)
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-i', '--index-name', type=str)
    return parser


def main():
    print('plot_relative_performance.py:')
    print('os.getcwd() =', os.getcwd()) # /Users/joelyancey/MCell/article_mcell4/performance/plotting
    plt.style.use(
        ['../../_plotting/styles/plot_relative_performance.mplstyle', '../../_plotting/styles/master.mplstyle'])
    dataA = '../smaller_ratio.csv'
    dataB = '../larger_ratio.csv'
    datas = [dataA, dataB]
    pdf = matplotlib.backends.backend_pdf.PdfPages('Fig17.pdf')
    fig = plt.figure()
    fig = plt.figure(figsize=(3.5, 3.5))
    # fig.set_figwidth(3.5)
    # fig.set_figwidth(7)


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

        # fig, ax = plt.subplots()

        # fig = plt.figure(2,2,figsize=(100,100))
        # f, axarr = plt.subplots(1,2)
        # fig = plt.figure(figsize=(7.0, 7.0))
        # fig, ax = plt.subplots()

        # ax1 = fig.add_subplot(121)
        # ax2 = fig.add_subplot(122)

        if data == dataA:
            print('Working on subplot A')
            # ax = fig.add_subplot(121)
            # ax = fig.add_subplot(211)
            ax = plt.subplot2grid((7, 2), (0, 0), rowspan=7)
        elif data == dataB:
            print('Working on subplot B')
            # ax = fig.add_subplot(122)
            # ax = fig.add_subplot(212)
            ax = plt.subplot2grid((7, 2), (0, 1), rowspan=3)

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
            names = ['Synaptic Ca Homeostasis Presynaptic', 'Rat NMJ', 'Neuropil    (full model)',
                     'Neuropil (simplified geometry)', 'Mitochondria Presynaptic', 'Membrane Localization',
                     'Auto-     phosphorylation']
        elif data == dataB:
            names = ['CaMKII     Holoenzyme', 'CaMKII      Monomer', 'SynGAP +      TARP']

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
        bar_height = 0.8
        # bars = plt.barh(names, results, color=colors, align='center', height=bar_height)
        # bars = plt.barh(names, results, color='b', align='center', height=bar_height)
        bars = plt.barh(names, results, color='b', align='center', height=bar_height)

        # rects = ax.barh(range(len(names)), results, color=colors)

        # ax.invert_yaxis()
        # ax1.spines['top'].set_visible(False)
        # ax1.spines['right'].set_visible(False)
        # ax1.spines['bottom'].set_visible(False)
        # ax1.spines['left'].set_visible(False)
        # ax2.spines['top'].set_visible(False)
        # ax2.spines['right'].set_visible(False)
        # ax2.spines['bottom'].set_visible(False)
        # ax2.spines['left'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        # ax.annotate('1', (1, len(names)-1), color='red')

        if max(results) < 3:
            ax.xaxis.set_ticks(np.arange(0, 4, 1))
        if max(results) > 3:
            ax.xaxis.set_ticks(np.arange(0, 50, 20))

        ax.set_xlabel('Rel. Performance', fontsize=9)
        # ax.yaxis.set_ticks(names)
        # plt.yticks(wrap=True,linespacing=0.8)
        # plt.yticks(x_axis, [textwrap.fill(label, 10) for name in names],
        #            rotation=10, fontsize=12, horizontalalignment="center")


        # from textwrap import wrap
        # names_wrapped = ['\n'.join(wrap(l, 14)) for l in names]
        # print('labels =\n', str(names_wrapped))
        # # ax.yaxis.set_ticks(names_wrapped)


        for bar in bars:
            width = bar.get_width()
            label_y = bar.get_y() + bar.get_height() / 2

            if width < 1:
                # plt.annotate("{:.2f}".format(width), xy=(1.05, label_y), ha='left', va='center')
                plt.annotate("{:.2f}".format(width), xy=(1.05, label_y), ha='left', va='center', fontsize=9)
            else:
                # plt.annotate("{:.2f}".format(width), xy=(width+.05, label_y), ha='left', va='center')
                if data == dataA:
                    plt.annotate("{:.2f}".format(width), xy=(width+.05, label_y), ha='left', va='center', fontsize=9)
                elif data == dataB:
                    plt.annotate("{:.2f}".format(width), xy=(width + .65, label_y), ha='left', va='center', fontsize=9)



            # add_plot_index(plt, ax, args.index_name)
            # add_plot_index(plt, ax, args.index_name, x_offset=-.5)
            # add_plot_index(plt, ax, args.index_name)
            # (plt, ax, name, x_offset = 0)
        # plt.text(.03, .95, '(' + args.index_name + ')', horizontalalignment='left',verticalalignment='top', transform=fig.transFigure)

        # NOTE use plt.subplots_adjust to modify spacing between subplots
        # subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
        #   left = 0.125  # the left side of the subplots of the figure
        #   right = 0.9  # the right side of the subplots of the figure
        #   bottom = 0.1  # the bottom of the subplots of the figure
        #   top = 0.9  # the top of the subplots of the figure
        #   wspace = 0.2  # the amount of width reserved for blank space between subplots
        #   hspace = 0.2  # the amount of height reserved for white space between subplots
        # https://stackoverflow.com/questions/6541123/improve-subplot-size-spacing-with-many-subplots-in-matplotlib

        #plt.subplots_adjust(wspace=1.3)
        index_name = '(?)'
        if data == dataA:
            index_name = '(A)'
            # plt.text(-2, 1.1, index_name, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
            # plt.text(.1, .9, index_name, horizontalalignment='left', verticalalignment='top', transform=fig.transSubfigure)
            # plt.text(0, 1, index_name, horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
            plt.yticks(names, [textwrap.fill(name, 15) for name in names], linespacing=1.0, fontsize=8)
            dataA_ylim = ax.get_ylim()
            plt.axvline(x=1, ymin=0, ymax=1, color='r', linestyle='--')
            # plt.xticks(fontsize=8)


        elif data == dataB:
            index_name = '(B)'
            # plt.text(-2, 1.1, index_name, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)
            # plt.text(.5, .9, index_name, horizontalalignment='left', verticalalignment='top', transform=fig.transSubfigure)
            # plt.text(.5, 1, index_name, horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
            plt.yticks(names, [textwrap.fill(name, 15) for name in names], linespacing=1.0, fontsize=8)

            # ylim = ax.get_ylim()
            # print('\n\nold ylim = \n\n', str(ylim))
            # figs = list(map(plt.figure, plt.get_fignums()))
            # dataA_ylim = (dataA_ylim[0] + 4, dataA_ylim[1] + 4)
            # print("new ylim = %s\n\n" % str(dataA_ylim))

            # ax.set_ylim(dataA_ylim)

            # plt.axvline(x=1, ymin=0, ymax=4 / 7, color='r', linestyle='--')
            plt.axvline(x=1, ymin=0, ymax=1, color='r', linestyle='--')


        # plt.subplots_adjust(wspace=1.4, left=0.25, bottom=0.15, top=0.9)
        # plt.subplots_adjust(wspace=1.1, left=0.25, right=.95, bottom=0.15, top=0.9)
        # plt.text(.01, .98, '(A)', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
        # plt.text(0.51, .98, '(B)', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
        plt.subplots_adjust(wspace=1.2, left=0.25, right=.93, bottom=0.11, top=0.94)
        plt.text(.01, .97, '(A)', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
        plt.text(0.51, .97, '(B)', horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)

        # plt.subplot_tool()
        # plt.show()
        # plt.text(.02, .98, index_name, horizontalalignment='left', verticalalignment='top', transform=fig.transFigure)
        # plt.text(-.30, 1.1, index_name, horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

        # plt.subplots_adjust(bottom=0.1, right=0.8, top=0.9)

        # plt.autoscale() #0422

        # plt.savefig(args.output, dpi=OUTPUT_DPI) # 'dpi' now controlled by master stylesheet
        # plt.savefig(args.output)
        # print("Plot " + args.output + " generated")

    # plt.subplots_adjust(wspace=3.0, bottom=0.2, top=0.9)


    # print('Getting figures list..')
    # figs = list(map(plt.figure, plt.get_fignums()))
    # print('len(figs) =', len(figs))
    # print('type(figs[0]) = ', type(figs[0]))
    # pdf.savefig(figs[0])
    # pdf.savefig(figs[1])

    plt.savefig('Fig17.png')
    pdf.savefig()
    pdf.close()
    # plt.savefig(base_name + '.tiff')
    # plt.savefig('Fig17.tiff')

    # plt.show()
    # plt.close()

    '''
    str(colors) =  
    [(0.12156862745098039, 0.4666666666666667, 0.7058823529411765, 1.0), 
    (1.0, 0.4980392156862745, 0.054901960784313725, 1.0), 
    (0.17254901960784313, 0.6274509803921569, 0.17254901960784313, 1.0), 
    (0.8392156862745098, 0.15294117647058825, 0.1568627450980392, 1.0), 
    (0.5803921568627451, 0.403921568627451, 0.7411764705882353, 1.0), 
    (0.5490196078431373, 0.33725490196078434, 0.29411764705882354, 1.0)]


    '''

    # ax.set(yticks=x_locs, yticklabels=t_label_lst, ylim=[0 - padding, len(x_locs)])

    # plt.barh(y=df.Benchmark, width=df.Value);

    '''
    names = {0: 'Synaptic Ca Homeostasis Presynaptic', 1: 'Rat Neuromuscular Junction', 2: 'Neuropil - full model', 3: 'Neuropil - with simplified geometry', 4: 'Mitochondria Presynaptic', 5: 'Membrane Localization', 6: 'Auto-phosphorylation'}

    names = {0: 'CaMKII Holoenzyme', 1: 'CaMKII Monomer', 2: 'SynGAP with TARP'}
    '''

    '''
    x = df['Benchmark']
    y = df['MCell3/MCell4']

    # wrap label names because they may be long 
    x = ['\n'.join(textwrap.wrap(l, 18)) for l in x]

    # print(x)

    fig, ax = plt.subplots()

    plt.axhline(y=1, linewidth=1, color='c')

    plt_bar(plt, x, y)

    plt.ylabel("Relative performance")
    plt.subplots_adjust(bottom=0.3)

    # rotate labels by 45 degrees
    plt.xticks(x, rotation=45)
    '''


if __name__ == '__main__':
    main()
