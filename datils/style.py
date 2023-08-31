import time
from math import sqrt
from datetime import datetime
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt

from functools import partial

style_dict = {
    # FONT
    'font.size': 14,
    'font.family': 'sans-serif',
    'font.stretch': 'semi-expanded',
    'font.style': 'normal',
    'font.variant': 'normal',
    'font.weight': 'normal',
    'font.sans-serif': ['Helvetica', 'TeX Gyre Heros', 'Noto Sans'],

    # 'text.usetex': True,
    # 'mathtext.fontset': 'custom',
    # 'mathtext.rm':  'Helvetica',
    # 'mathtext.it': 'Helvetica',
    # 'mathtext.bf': 'Helvetica',
    'mathtext.default': 'regular',

    # AXES
    'axes.linewidth': 1,        # spine thickness
    'axes.xmargin': 0.05,       # spine distance from grid
    'axes.ymargin': 0.05,
    'axes.titlepad': 10.0,
    'axes.labelpad': 5,

    # FIGURE
    'figure.dpi': 250,
    'figure.frameon': False,
    'figure.figsize': [8, 6],
    'figure.facecolor': 'white',

    # LINES
    'lines.linestyle': '-',
    # 'lines.color': '#000000',
    "lines.linewidth": 2,
    "lines.markersize": 6,

    # LEGEND
    # 'legend.framealpha': 1,
    'legend.frameon': False,
    # 'legend.handleheight': 2.5,
    # 'legend.handlelength': 2.5,
    # 'legend.loc': 'upper right',
    # 'legend.labelspacing': 0.8,
    # 'legend.borderpad': 0.5,
    # 'legend.columnspacing': 2.0,

    # "legend.numpoints": 1,
    # "legend.labelspacing": 0.3,
    # "legend.handlelength": 2,
    # "legend.borderpad": 1.0,

    # SAVEFIG
    'savefig.bbox': 'tight',
    'savefig.dpi': 'figure',
    'savefig.edgecolor': 'white',
    'savefig.format': 'png',
    "savefig.transparent": False,

    # X-TICK
    'xtick.alignment': 'center',
    'xtick.direction': 'in',
    'xtick.bottom': True,
    'xtick.top': True,
    'xtick.labelbottom': True,
    'xtick.labeltop': False,
    'xtick.major.width': 1.0,
    'xtick.minor.visible': True,
    'xtick.minor.width': 0.5,
    "xtick.major.size": 5,
    "xtick.minor.size": 3,

    # Y-TICK
    'ytick.alignment': 'center_baseline',
    'ytick.direction': 'in',
    'ytick.labelleft': True,
    'ytick.labelright': False,
    'ytick.left': True,
    'ytick.right': True,
    "ytick.major.size": 10,
    "ytick.minor.size": 5,

    'ytick.minor.visible': True,
    'ytick.minor.width': 0.5,
}

plt.rcParams.update(style_dict)


# Move title axes to right (x) and top (y) --> not working with jupyter if datils is reloaded!
_ORIG_SET_XLABEL = mpl.axes.Axes.set_xlabel
def set_xlabel(axes, label, *args, **kwargs):
    kwargs_ = dict(loc='right')
    kwargs_.update(kwargs)
    _ORIG_SET_XLABEL(axes, label, *args, **kwargs_)

_ORIG_SET_YLABEL = mpl.axes.Axes.set_ylabel
def set_ylabel(axes, label, *args, **kwargs):
    kwargs_ = dict(loc='top')
    kwargs_.update(kwargs)
    _ORIG_SET_YLABEL(axes, label, *args, **kwargs_)

mpl.axes.Axes.set_xlabel = set_xlabel
mpl.axes.Axes.set_ylabel = set_ylabel

# mpl.axes.Axes.set_xlabel = partial(mpl.axes.Axes.set_xlabel, loc='right')
# mpl.axes.Axes.set_ylabel = partial(mpl.axes.Axes.set_ylabel, loc='top')


# Colors
colours_dict = {
    # base 00: #1B2B34
    # base 01: #343D46
    # base 02: #4F5B66
    # base 03: #65737E
    # base 04: #A7ADBA
    # base 05: #C0C5CE
    # base 06: #CDD3DE
    # base 07: #D8DEE9
    # base 08: #EC5f67
    # base 09: #F99157
    # base 0A: #FAC863
    # base 0B: #99C794
    # base 0C: #5FB3B3
    # base 0D: #6699CC
    # base 0E: #C594C5
    # base 0F: #AB7967
}


