import mesa
import numpy as np
import scipy.cluster.hierarchy as hcluster

def compute_clusters(model, data, plot=False):
    thresh = 1.5
    clusters = hcluster.fclusterdata(data, thresh, criterion="distance")
    if plot:
        return clusters
    return len(set(clusters))


def plot_clusters(model):
    data = []
    for a in model.schedule.agents:
        data.append(list(a.pos))
    clusters = compute_clusters(model, data, True)
    plt.scatter(*np.transpose(data), c=clusters)
    plt.axis("equal")
    title = "Threshold: %f, # of clusters: %d" % (thresh, len(set(clusters)))
    plt.title(title)
    plt.show()
