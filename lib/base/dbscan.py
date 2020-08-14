from sklearn.cluster import DBSCAN
#from sklearn import metrics
from sklearn.preprocessing import StandardScaler
import numpy as np

class Scan():

	def __init__(self, input_data, radius, samples, mu, sig):


		#Normalising data for a better dbscan fit
		data = []
		for i in range(len(input_data)):
			
			data_point = []
		
			for j in range(len(input_data[i])):
			
				data_point.append((input_data[i][j] - mu[j])/sig[j])
				
			data.append(data_point)
		
		data = np.array(data)
		
		#data = StandardScaler().fit_transform(input_data)
		
		#print(data)

		# #############################################################################
		# Compute DBSCAN
		db = DBSCAN(eps=radius, min_samples=samples).fit(data)

		#DBSCAN creates 2 arrays. One of all the indices of the points within clusters. The other is 
		# an array containing a label for every item.

		#This creates an array in the same shape as the label array but every item is false
		core_samples_mask = np.zeros_like(db.labels_, dtype=bool)

		#This changes the false values to true if the point is part of a cluster.
		#(and leaves it false if it is an outlier - i.e. does not appear in the index array.
		core_samples_mask[db.core_sample_indices_] = True

		#Copying the labels array for manipulation
		labels = db.labels_



		# Number of clusters in labels, ignoring noise if present.
		n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
		n_noise_ = list(labels).count(-1)

		#print('Estimated number of clusters: %d' % n_clusters_)
		#print('Estimated number of noise points: %d' % n_noise_)

		#If the cluster values are already known these scoring functions can be used.

		#print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
		#print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
		#print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
		#print("Adjusted Rand Index: %0.3f"
		#      % metrics.adjusted_rand_score(labels_true, labels))
		#print("Adjusted Mutual Information: %0.3f"
		#      % metrics.adjusted_mutual_info_score(labels_true, labels))
		#print("Silhouette Coefficient: %0.3f"
		#      % metrics.silhouette_score(X, labels))

		# #############################################################################
		# Plot result

		# Black removed and is used for noise instead.
		unique_labels = set(labels)
		#colors = [plt.cm.Spectral(each)
		#		  for each in np.linspace(0, 1, len(unique_labels))]
				  


		tilde = []
		non_tilde = []	
		outliers = []

		#This loop creates creates 3 arrays.
		# 1. The outliers in the form (No. Outliers, 1)
		# 2. An array of the cluster points from the normal core_samples_mask in the form (No. Points in cluster, No. Clusters)
		# 3. An array of the cluster points from the tilde (~) core_samples_mask in the form (No. Points in cluster, No. Clusters)

		#Usually the tilde array is empty but occasionally in sparse clusters there will be some points.
		for k in unique_labels:
			
			class_member_mask = (labels == k)
			
			if k == -1:
				outliers.append(data[class_member_mask & ~core_samples_mask])
			else:
			
				non_tilde.append(data[class_member_mask & core_samples_mask])
				
				tilde.append(data[class_member_mask & ~core_samples_mask])
			



		#This loop combines the Outliers into a single list
		outlier_holder = []

		for k in range(len(outliers)):
		
			for l in range(len(outliers[k])):
			
				outlier_holder.append(outliers[k][l])

		#The outlier list is then put inside another list so that is in the same format as Clusters
		outliers = [outlier_holder, ]
		
		
		#Finding the number of clusters present and the dimnesions of the data.
		total_clusters = len(non_tilde)
		#print('length')
		#print(non_tilde[0])
		dimensions = len(data[0])

		#Ndarray to calculate the length of each tilde and non_tilde array
		lengths = np.ndarray((total_clusters, 2), dtype = int)

		clusters = []

		#Populating Ndarray with values, becomes important as the aim is to merge the values in tilde
		# and non_tilde
		for i in range(total_clusters):

			lengths[i][0] = len(non_tilde[i])
			lengths[i][1] = len(tilde[i])
			
		#print(lengths)
			

		for p in range(total_clusters):

			#Taking the individual cluster tilde and non_tilde_values
			non_tilde_values = non_tilde[p]
			tilde_values = tilde[p]
			
			#Creating Ndarray in the form (Total no. points in the cluster, No. Dimensions)
			x = lengths[p,0] + lengths[p][1]
			y = dimensions
			
			#Create ndarray to hold the coordinates of every point in the cluster
			c = np.ndarray(shape = (x, y))
				

			#This loop populates the ndarray with all the values from non_tilde
			for i in range(lengths[p][0]):

				for j in range(dimensions):
				
					c[i][j] = non_tilde_values[i][j]
					
			#This loop then populates the ndarray with all the values from tilde
			for i in range(lengths[p][1]):
				for j in range(dimensions):
					c[i + lengths[p][0]][j] = tilde_values[i][j]

			#As c was created to be as long as len(non_tilde) + len(tilde) every index has a value
			
			#Now c contains the coordinates for every point in the cluster.
			#It now loops over every cluster to create a list of the ndarrays which hold the 
			# coordinates.
			clusters.append(c)
			
			

		self.clusters = clusters
		
		self.outliers = outliers


		
	def arrays(self):
		return self.clusters, self.outliers
		
	def get_clusters(self):
		return self.clusters

	def get_outliers(self):
		return self.outliers
	
		
		
