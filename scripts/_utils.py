"""
This is a script for ...
"""
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# Settings
pd.set_option('expand_frame_repr', False)  # Single line print for pd.Dataframe


# I Helper Functions


# II Main Functions
def check_non_negative_number(name=None, val=None, min_val=0, max_val=None, accept_none=False, just_int=True):
    """Check if value of given name variable is non-negative integer"""
    check_types = [int] if just_int else [float, int]
    str_check = "non-negative integer" if just_int else "non-negative float"
    add_str = f"n>{min_val}" if max_val is None else f"{min_val}<=n<={max_val}"
    if accept_none:
        add_str += " or None"
    error = f"'{name}' ({val}) should be {str_check} n, where " + add_str
    if accept_none and val is None:
        return None
    if type(val) not in check_types:
        raise ValueError(error)
    if val < min_val:
        raise ValueError(error)
    if max_val is not None and val > max_val:
        raise ValueError(error)


def plot_settings(fig_format="pdf", verbose=False, grid=False, grid_axis="y"):
    """General plot settings"""
    if verbose:
        print(plt.rcParams.keys)    # Print all plot settings that can be modified in general
    sns.set_context("talk", font_scale=0.9)
    #plt.style.use("Solarize_Light2") # https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html
    # Font settings https://matplotlib.org/3.1.1/tutorials/text/text_props.html
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = "Arial"
    plt.rcParams["axes.labelweight"] = "bold"
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.labelsize"] = 17 #13.5
    plt.rcParams["axes.titlesize"] = 16.5 #15
    if fig_format == "pdf":
        mpl.rcParams['pdf.fonttype'] = 42
    elif "svg" in fig_format:
        mpl.rcParams['svg.fonttype'] = 'none'
    font = {'family': 'Arial',
            "weight": "bold"}
    mpl.rc('font', **font)
    # Error bars
    plt.rcParams["errorbar.capsize"] = 10   # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.errorbar.html
    # Grid
    plt.rcParams["axes.grid.axis"] = grid_axis  # 'y', 'x', 'both'
    plt.rcParams["axes.grid"] = grid
    # Legend
    plt.rcParams["legend.frameon"] = False
    plt.rcParams["legend.fontsize"] = "medium" #"x-small"
    plt.rcParams["legend.loc"] = 'upper right'  # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
