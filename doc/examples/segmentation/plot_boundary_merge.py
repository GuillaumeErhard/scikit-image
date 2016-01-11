"""

"""

from skimage import data, io, segmentation, color, filters
from skimage.future import graph
import numpy as np


def attr(graph, src, dst, n):
    """Callback to handle merging nodes by recomputing mean color.

    The method expects that the mean color of `dst` is already computed.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    n : int
        A neighbor of `src` or `dst` or both.

    Returns
    -------
    weight : float
        The absolute difference of the mean color between node `dst` and `n`.
    """

    if graph.has_edge(src, n) and graph.has_edge(dst, n):
        count_src = graph[src][n]['count']
        count_dst = graph[dst][n]['count']

        weight_src = graph[src][n]['weight']
        weight_dst = graph[dst][n]['weight']

        count = count_src + count_dst
        return {
            'count':count,
            'weight':(count_src*weight_src + count_dst*weight_dst)/count
        }
    elif graph.has_edge(src, n):
        return graph[src][n]
    elif graph.has_edge(dst, n):
        return graph[dst][n]

def merge(graph, src, dst):
    """Callback called before merging two nodes of a mean color distance graph.

    This method computes the mean color of `dst`.

    Parameters
    ----------
    graph : RAG
        The graph under consideration.
    src, dst : int
        The vertices in `graph` to be merged.
    """
    pass


img = data.coffee()
labels = segmentation.slic(img, compactness=30, n_segments=400)
energy = filters.sobel(color.rgb2gray(img))
g = graph.rag_boundary(labels, energy)

labels2 = graph.merge_hierarchical(labels, g, thresh=.05, rag_copy=False,
                                   in_place_merge=True,
                                   merge_func=merge,
                                   weight_func=attr)


out = color.label2rgb(labels2, img, kind='avg')
out = segmentation.mark_boundaries(out, labels2, (0, 0, 0))
io.imshow(out)
io.show()
