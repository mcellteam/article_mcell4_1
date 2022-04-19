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

plt.style.use(['../../_plotting/styles/plot_relative_performance.mplstyle','../../_plotting/styles/master.mplstyle'])

def create_argparse():
    parser = argparse.ArgumentParser(description='MCell4 Runner')
    parser.add_argument('-d', '--data', type=str, help='cvs file with benchmark results')
    parser.add_argument('-l', '--labels', type=str)
    parser.add_argument('-o', '--output', type=str)
    parser.add_argument('-i', '--index-name', type=str)
    return parser


def main():
    parser = create_argparse()
    args = parser.parse_args()
    if not args.data:
        sys.exit("Input file must be set with -d.")
    
    print("Loading " + args.data)
    df = pd.read_csv(args.data) # 'df' type: <class 'pandas.core.frame.DataFrame'>

    # df = df.sort_values(by=['Benchmark'])


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

    fig, ax = plt.subplots()

    # df['MCell3/MCell4'].plot(kind="barh", width = .8)

    dict = df.to_dict()
    names = list(dict['Benchmark'].values())
    results = list(dict['MCell3/MCell4'].values())



    # cm = plt.get_cmap('tab10')
    cm = plt.cm.get_cmap('tab10')
    NUM_COLORS = len(names)
    colors = [cm(i) for i in range(NUM_COLORS)] # type is list
    bar_height = 0.8
    bars = plt.barh(names, results, color=colors, align='center', height = bar_height)

    # rects = ax.barh(range(len(names)), results, color=colors)

    # ax.invert_yaxis()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    plt.axvline(x = 1, color = 'r')
    ax.annotate('1', (1, len(names)), color='red')


    if max(results) < 3:
        ax.xaxis.set_ticks(np.arange(0, 4, 1))

    ax.set_xlabel('Relative Performance')
    ax.set_yticklabels(names)

    for bar in bars:
        width = bar.get_width()
        label_y = bar.get_y() + bar.get_height() / 2
        if width < 1 :
            plt.annotate("{:.2f}".format(width), xy=(1, label_y), ha='left', va='center')
        else:
            plt.annotate("{:.2f}".format(width), xy=(width, label_y), ha='left', va='center')


        # add_plot_index(plt, ax, args.index_name)
        # add_plot_index(plt, ax, args.index_name, x_offset=-.5)
        # add_plot_index(plt, ax, args.index_name)
        #(plt, ax, name, x_offset = 0)
    # plt.text(.03, .95, '(' + args.index_name + ')', horizontalalignment='left',verticalalignment='top', transform=fig.transFigure)
    plt.text(.02, .98, '(' + args.index_name + ')', horizontalalignment='left',verticalalignment='top', transform=fig.transFigure)


    plt.autoscale()

    # plt.savefig(args.output, dpi=OUTPUT_DPI) # 'dpi' now controlled by master stylesheet
    plt.savefig(args.output)
    print("Plot " + args.output + " generated")

    print('Saving figures to PDF...')


    for fig in xrange(1, figure().number):  ## will open an empty extra figure :(
        pdf.savefig(args.output)
    pdf.close()

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
