
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

X_LABEL_TIME_UNIT_S = "time [s]"
Y_LABEL_N_PARAM_TIME = "N(t)"

OUTPUT_DPI = 600

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
def add_plot_index(plt, ax, name):
    plt.text(-0.07, 1, '(' + name + ')', horizontalalignment='center',
             verticalalignment='center', transform = ax.transAxes)
    