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
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning) #suppress performance warnings

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

def load_counts(opts):
    counts = []
    if opts.mcell4_dir:
        if os.path.exists(opts.mcell4_dir):
            print("Loading MCell data from " + opts.mcell4_dir)
            counts.append(get_mcell_observables_counts(opts.mcell4_dir))
        else:
            print("Directory " + opts.mcell4_dir + " with MCell4 data not found, ignored")
            sys.exit(1)
    else:
        counts.append({})

    if opts.mcell3_dir:
        if os.path.exists(opts.mcell3_dir):
            print("Loading MCell data from " + opts.mcell3_dir)
            counts.append(get_mcell_observables_counts(opts.mcell3_dir))
        else:
            print("Error: directory " + opts.mcell3_dir + " with MCell3 data not found, ignored")
            sys.exit(1)
    else:
        counts.append({})
    
    # get_nfsim_observables_counts may return an empty dict
    if opts.bng_dir:
        if os.path.exists(opts.bng_dir):
            print("Loading BNG data from " + opts.bng_dir)
            counts.append(get_nfsim_observables_counts(opts))
        else:
            print("Error: directory " + opts.bng_dir + " with BNG data not found, ignored")
            sys.exit(1)
    else:
        counts.append({})
        
    return counts
        
    
def get_all_observables_names(counts):
    all_observables = set(counts[0].keys())
    all_observables = all_observables.union(set(counts[1].keys()))
    all_observables = all_observables.union(set(counts[2].keys()))

    return all_observables


def load_gdat_file(fname, sel_str, time_mult):
    print("Loading " + fname)
    df = pd.read_csv(fname, index_col=0, skipinitialspace=True, delim_whitespace=True)
    #print(df)
    
    col_names = pd.DataFrame
    sel = [int(i) for i in sel_str.split('-') ]
    col_names = df.columns[sel]
    #print("Selecting", col_names)
    
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

def load_selected_observables(fname):
    before_split = load_labels(fname)

    index_names = []
    observables = []
    for line in before_split:
        s = line.split(' ')
        index_names.append(s[0])
        observables.append(s[1])
    return index_names, observables
