
import matplotlib.pyplot as plt

X_LABEL_TIME_UNIT_S = "time [s]"
Y_LABEL_N_PARAM_TIME = "N(t)"

OUTPUT_DPI = 600

# wrapper for ax.plot call
def ax_plot(
        ax, x_index, y_data, label, **kwargs):
    
    # kwargs is a normal dictionary so one can modify it in any way needed
    # and check what other options were set
    kwargs['label'] = label
    
    return ax.plot(x_index, y_data, **kwargs)

# wrapper for ax.fill_between call
def ax_fill_between(
        ax, x_index, y_data_low, y_data_high, **kwargs):
    
    return ax.fill_between(
         x_index, y_data_low, y_data_high, **kwargs)

