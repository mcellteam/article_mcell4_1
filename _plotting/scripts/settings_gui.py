#!/usr/bin/env python
import os, sys, time, subprocess
from tkinter import ttk, filedialog
import tkinter as tk
from tkinter import Tk, Text
from tkinter.ttk import Style, Notebook, Scrollbar, Treeview, Entry, Label, Frame, Button
from tkinter import *

app = Tk()
app.title("Plot Settings")
app.geometry("300x500")
app['bg'] = '#2a636e'
nb = Notebook(app)

paths = ['styles/master.mplstyle',
         'styles/snare_complex.mplstyle',
         'styles/plot_averages_plot_per_observable.mplstyle',
         'styles/plot_hybrid.mplstyle',
         'styles/plot_relative_performance.mplstyle',
         'styles/plot_trajectories_single_plot.mplstyle']

plot_paths = ['MASTER stylesheet **has precedence**',
              'scripts/plot_trajectories_single_plot.py',
              'scripts/plot_averages_plot_per_observable.py',
              'scripts/plot_hybrid.py',
              'scripts/plot_relative_performance.py',
              'scripts/plot_trajectories_single_plot.py']

cli_paths = ['all.sh',
             '',
             '',
             'hybrid.sh',
             'performance.sh',
             '']


def save():
    frame = nb.select()
    index = nb.index(nb.select())
    path = paths[index]
    print('Saving: ', path)
    new_text = settings[index]
    print('\n-------- New Settings --------\n', new_text.get("1.0", END))
    try:
        with open(path, 'w') as f:
            f.writelines(new_text.get("1.0", END))
    except IOError:
        print('Unable to save')
        return
    print('File saved %s successfully!' % os.path.basename(path))
    return


def run_all():
    print('Running all scripts...')
    subprocess.call('./all.sh')
    print('Done.')

def print_rcParams():
    print(os.getcwd())
    with open('scripts/rcParams.txt', 'r') as f:
        contents = f.readlines()
    file.close()
    print('\n'.join(map(str, contents)))
    # print(contents, sep = '\n')


style = Style()
style.theme_create('dummy', parent='alt', settings={
    'TNotebook': {'configure': {'tabmargins': [2, 5, 2, 0]}},
    'TNotebook.Tab': {
        'configure': {'padding': [1, 1], 'background': '#DCF0F2'},
        'map': {'background': [('selected', '#F2C84B')],
                'expand': [('selected', [1, 1, 1, 0])]}}})
style.theme_use('dummy')

print_params_button = Button(app, text='Print Available rcParams', command=print_rcParams)
print_params_button.pack(side="bottom", fill="x")

run_all_button = Button(app, text='Run All', command=run_all)
run_all_button.pack(side="bottom", fill="x")

save_button = Button(app, text='Save', command=save)
save_button.pack(side="bottom", fill="x")


frames = []
settings = []
for i, path in enumerate(paths):
    file_name = os.path.basename(path)
    print('i=%s,    path=%s,    filename=%s' % (str(i), path, file_name))

    # frames.append(ttk.Frame(nb))
    frames.append(Frame(nb))

    frame = ttk.Frame(nb)
    nb.add(frames[i], text=file_name)
    nb.pack(expand=True, fill=BOTH, padx=5, pady=5)

    ttk.Label(frames[i],
              text = 'Editing: %s\nUsed by: %s' % (paths[i], plot_paths[i]),
              font = 'Helvetica 12 bold').pack(fill='both', side="top", expand=1)

    # adding scrollbars
    ver_sb = Scrollbar(frames[i], orient=VERTICAL)
    ver_sb.pack(side=RIGHT, fill=BOTH)

    hor_sb = Scrollbar(frames[i], orient=HORIZONTAL)
    hor_sb.pack(side=BOTTOM, fill=BOTH)

    # adding writing space
    settings.append(Text(frames[i], width=100, height=100))
    settings[i].pack(side=BOTTOM)

    # binding scrollbar with text area
    settings[i].config(yscrollcommand=ver_sb.set)
    ver_sb.config(command=settings[i].yview)

    settings[i].config(xscrollcommand=hor_sb.set)
    hor_sb.config(command=settings[i].xview)

    file = open(path)
    content = file.read()
    settings[i].insert(END, content)

    # adding path showing box
    pathh = Entry(app)
    pathh.pack(expand=True, fill=X, padx=10)

    # adding scrollbars
    ver_sb = Scrollbar(frames[i], orient=VERTICAL)
    ver_sb.pack(side=RIGHT, fill=BOTH)

    hor_sb = Scrollbar(frames[i], orient=HORIZONTAL)
    hor_sb.pack(side=BOTTOM, fill=BOTH)

app.mainloop()