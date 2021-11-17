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


class Options:
    def __init__(self):
        self.mcell3_dir = None
        self.mcell4_dir = None
        self.bng_dir = None
        self.single_bng_run = False
        self.extra = None
        self.labels = None
        self.max_time = None
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
        
    opts.extra = args.extra
    
    opts.output = args.output

    return opts


def get_mcell_observables_counts(dir):
    counts = {}
    seed_dirs = os.listdir(dir)
    
    for seed_dir in seed_dirs:
        if not seed_dir.startswith('seed_'):
            continue
        
        file_list = os.listdir(os.path.join(dir, seed_dir))
        for file in file_list:
            file_path = os.path.join(dir, seed_dir, file)
            if os.path.isfile(file_path) and file.endswith('.dat'):
                observable = os.path.splitext(file)[0]
                if observable.endswith('_MDLString'):
                    observable = observable[:-len('_MDLString')]
                
                if observable not in counts:
                    index = 0
                else:
                    index = counts[observable].shape[1] - 1 
                
                col_name = 'count' + str(index)
                df = pd.read_csv(file_path, sep=' ', names=['time', col_name])

                if observable not in counts:
                    counts[observable] = df
                else:
                    # add new column
                    counts[observable][col_name] = df[col_name]
                
    return counts 


def get_bng_observables_counts(file, counts):
    if not os.path.exists(file):
        print("Expected file " + file + " not found, skipping it")
        return
    
    with open(file, 'r') as f:
        first_line = f.readline()
        header = first_line.split()[1:]
    df = pd.read_csv(file, delim_whitespace=True, comment='#', names=header)
    return df
    

def process_gdat_file(full_dir, counts):
    df = get_bng_observables_counts(os.path.join(full_dir, 'test.gdat'), counts)
    
    # transform into separate dataframes based on observable 
    for i in range(1, df.shape[1]):
        observable = df.columns[i] 
        if observable not in counts:
            col_name = 'count0'  
            # select time and the current observable
            counts[observable] = pd.DataFrame()           
            counts[observable]['time'] = df.iloc[:, 0]
            counts[observable][col_name] = df.iloc[:, i]
        else:
            col_name = 'count' + str(counts[observable].shape[1] - 1)            
            counts[observable][col_name] = df.iloc[:, i]             
                
                
def get_nfsim_observables_counts(opts):
    single_bng_run = opts.single_bng_run
    dir = opts.bng_dir
    counts = {}
    
    if not single_bng_run:
        nf_dirs = os.listdir(dir)
        
        for nf_dir in nf_dirs:
            full_dir = os.path.join(dir, nf_dir)
            if not nf_dir.startswith('nf_') or not os.path.isdir(full_dir):
                continue
            process_gdat_file(full_dir, counts)
    else:
        process_gdat_file(dir, counts)

    return counts 


def load_gdat_file(fname, sel_str, time_mult):
    print("Loading ", fname)
    df = pd.read_csv(fname, index_col=0, skipinitialspace=True, delim_whitespace=True)
    print(df)
    
    col_names = pd.DataFrame
    sel = [int(i) for i in sel_str.split('-') ]
    col_names = df.columns[sel]
    print("Selecting", col_names)
    
    if not col_names.empty:
        df_sel = df[col_names]
    else:
        df_sel = df
        
    df_sel.index = df_sel.index * time_mult
    df_sel.index.name = 'time' 
        
    return df_sel
        

def load_extra_data(fname):
    res = []
    
    info = pd.read_csv(fname, names=['file', 'sim', 'cols', 'time_mult'], sep=',')
    
    for index, line in info.iterrows():
        res.append(load_gdat_file(line['file'], str(line['cols']), line['time_mult']))
    
    return res    
    

def load_labels(fname):
    res = []
    with open(fname) as f:
        for line in f:
            if not line.strip():
                continue
            res.append(line.strip())

    return res
        
def main():
    
    opts = process_opts()
    
    current_label = 0
    if opts.labels:
        labels = load_labels(opts.labels)
    else:
        labels = None
    
    
    counts = []
    if opts.mcell4_dir:
        if os.path.exists(opts.mcell4_dir):
            print("Reading MCell data from " + opts.mcell4_dir)
            counts.append(get_mcell_observables_counts(opts.mcell4_dir))
        else:
            print("Directory " + opts.mcell4_dir + " with MCell4 data not found, ignored")
            sys.exit(1)
    else:
        counts.append({})

    if opts.mcell3_dir:
        if os.path.exists(opts.mcell3_dir):
            print("Reading MCell data from " + opts.mcell3_dir)
            counts.append(get_mcell_observables_counts(opts.mcell3_dir))
        else:
            print("Error: directory " + opts.mcell3_dir + " with MCell3 data not found, ignored")
            sys.exit(1)
    else:
        counts.append({})
    
    # get_nfsim_observables_counts may return an empty dict
    if opts.bng_dir:
        if os.path.exists(opts.bng_dir):
            print("Reading BNG data from " + opts.bng_dir)
            counts.append(get_nfsim_observables_counts(opts))
        else:
            print("Error: directory " + opts.bng_dir + " with BNG data not found, ignored")
            sys.exit(1)
    else:
        counts.append({})
            
    M4 = 'MCell4'
    names = ['MCell4', 'MCell3R', 'BNG']
    clrs = ['b', 'g', 'r'] 

    all_observables = set(counts[0].keys())
    all_observables = all_observables.union(set(counts[1].keys()))
    all_observables = all_observables.union(set(counts[2].keys()))
    
    fig,ax = plt.subplots()
    #ax.set_title(obs)
    fig.set_size_inches((14,2.5))

    linestyles = [
        'solid',
        'solid',
        'dashed', 
        'dotted', 
        'dashdot', 
        (0, (3, 1, 1, 1, 1, 1)),    # 'densely dashdotdotted', 
#        (0, (3, 1, 3, 1, 1, 1)),
#        (0, (3, 1, 3, 1, 1, 1, 1, 1)),
    ]
    
    cm = plt.get_cmap('tab10')
    NUM_COLORS = 6
    colors = [cm(i) for i in range(NUM_COLORS)]
    ax.set_prop_cycle(linestyle = linestyles, color = colors)
    
    max_time = None

    dfs = {}
    for obs in sorted(all_observables): 
        print("Processing observable " + obs)
        
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
            
            ax.plot(df.index, df[sim_obs_name], label=l) #
            ax.fill_between(
                df.index, 
                df[sim_obs_name + '_minus_std'], df[sim_obs_name + '_plus_std'],
                alpha=0.2, facecolor=clrs[i])
    
            

    if opts.max_time:
        max_time = opts.max_time 
    
    # returns a list of DFs
    if opts.extra:
        extra_dfs = load_extra_data(opts.extra)
    else:
        extra_dfs = {}

    if max_time:
        #for k,df in extra_dfs.items():
        for i in range(len(extra_dfs)):
            df = extra_dfs[i]
            extra_dfs[i] = df[df.index <= max_time]
            

    #for k,df in extra_dfs.items():
    for i in range(len(extra_dfs)):        
        df = extra_dfs[i]
        for name, col in df.iteritems():
            line, = ax.plot(df.index, col, label=name)
            if labels:
                line.set_label(labels[current_label])
                current_label += 1

            ax.legend()
        
    plt.xlabel("time [s]")
    plt.ylabel("N(t)")
    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(right=0.7, bottom=0.2)
    
    #plt.show()
    
    plt.savefig(opts.output, dpi=600)
    #plt.close(fig)


if __name__ == '__main__':
    main()
    
    