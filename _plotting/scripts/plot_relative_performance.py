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
import textwrap
from shared import *

def create_argparse():
    parser = argparse.ArgumentParser(description='MCell4 Runner')
    parser.add_argument('-d', '--data', type=str, help='cvs file with benchmark results')
    parser.add_argument('-l', '--labels', type=str)
    parser.add_argument('-o', '--output', type=str)
    return parser


def main():
    parser = create_argparse()
    args = parser.parse_args()
    if not args.data:
        sys.exit("Input file must be set with -d.")
    
    print("Loading " + args.data)
    df = pd.read_csv(args.data)
    #print(df)
    
    x = df['Benchmark']
    y = df['MCell3/MCell4']
    
    # wrap label names because they may be long 
    x = ['\n'.join(textwrap.wrap(l, 18)) for l in x]
    
    #print(x)
    
    plt.axhline(y=1,linewidth=1, color='c')
    
    plt_bar(plt, x, y)
    
    plt.ylabel("Relative performance")
    plt.subplots_adjust(bottom=0.3)
    
    # rotate labels by 45 degrees
    plt.xticks(x, rotation=45)
    
    plt.savefig(args.output, dpi=OUTPUT_DPI)

if __name__ == '__main__':
    main()