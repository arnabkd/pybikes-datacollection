from sklearn.cluster import MeanShift
import numpy as np, time, random

size = 1000

data_x = [random.randint(7,24) for x in range(size)]
data_y = [random.randint(0,100) for y in range(size)]
data_z = [random.randint(0,10) for z in range(size)]
X = np.array(zip(data_x,data_y,data_z))


t0 = time.time()
ms = MeanShift().fit(X)
t1 = time.time()

print str(t1-t0), "seconds"
labels = ms.labels_
print set(labels)

cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)
#print cluster_centers
###############################################################################
# Plot result

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
x = [t[0] for t in cluster_centers]
y = [t[1] for t in cluster_centers]
z = [t[2] for t in cluster_centers]

print cluster_centers

#ax.plot_wireframe(x,y,z, rstride=1, cstride=1)

ax.scatter(x, y, z, c='b', marker='^')

#for (x,y,z) in cluster_centers:
#  print x,y,z

plt.show()


"""
import pylab as pl
from itertools import cycle

pl.figure(1)
pl.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    pl.plot(X[my_members, 0], X[my_members, 1], X[my_members, 2], col + '.')
    pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=14)
pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()

"""