def _header(palette,
            n_colors,
            fig_width=None,
            fig_height=None):

    # if palette == 'random':
    #     palette = randomcolor()


    n = _n_decider(n_colors)

    # try:
    #     if palette.startswith('colorblind'):
    #         palette = color_blind(palette)
    # except AttributeError:
    ##palette = palette

    # else:
    #     try:
    palette = color_picker(palette=palette, n_colors=n)
    #     except UnboundLocalError:
    #         palette = _label_to_hex(palette, n_colors=n)

    if fig_height != None and fig_width != None:
        plt.figure(figsize=(fig_width, fig_height))

    return palette


def _footer(p,
            xlabel,
            ylabel,
            legend=False,
            n=None,
            save=False,
            tight=True,
            despine=True):

    if legend != False:
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 0.9), ncol=1)

    plt.xlabel(xlabel, color=default_color)
    plt.ylabel(ylabel, color=default_color)

    # if despine == True:
    #     try:
    #         p.spines['bottom'].set_color('black')
    #     except:
    #         pass
    #     sns.despine(left=True, right=True, top=True)

    plt.tight_layout()

    if save:
        if isinstance(save, str):
            filename = save
        else:
            dt = datetime.now()
            time_stamp = time.strftime('%Y%m%d_%H%M%S_' + str(dt.microsecond))
            filename = "astetik_" + time_stamp + ".png"

        plt.savefig(filename, dpi=72)


def _titles(title,
            sub_title,
            location='center',
            fontname='Arial',
            fontsize='18'):

    '''TITLE HANDLER

    Takes care of the extremely painful task of positioning
    various titles and labels dynamically regardless of the plot.
    Or at least that's the idea...

    USE
    ===
    _title_handling(p, data, title, sub_title, samplenote, footnote)

    PARAMETERS
    ==========
    p :: the figure object
    data :: the data that is used in the plot
    title :: title string object or None
    sub_title :: sub_title string object or None
    footnote :: string object or None
    samplenote :: string object or None

    NOTE: At the moment works with one dimensional data.

    '''
    if len(title) + len(sub_title) > 0:
        title = title.replace(' ', '\,')
        title = title.replace('_', '\_')

        plt.title(r"$\bf{" + title + "}$" + '\n' + sub_title,
                  loc=location,
                  fontsize=fontsize,
                  fontname=fontname,
                  weight='normal',
                  y=1.03,
                  color="#342b3b");



def _legend(x, legend, legend_labels, legend_position):

    if legend:
        if legend_labels != None:
            x = legend_labels

        if len(legend_position) == 0:
            plt.legend(x, loc=1, ncol=1, bbox_to_anchor=(1.25, 1.0))
        else:
            plt.legend(x, loc=legend_position[0], ncol=legend_position[1])


def color_picker(palette, center='light', n_colors=10):

    if palette == 'default':
        palette = 'blue_to_red'

    # handle the case where few colors only are used
    if n_colors <= 5:
        n_input = n_colors
        n_colors = 8  # this decides how dark colors will be
    else:
        n_input = n_colors

    if palette == 'blue_to_red':
        out = sns.color_palette("RdBu_r", n_colors=n_colors)
    elif palette == 'blue_to_green':
        out = sns.color_palette("GnBu_d", n_colors=n_colors)
    elif palette == 'red_to_green':
        out = sns.diverging_palette(16, 180, sep=5, center=center, n=n_colors)
    elif palette == 'green_to_red':
        out = sns.diverging_palette(180, 16, sep=5, center=center, n=n_colors)
    elif palette == 'violet_to_blue':
        out = sns.diverging_palette(1, 255, sep=5, center=center, n=n_colors)
    elif palette == 'brown_to_green':
        out = sns.diverging_palette(50, 100, sep=5, center=center, n=n_colors)
    elif palette == 'green_to_marine':
        out = sns.diverging_palette(100, 200, sep=5, center=center, n=n_colors)

    if n_input == 1:
        out = out[0]

    elif n_input == 2:
        out = out[:2]

    if np.ndim(out) == 1:
        out = [out]

    return out


def cmaps(cmap):

    if cmap == 'paired':
        cmap = cm.Paired
    elif cmap == 'jet':
        cmap = cm.jet
    elif cmap == 'prism':
        cmap = cm.prism
    elif cmap == 'RdYlGn':
        cmap = cm.RdYlGn
    elif cmap == 'seismic':
        cmap = cm.seismic
    elif cmap == 'coolwarm':
        cmap = cm.coolwarm
    elif cmap == 'inferno':
        cmap = cm.inferno
    elif cmap == 'plasma':
        cmap = cm.plasma
    elif cmap == 'OrRd':
        cmap = cm.OrRd
    elif cmap == 'tab20c':
        cmap = cm.tab20c

    return cmap


# def _label_to_hex(label, n_colors):
#     hex = sns.color_palette(label, n_colors)
#     return hex.as_hex()

def _sizer(data):
    sizes = data.apply(sqrt)
    sizes = rescaler(sizes, 10)
    return sizes
