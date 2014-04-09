
from numpy import array
from pylab import plot, show, axis
from scipy.cluster.vq import vq, kmeans, std

features = array([[8,1,70], [8,1,80], [8,2,90], [8,5,30], [8,4,40], [16,1,30], [16,2,50], [16,4,70], [16,5,80]])

#def read_data_from_bike_data(srcDir):
  #return features

#def whiten(obs):
  #return obs / std(obs)

#whitened = whiten(read_data_from_bike_data("../testdata/"))

centroids, distortion = kmeans(features, 3, iter=1000)
idx, distortion = vq(features, centroids)

plot(features[idx==0,0],features[idx==0,1],'ob',
     features[idx==1,0],features[idx==1,1],'or',
     features[idx==2,0],features[idx==2,1],'og') # third cluster points  
                  
plot(centroids[:,0],centroids[:,1],'sm',markersize=3)
axis([30, 30, 30, 30])
show() 

 
""""
import numpy
import matplotlib
matplotlib.use('Agg')
from scipy.cluster.vq import *
from pylab import scatter, plot, show
#pylab.close()
 
features = numpy.array([[8,1,70], [8,1,80], [8,2,90], [8,5,30], [8,4,40], [16,1,30], [16,2,50], [16,4,70], [16,5,80]])
 
# kmeans for 3 clusters
centroids, idx = kmeans(features,2, iter=10000)

#print res,idx
#print centroids

plot(centroids[:,0],centroids[:,1],'sm',markersize=8)
show() 
 
#colors = ([([0.4,1,0.4],[1,0.4,0.4],[0.1,0.8,1])[i] for i in idx])
 
# plot colored points
#scatter(xy[:,0],xy[:,1], c=colors)
 
# mark centroids as (X)
#scatter(res[:,0],res[:,1], marker='o', s = 500, linewidths=2, c='none')
#scatter(res[:,0],res[:,1], marker='x', s = 500, linewidths=2)

#pylab.savefig('/Users/arnab/test.png')"""