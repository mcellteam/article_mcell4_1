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
        ['../../_plotting/styles/master.mplstyle','../../_plotting/styles/plot_relative_performance.mplstyle'])
    dataA = '../smaller_ratio.csv'
    dataB = '../larger_ratio.csv'
    datas = [dataA, dataB]
    pdf = matplotlib.backends.backend_pdf.PdfPages('Fig18.pdf')
    fig = plt.figure(figsize=(3.25, 2.25))

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
    
        '''

        if data == dataA:
            print('Working on subplot A')
            ax = plt.subplot2grid((21, 2), (0, 0), rowspan=21)
        elif data == dataB:
            print('Working on subplot B')
            ax = plt.subplot2grid((21, 2), (0, 1), rowspan=10)

        df = pd.read_csv(data)
        dict = df.to_dict()
        names = list(dict['Benchmark'].values())
        results = list(dict['MCell3/MCell4'].values())

        if data == dataA:
            names = ['Synaptic Ca Homeostasis Presynaptic', 'Rat NMJ', 'Neuropil             (full model)',
                     'Neuropil          (simple geometry)', 'Mitochondria Presynaptic', 'Membrane          Localization',
                     'Auto-    phosphorylation']
        elif data == dataB:
            names = ['CaMKII              Holoenzyme', 'CaMKII Monomer', 'SynGAP +      TARP']

        bars = plt.barh(names, results, color='b', align='center', height=.9, linewidth = 0)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.yaxis.set_tick_params(length=0) # hide ticks but keep tiok labels
        ax.xaxis.set_tick_params(length=5)
        ax.set_xlabel('Rel. Performance',labelpad=3)


        for bar in bars:
            width = bar.get_width()
            ylabel_pos = bar.get_y() +.45
            ylabel_valign = 'center'

            if width < 1:
                plt.annotate("{:.2f}".format(width), xy=(1.07, ylabel_pos), ha='left', va=ylabel_valign)
            else:
                if data == dataA:
                    plt.annotate("{:.2f}".format(width), xy=(width+.07, ylabel_pos), ha='left', va=ylabel_valign)
                elif data == dataB:
                    plt.annotate("{:.2f}".format(width), xy=(width + .95, ylabel_pos), ha='left', va=ylabel_valign)


        index_name = '(?)'
        if data == dataA:
            index_name = '(A)'
            plt.yticks(names, [textwrap.fill(name, 21) for name in names], linespacing=.82)
            plt.axvline(x=1, ymin=.01, color='red', linestyle='--', dashes=(4, 1.3), linewidth=1.2)
            ax.xaxis.set_ticks(np.arange(0, 4, 1))

        elif data == dataB:
            index_name = '(B)'
            plt.yticks(names, [textwrap.fill(name, 13) for name in names], linespacing=.82)
            plt.axvline(x=1, ymin=.01, ymax=1.25, color='red', linestyle='--', dashes=(4, 1.2), linewidth=1.3)
            ax.margins(y=.05*(7/3))
            ax.xaxis.set_ticks([0,12,24,36])

        xticks = ax.xaxis.get_major_ticks()
        plt.subplots_adjust(wspace=.9, left=0.23, right=.90, bottom=0.20, top=0.90)
        plt.text(.04, .98, 'A', weight="bold", horizontalalignment='left', verticalalignment='top', transform=fig.transFigure, fontsize=8)
        plt.text(0.51, .98, 'B', weight="bold", horizontalalignment='left', verticalalignment='top', transform=fig.transFigure, fontsize=8)


    plt.savefig('Fig18.png')
    pdf.savefig()
    pdf.close()
    print_summary(fig, 'Figure 18')


if __name__ == '__main__':
    main()
