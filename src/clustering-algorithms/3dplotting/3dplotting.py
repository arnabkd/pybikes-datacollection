from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random
from scipy.cluster.vq import kmeans,vq
import numpy


fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

size = 40000
X = [random.randint(0,24) for x in range(size)]
Y = [random.random()*4 for y in range(size)]
Z = [random.random()*100 for z in range(size)]
#data = numpy.array([X,Y,Z])

print X[0], Y[0], Z[0]
#print max(X)
#print max(Y)
#print Z
ax.scatter(X,Y,Z, c = 'r', marker = 'o')

#Compute k-means with k=3
#centroids,_  = kmeans(data, 3, iter=10000)

#assign samples to clusters
#idx,_ = vq(data,centroids)

#plt.plot(data[idx==0,0], data[idx==0,1], 'ob', data[idx==1,0], data[idx==1,1],'or', data[idx==2,0], data[idx==2,1], 'og')
#plt.plot(centroids[:,0], centroids[:,1],'sm', markersize=8)

ax.set_xlabel('Time of day') 
ax.set_ylabel('Bike available percentage') 
ax.set_zlabel('Distance from city center (km)') 




plt.show()
