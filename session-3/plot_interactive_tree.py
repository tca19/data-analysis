import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from sklearn.tree import DecisionTreeClassifier

from six import StringIO
from sklearn.tree import export_graphviz
from matplotlib.pyplot import imread
from scipy import ndimage
from sklearn.datasets import make_moons

from matplotlib.colors import ListedColormap, colorConverter
import re

cm2 = ListedColormap(['#0000aa', '#ff2020'])

def tree_image(tree, fout=None):
    try:
        import graphviz
    except ImportError:
        # make a hacky white plot
        x = np.ones((10, 10))
        x[0, 0] = 0
        return x
    dot_data = StringIO()
    export_graphviz(tree, out_file=dot_data, max_depth=3, impurity=False)
    data = dot_data.getvalue()
    #data = re.sub(r"gini = 0\.[0-9]+\\n", "", dot_data.getvalue())
    data = re.sub(r"samples = [0-9]+\\n", "", data)
    data = re.sub(r"\\nsamples = [0-9]+", "", data)
    data = re.sub(r"value", "counts", data)

    graph = graphviz.Source(data, format="png")
    if fout is None:
        fout = "tmp"
    graph.render(fout)
    return imread(fout + ".png")


def plot_tree_progressive():
    X, y = make_moons(n_samples=100, noise=0.25, random_state=3)
    #plt.figure()
    ax = plt.gca()
    discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
    ax.set_xticks(())
    ax.set_yticks(())

    axes = []
    for i in range(3):
        fig, ax = plt.subplots(1, 2, figsize=(12, 4),
                               subplot_kw={'xticks': (), 'yticks': ()})
        axes.append(ax)
    axes = np.array(axes)

    for i, max_depth in enumerate([1, 2, 9]):
        tree = plot_tree(X, y, max_depth=max_depth, ax=axes[i, 0])
        axes[i, 1].imshow(tree_image(tree))
        axes[i, 1].set_axis_off()


def plot_tree_partition(X, y, tree, ax=None):
    if ax is None:
        ax = plt.gca()
    eps = X.std() / 2.

    x_min, x_max = X[:, 0].min() - eps, X[:, 0].max() + eps
    y_min, y_max = X[:, 1].min() - eps, X[:, 1].max() + eps
    xx = np.linspace(x_min, x_max, 1000)
    yy = np.linspace(y_min, y_max, 1000)

    X1, X2 = np.meshgrid(xx, yy)
    X_grid = np.c_[X1.ravel(), X2.ravel()]

    Z = tree.predict(X_grid)
    Z = Z.reshape(X1.shape)
    faces = tree.apply(X_grid)
    faces = faces.reshape(X1.shape)
    border = ndimage.laplace(faces) != 0
    ax.contourf(X1, X2, Z, alpha=.4, cmap=cm2, levels=[0, .5, 1])
    ax.scatter(X1[border], X2[border], marker='.', s=1)

    discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks(())
    ax.set_yticks(())
    return ax


def plot_tree(X, y, max_depth=1, ax=None):
    tree = DecisionTreeClassifier(max_depth=max_depth, random_state=0).fit(X, y)
    ax = plot_tree_partition(X, y, tree, ax=ax)
    ax.set_title("depth = %d" % max_depth)
    return tree


def discrete_scatter(x1, x2, y=None, markers=None, s=10, ax=None,
                     labels=None, padding=.2, alpha=1, c=None, markeredgewidth=None):
    """Adaption of matplotlib.pyplot.scatter to plot classes or clusters.
    Parameters
    ----------
    x1 : nd-array
        input data, first axis
    x2 : nd-array
        input data, second axis
    y : nd-array
        input data, discrete labels
    cmap : colormap
        Colormap to use.
    markers : list of string
        List of markers to use, or None (which defaults to 'o').
    s : int or float
        Size of the marker
    padding : float
        Fraction of the dataset range to use for padding the axes.
    alpha : float
        Alpha value for all points.
    """
    if ax is None:
        ax = plt.gca()

    if y is None:
        y = np.zeros(len(x1))

    unique_y = np.unique(y)

    if markers is None:
        markers = ['o', '^', 'v', 'D', 's', '*', 'p', 'h', 'H', '8', '<', '>'] * 10

    if len(markers) == 1:
        markers = markers * len(unique_y)

    if labels is None:
        labels = unique_y

    # lines in the matplotlib sense, not actual lines
    lines = []

    current_cycler = mpl.rcParams['axes.prop_cycle']

    for i, (yy, cycle) in enumerate(zip(unique_y, current_cycler())):
        mask = y == yy
        # if c is none, use color cycle
        if c is None:
            color = cycle['color']
        elif len(c) > 1:
            color = c[i]
        else:
            color = c
        # use light edge for dark markers
        if np.mean(colorConverter.to_rgb(color)) < .4:
            markeredgecolor = "grey"
        else:
            markeredgecolor = "black"

        lines.append(ax.plot(x1[mask], x2[mask], markers[i], markersize=s,
                             label=labels[i], alpha=alpha, c=color,
                             markeredgewidth=markeredgewidth,
                             markeredgecolor=markeredgecolor)[0])

    if padding != 0:
        pad1 = x1.std() * padding
        pad2 = x2.std() * padding
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        ax.set_xlim(min(x1.min() - pad1, xlim[0]), max(x1.max() + pad1, xlim[1]))
        ax.set_ylim(min(x2.min() - pad2, ylim[0]), max(x2.max() + pad2, ylim[1]))

    return lines
