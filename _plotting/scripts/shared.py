import sys
import inspect
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.style.use('../../_plotting/styles/master.mplstyle')



# X_LABEL_TIME_UNIT_S = 'time [s]'
X_LABEL_TIME_UNIT_S = 'time (s)'
# Y_LABEL_N_PARAM_TIME = "N(t)"
Y_LABEL_N_PARAM_TIME = '# molecules'

# OUTPUT_DPI = 600 # 'dpi' now controlled by master stylesheet

# wrapper for ax.plot call
def ax_plot(
        ax, x_index, y_data, label=None, **kwargs):
    
    # kwargs is a normal dictionary so one can modify it in any way needed
    # and check what other options were set
    if label:
        kwargs['label'] = label
    
    return ax.plot(x_index, y_data, **kwargs)

def ax_errorbar(
        ax, x_index, y_data, xerr, fmt, capsize, **kwargs):
    
    return ax.errorbar(x_index, y_data, xerr=xerr, fmt=fmt, capsize=capsize, **kwargs)

# wrapper for ax.fill_between call
def ax_fill_between(
        ax, x_index, y_data_low, y_data_high, **kwargs):
    
    return ax.fill_between(
         x_index, y_data_low, y_data_high, **kwargs)

# wrapper for plt.bar call
def plt_bar(plt, x_index, y_data, **kwargs):
    return plt.bar(x_index, y_data, **kwargs)


# adds (a), (b), ...
def add_plot_index(plt, ax, name, x_offset = 0):
    # plt.text(-0.07 + x_offset, 1, '(' + name + ')', horizontalalignment='center',
    #          verticalalignment='center', transform = ax.transAxes)
    plt.text(-0.02 + x_offset, 1.15, '(' + name + ')', horizontalalignment='center',
             verticalalignment='center', transform=ax.transAxes, fontsize=16)


def print_summary(fig, comment=''):
    print('\n-------------------------------------------')
    print('comment: %s' % str(comment))
    print('-------------------------------------------')
    print('Summary of: ',sys.argv[0])
    print('figure size: %sinches, %spixels' % (fig.get_size_inches(), fig.get_size_inches() * fig.dpi))
    print('savefig.dpi: %s' % mpl.rcParams['savefig.dpi'])
    print('figure.dpi: %s' % mpl.rcParams['figure.dpi'])
    print('font: %s, font.size: %s, pdf.fonttype: %s' % (mpl.rcParams['font.family'],mpl.rcParams['font.size'],mpl.rcParams['pdf.fonttype']))
    print('legend.fontsize: %s, axes.labelsize: %s, xtick.labelsize: %s' % (mpl.rcParams['legend.fontsize'], mpl.rcParams['axes.labelsize'],mpl.rcParams['xtick.labelsize']))
    print('lines.linewidth: %s' % mpl.rcParams['lines.linewidth'])
    print('-------------------------------------------\n')



