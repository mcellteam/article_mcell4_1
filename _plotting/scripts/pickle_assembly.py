#!/usr/bin/env python

import os
import sys
import pickle
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.backends.backend_pdf
# from matplotlib.backends.backend_pdf import PdfPages




print('\npickle_assembly.py: Loading pickles...')
# print('curr dir =', os.getcwd()) # /article_mcell4/_plotting/scripts


# os.chdir(sys.path[0])
# print('new curr dir =', os.getcwd())


'''print('Loading Fig14 pickles...')
pdf = matplotlib.backends.backend_pdf.PdfPages('../result/Fig14.pdf')
# fig14a, ax14a = pickle.load(open('../../CaMKII_model_variations/plotting/PSD_transparent.pickle','rb'))
# fig14b, ax14b = pickle.load(open('../../CaMKII_model_variations/plotting/PSD.pickle','rb'))
fig14c, ax14c = pickle.load(open('../../CaMKII_model_variations/plotting/half_in_PSD.pickle','rb'))
pdf.savefig()
pdf.close()'''


'''print('Loading Fig21 pickles...')
pdf = matplotlib.backends.backend_pdf.PdfPages('../result/Fig21.pdf')
fig21a, ax21a = pickle.load(open('../../hybrid_circadian_clock/plotting/hybrid_low_pass_nfsim.pickle','rb'))
fig21b, ax21b = pickle.load(open('../../hybrid_circadian_clock/plotting/hybrid_peaks.pickle','rb'))
fig21c, ax21c = pickle.load(open('../../hybrid_circadian_clock/plotting/hybrid_averages_fast.pickle','rb'))
fig21d, ax21d = pickle.load(open('../../hybrid_circadian_clock/plotting/hybrid_averages_hybrid_slow.pickle','rb'))
fig21e, ax21e = pickle.load(open('../../hybrid_circadian_clock/plotting/hybrid_averages_particle_slow.pickle','rb'))
pdf.savefig(fig21a)
pdf.savefig(fig21b)
pdf.savefig(fig21c)
pdf.savefig(fig21d)
pdf.savefig(fig21e)
pdf.close()'''


# print('Done assembling pickled figures.')





# pp = PdfPages('../result/Fig14_pp.pdf')
# fig_nums = plt.get_fignums()
# figs = [plt.figure(n) for n in fig_nums]
# for fig in figs:
#     fig.savefig(pp, format='pdf')
# pp.close()


# with PdfPages('foo.pdf') as pdf:
#        plt.figure()
#        pdf.savefig(fig)



# fig14, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
# fig, axes = plt.subplm atplots(2, 2)


# fig = plt.figure(constrained_layout=True)
# spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)
# fig = plt.figure()
# fig.add_subplot(ax14a)
# fig.add_subplot(ax14b)
# fig.add_subplot(ax14c)
# fig.axes.append(ax14a)
# fig.axes.append(ax14b)
# fig.axes.append(ax14c)

# gs = fig.add_gridspec(2,2)
# fig.add_axes(ax14a)
# fig.add_subplot(fig14b)
# fig.add_subplot(fig14c)

# fig.add_subplot(gs[3, 1])
# ax1 = ax14a
# ax2 = ax14b
# ax3 = ax14c





# fig14, ax14 = plt.subplots(ncols=2, nrows=2)
# fig14.set_figwidth(7)
# gs = ax14[1, 2].get_gridspec()
#
# fig = plt.figure()
#
# plt.grid(True)


# plt.show()





