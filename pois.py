import numpy as np
from math import sqrt, pi
from scipy.spatial import cKDTree

from lib.base.dbscan import Scan

#Creating output list which is the difference of two input lists
def difference(list1, list2):

	#List to hold values of list1 found in list2
	list1_indices_to_delete = []
	
	#List to hold values of list2 not found in list1
	list2_indices_to_add = []
	
	for i in range(len(list2)):
	
		match = False
	
		for j in range(len(list1)):
		
			if np.array_equal(list1[j],list2[i]):
			
				
				if j in list1_indices_to_delete:
					pass
					
				else:
					list1_indices_to_delete.append(j)
					match = True
					break
				
			
		if not match:
		
			list2_indices_to_add.append(i)
			
	list3 = []
			
	for i in range(len(list1)):
	
		if not i in list1_indices_to_delete:
			
			list3.append(list1[i])
			
	for i in range(len(list2)):
	
		if i in list2_indices_to_add:
		
			list3.append(list2[i])
			
			
		
	return list3

#Function to reverse standard scalar function
def Reverse_standard_scalar(original_data, data_to_reverse):
	
	dat = original_data.get_Combined_Data()
	
	mean = np.average(dat, 0)
	sig = np.std(dat, 0)
	
	original_coordinates = []
	
	#print(data_to_reverse)
	
	for j in range(len(data_to_reverse)):
	
		#print(data_to_reverse[j])
		for i in range(len(data_to_reverse[j])):
		
			#print(i)
		
			original_coordinates.append([(data_to_reverse[j][i][0] * sig[0]) + mean[0], (data_to_reverse[j][i][1] * sig[1]) + mean[1], (data_to_reverse[j][i][2] * sig[2]) + mean[2]])
	
	return np.array(original_coordinates)
	
	
def Reverse_standard_scalar2(original_data, data_to_reverse):
	
	dat = original_data.get_combined_data()
	
	mean = np.average(dat, 0)
	sig = np.std(dat, 0)
	
	original_coordinates = []
	
	#print(data_to_reverse)
	
	for j in range(len(data_to_reverse)):
	
		#print(data_to_reverse[j])
		original_coordinates2 = []
		
		for i in range(len(data_to_reverse[j])):
		
			#print(i)
		
			original_coordinates2.append([(data_to_reverse[j][i][0] * sig[0]) + mean[0], (data_to_reverse[j][i][1] * sig[1]) + mean[1], (data_to_reverse[j][i][2] * sig[2]) + mean[2]])
	
		original_coordinates.append(np.array(original_coordinates2))
	
	return original_coordinates
		
	
	
def Find_Outliers(cluster_data, raw_data, min_z_value, mu, sig, z):


	outliers = list(cluster_data)
	

	for i in range(len(cluster_data)):
		
		#Lists which hold the indices to be deleted
		marker1 = []
		
	
		for j in range(len(cluster_data[i])):
		
		
		
			if cluster_data[i][j][-1] < min_z_value:
			
				marker1.append(j)
			
				
	
		marker1.sort(reverse=True)

		
	
		for k in range(len(marker1)):
			
			outliers[i] = np.delete(outliers[i], marker1[k], 0)
			
			
	#print(outliers)
			
			
	indice_match = []

	
	for k in range(len(outliers)):
	
		#indices = []
		indice_match1 = []
	
		for i in range(len(outliers[k])):
		
			#indices = []
		
			array = (outliers[k][i] * sig) + mu
			
			array[2] = round(array[2], 6)
			
			found = False
		
			for j in range(len(raw_data)):
			
			
				if raw_data[j][3] == 0:
				
					com_lev_spr = 0
					
				else:
				
					com_lev_spr = round(raw_data[j][2]/raw_data[j][3], 6)
					
			
				raw_array = [raw_data[j][0], raw_data[j][1], com_lev_spr]
				
				#if i == 0:
				
					#print(raw_array)
			
				if np.array_equal(raw_array, array):
				
					#indices.append([j, [k, i]])
					
					index = j
					
					found = True
					break
					#print(indices)
					
					
			if not found:
			
				print(array)
				print([k, i])
					
			#print(red_array)
		
			indice_match1.append(index)
			
		indice_match.append(indice_match1)
			
	#print(indice_match)
	
	
	# idn = []
			
	# for i in range(len(indice_match)):
	
		# new_indice_match = []
		
		# for j in range(len(indice_match[i])):
	
			# if not indice_match[i][j] in new_indice_match:
			
				# new_indice_match.append(indice_match[i][j])
		
		# #print(new_indice_match)
		
		# idn.append(new_indice_match)
			

	
	# indice_match = idn

	#print(indice_match)

	indices_to_delete = []
	
	
	for i in range(len(indice_match)):
	
		delete_indices = []
	
		for j in range(len(indice_match[i])):
		
			#print(indice_match[i][j])
		
			#print(raw_data[indice_match[i][j]])
		
			if raw_data[indice_match[i][j]][2] < z[1]:
			
				#print([i, j])
				#print(raw_data[indice_match[i][j]])
			
				delete_indices.append(j)
				
		indices_to_delete.append(delete_indices)
	
	
	for i in range(len(indices_to_delete)):
	
		indices_to_delete[i].sort(reverse=True)
	
	
	
	
	#print(indices_to_delete)
	
	#print(outliers)
	
	for i in range(len(indices_to_delete)):
	
		for j in range(len(indices_to_delete[i])):
		
			#print(outliers)
			outliers[i] = np.delete(outliers[i], indices_to_delete[i][j], 0)
			
	#print(outliers)

	return outliers


def Halma_Data(leak_data, combined_data):

	
	#label = data.get_leak_Data()
	
	#leaks = data.get_Combined_Data()
	
	labels = []
	
	#print(label)
	
	n_leaks = 0
	
	for i in range(len(leak_data)):
	
		if leak_data[i][-1] == 'N' :
		
			labels.append(0)
			
		else:
		
			labels.append(1)
			n_leaks += 1
	
	
	halmer = []
	
	for i in range(len(combined_data)):

		if labels[i] == 1 :
	
			halmer.append(combined_data[i])

	halmer = np.array(halmer)
	
	

	return halmer


def Matrix(raw_data):


	m_data = np.array(raw_data)
	
	#print(len(m_data))

	final_data = []
	maybe_data = []
	
	indices_to_delete = []
	
	for i in range(len(m_data)):
	
		if m_data[i][2] >= 65 :
		
			final_data.append(m_data[i])
			
			indices_to_delete.append(i)
			
			
	indices_to_delete.sort(reverse=True)
			
	for i in range(len(indices_to_delete)):
	
		m_data = np.delete(m_data, indices_to_delete[i], 0)
	
	

	indices_to_delete = []
		
			
			
	for i in range(len(m_data)):
	
		if m_data[i][2] > 19 :
		
			if m_data[i][3] == 3 or m_data[i][3] == 4 :
			
				final_data.append(m_data[i])
				indices_to_delete.append(i)
				
		if m_data[i][2] > 21 and m_data[i][3] == 5:
		
			final_data.append(m_data[i])
			indices_to_delete.append(i)
			
		if m_data[i][2] > 34 and m_data[i][3] == 6:
		
			final_data.append(m_data[i])
			indices_to_delete.append(i)
			
		if m_data[i][2] > 44 and m_data[i][3] == 7:
		
			final_data.append(m_data[i])
			
			indices_to_delete.append(i)
			
			
		if m_data[i][2] == 19 :
		
			if m_data[i][3] < 2 and m_data[i][3] > 5 :
			
				maybe_data.append(m_data[i])
				
				indices_to_delete.append(i)
				
		if m_data[i][3] == 2 and m_data[i][2] > 18 and m_data[i][2] < 24 :
		
			maybe_data.append(m_data[i])
			indices_to_delete.append(i)
				
				
		if m_data[i][3] == 5 and m_data[i][2] > 19 and m_data[i][2] < 22 :
		
			maybe_data.append(m_data[i])
			indices_to_delete.append(i)
				
		if m_data[i][3] == 6 and m_data[i][2] > 21 and m_data[i][2] < 35 :
		
			maybe_data.append(m_data[i])
			indices_to_delete.append(i)
			
		if m_data[i][3] == 7 and m_data[i][2] > 34 and m_data[i][2] < 45 :
		
			maybe_data.append(m_data[i])
			indices_to_delete.append(i)
			
		if m_data[i][3] == 8 and m_data[i][2] > 44 :
		
			maybe_data.append(m_data[i])
			indices_to_delete.append(i)
		




	
	indices_to_delete.sort(reverse=True)
			
	#print(len(indices_to_delete))
	
	#print(len(m_data))
			
	for i in range(len(indices_to_delete)):
	
		#print(indices_to_delete[i])
	
		m_data = np.delete(m_data, indices_to_delete[i], 0)

	return final_data, maybe_data
	
	
def Transform_Outliers(combined_data, raw_data, tree_data, mu, sig, z, min_z_value):


	#Number of data points variable for use in the DBSCAN module
	n_points = len(combined_data)
	
	
	#Calling Scan class. See dbscan module for details
	dbscan = Scan(combined_data, 1, int(n_points/10), mu, sig)


	#Retrieving data from scan class
	Clusters, Outliers = dbscan.arrays()


	if len(Clusters) < 2:

		red_outliers = Find_Outliers(Clusters, raw_data, min_z_value, mu, sig, z)
	
		true_outliers = Find_Outliers(Outliers, raw_data, min_z_value, mu, sig, z)


	else:
		
		#print('More Clusters')
	
		indices_to_delete = []
	
		for i in range(len(Clusters)):
		
			#print(Clusters[i])
		
			avg = np.average(Clusters[i], 0)
			
			#print(avg[2])
			
			
			if avg[2] >= min_z_value and len(Clusters[i]) < n_points/3:
			
				#print('high cluster')
				#print(avg[2])
				#print(min_z_value)
				
				#print(len(Clusters[i]))
			
				for j in range(len(Clusters[i])):
				
					Outliers[0].append(Clusters[i][j])
					
				indices_to_delete.append(i)
				
		indices_to_delete.sort(reverse=True)
		
		hold_clusters = []
		
		for i in range(len(Clusters)):
		
			if not i in indices_to_delete:
			
				hold_clusters.append(Clusters[i])
			
		Clusters = hold_clusters
		
		
		red_outliers = Find_Outliers(Clusters, raw_data, min_z_value, mu, sig, z)
	
		true_outliers = Find_Outliers(Outliers, raw_data, min_z_value, mu, sig, z)


	#print([len(red_outliers), len(true_outliers)])

	# for i in range(len(red_outliers)):
	
		# for j in range(len(red_outliers[i])):
		
			# if round(red_outliers[i][j][0], 8) == round(0.700521075968413, 8) and round(red_outliers[i][j][1], 8) == round(0.22703651493618954, 8):
			
				# print('yes3')
				# print(red_outliers[i][j])


	#This section averages the level and spread ratios from logger within 'rad' meters of each other. 

	#tree_data = data.get_XY_Data()
	
	tree = cKDTree(tree_data)

	
	
	rad = 5
	#mu = data.get_mu(True)
	#sig = data.get_sigma(True)
	
	#No information is lost. The DBscan module concatenates everything.
	new_out = np.array(true_outliers[0])

	for i in range(len(true_outliers[0])):
	
		new_out[i] = ((true_outliers[0][i] * sig) + mu)


	indices_to_delete = []
	
	#This loop firstly calculates the average z value for an outlier which has other loggers within rad meters.
	#It then removes the point from the outliers list if the new z value falls below the threshold
	
	for i in range(len(new_out)):
	
		point = [new_out[i][0], new_out[i][1]]
		
		neighbours = tree.query_ball_point(point, rad)
		
		if len(neighbours) > 1 :
			
			new_z_value = 0
			
			for j in range(len(neighbours)):
			
				new_z_value += combined_data[neighbours[j]][2]
			
			
			new_z_value = new_z_value/len(neighbours)
			
			
			if new_z_value < min_z_value*sig[2] + mu[2]:
			
				#true_outliers[0][i][2] = new_z_value
			
				#false_outliers[0] = np.append(false_outliers[0], [true_outliers[0][i]], 0)
				
				indices_to_delete.append(i)
				
				
			#elif new_z_value >= min_z_value :
				
				#true_outliers[0][i][2] = new_z_value
				
				

	
	new_red = []
	hold_red = []

	#This loop reverts the normalised values of red_outliers to physical cooridnates.
	#As the KDTree used the un_normalised data is it necessary to change to physical space
	#The KDTree was created in the physical space as the x and y in normal space are changed
	# by different amounts.
	#Finding neighbours in physical space allows for the radius to be real world measurements
	#When using Eastings and Northings the radius will be in meters
	for i in range(len(red_outliers)):
	
		hold_red = []
	
		for j in range(len(red_outliers[i])):

			un_normalised_red_outliers = np.array((red_outliers[i][j] * sig) + mu)
			
			hold_red.append(un_normalised_red_outliers)
			
		new_red.append(np.array(hold_red))
	
	
	
	red_indices_to_delete = []
	
	#This loop firstly calculates the average z value for a red outlier which has other loggers within rad meters.
	#It then removes the point from the outliers list if the new z value falls below the threshold
	
	#print('red before %s' %len(new_red))
	
	for i in range(len(new_red)):
		
	
		for j in range(len(new_red[i])):
	
			point = [new_red[i][j][0], new_red[i][j][1]]
			
			neighbours = tree.query_ball_point(point, rad)
			
			# if point[0] == 295488 and point[1] == 664680:
			
				# print(neighbours)
			
			if len(neighbours) > 1 :
				
				new_z_value = 0
				
				
				for k in range(len(neighbours)):
				
					new_z_value += combined_data[neighbours[k]][2]
					
					# if point[0] == 295488 and point[1] == 664680:
			
						# print(combined_data[neighbours[k]])
				
				
				new_z_value = new_z_value/len(neighbours)
				
				# if point[0] == 295488 and point[1] == 664680:
			
					# print(new_z_value)
					# print(min_z_value*sig[2] + mu[2])
				
				
				if new_z_value < min_z_value*sig[2] + mu[2]:
				
					#red_outliers[i][j][2] = new_z_value
				
					#false_outliers[0] = np.append(false_outliers[0], [red_outliers[i][j]], 0)
					
					red_indices_to_delete.append([i, j])
					
					
				#elif new_z_value >= min_z_value :
					
					
					#red_outliers[i][j][2] = new_z_value
					
					#print(red_outliers)
				
				
	
	indices_to_delete.sort(reverse=True)
	
	#print(red_indices_to_delete)
	
	red_indices_to_delete.sort(reverse=True)
	
	#print(red_indices_to_delete)
	
	#print('indices = %s' %indices_to_delete)
	
	#print('black before %s' %len(true_outliers[0]))
	
	for i in range(len(indices_to_delete)):
	
		true_outliers[0] = np.delete(true_outliers[0], indices_to_delete[i], 0)
		
	#print('black after %s' %len(true_outliers[0]))
	
	
	# lenght = 0
	
	# for i in range(len(red_outliers)):
	
		# lenght += len(red_outliers[i])
	
	# print('red before %s' %lenght)
	
	# for i in range(len(red_outliers)):
	
		# for j in range(len(red_outliers[i])):
		
			# if round(red_outliers[i][j][0], 8) == round(0.700521075968413, 8) and round(red_outliers[i][j][1], 8) == round(0.22703651493618954, 8):
			
				# print('yes')
				# print(red_outliers[i][j])
	
	for i in range(len(red_outliers)):
		for j in range(len(red_indices_to_delete)):
	
			if i == red_indices_to_delete[j][0] :
			
				red_outliers[i] = np.delete(red_outliers[i], red_indices_to_delete[j][1], 0)
		
	# lenght = 0
	
	# for i in range(len(red_outliers)):
	
		# for j in range(len(red_outliers[i])):
		
			# if round(red_outliers[i][j][0], 8) == round(0.700521075968413, 8) and round(red_outliers[i][j][1], 8) == round(0.22703651493618954, 8):
			
				# print('yes2')
				# print(red_outliers[i][j])
	
	# print('red after %s' %lenght)
	
	
	POIs = []
	
	for i in range(len(true_outliers)):
	
		for j in range(len(true_outliers[i])):
		
			POIs.append(true_outliers[i][j])
			
	for i in range(len(red_outliers)):
	
		for j in range(len(red_outliers[i])):
		
			POIs.append(red_outliers[i][j])
	
	
	
	return true_outliers, red_outliers, POIs



def Remove_Plastic(logger_info, data_to_check):


	plastic_loggers = []
	
	for i in range(len(logger_info)):
	
		if logger_info[i][1] == 'Plastic':
		
			plastic_loggers.append(logger_info[i][0])
			
			
	indices_to_delete = []
			
	for i in range(len(data_to_check)):
	
		xy = [data_to_check[i][0], data_to_check[i][1]]
		
		if xy in plastic_loggers:
		
			indices_to_delete.append(i)

	indices_to_delete.sort(reverse=True)

	for i in range(len(indices_to_delete)):

		data_to_check = np.delete(data_to_check, indices_to_delete[i], 0)
		
	return data_to_check
	
	
def Plastic_Outliers(raw_data, logger_info, z, min_z_value):

	plastic_POIs = []
	plastic_loggers = []
	
	for i in range(len(logger_info)):
	
		if logger_info[i][1] == 'Plastic':
		
			#plastic_loggers.append(logger_info[i][0])
			
			ratio = raw_data[i][2]/raw_data[i][3]
			
			
			if raw_data[i][2] >= z[1] and ratio >= min_z_value:
			
				plastic_POIs.append([raw_data[i][0], raw_data[i][1], ratio])

	
	return plastic_POIs





#This class finds the points of interest from a set of data

class POIs():

	def __init__(self, dma_id, node_info, database):
	
	
	
	
	
	
 		#Try to get node_info working with automatic threshold change
		#Get rid of output dropdowns
	

		#Getting data from database 
		data = database
		
		raw_data = data.get_data()

		#Getting combined level and spread data from database
		combined_data = np.array(data.get_combined_data())
		
		xy_data = data.get_xy_data()
		
		leak_data = data.get_leak_data()
		
		
		
		
		duplicate_list = []
		
		for i in range(len(combined_data)):
		
			duplicates = []
		
			for j in range(len(combined_data)):
			
				if np.array_equal(combined_data[i], combined_data[j]):
				
					duplicates.append(j)
			
			if len(duplicates) > 1:
			
				if not duplicates in duplicate_list:
					
					duplicate_list.append(duplicates)
				
				
				
		#print(duplicate_list)
		
		point_to_change_list = []
		
		for i in range(len(duplicate_list)):
		
			point_to_change = []
			
			skip = []
		
			for j in range(len(duplicate_list[i])):
			
				k = j
			
				while k <= len(duplicate_list[i]) - 1:
		
					if j != k:
						
						if not k in skip and not j in skip:
						
							if raw_data[duplicate_list[i][j]][2] != raw_data[duplicate_list[i][k]][2]:
			
			
								point_to_change.append(duplicate_list[i][k])
							
							else:
							
								skip.append(k)
		
					k += 1		
				
			if len(point_to_change) > 0:
				
				point_to_change_list.append(point_to_change)
		
		
		#print(point_to_change_list)
		
		for i in range(len(point_to_change_list)):
		
			for j in range(len(point_to_change_list[i])):
			
				raw_data[point_to_change_list[i][j]] = [raw_data[point_to_change_list[i][j]][0] + 0.000001, raw_data[point_to_change_list[i][j]][1], raw_data[point_to_change_list[i][j]][2], raw_data[point_to_change_list[i][j]][3]]
				
				#raw_data[point_to_change_list[i][j]][0] = raw_data[point_to_change_list[i][j]][0] + 0.001
				
				
				combined_data[point_to_change_list[i][j]] = [combined_data[point_to_change_list[i][j]][0] + 0.000001, combined_data[point_to_change_list[i][j]][1], combined_data[point_to_change_list[i][j]][2]]
		
				xy_data[point_to_change_list[i][j]] = [xy_data[point_to_change_list[i][j]][0] + 0.000001, xy_data[point_to_change_list[i][j]][1]]
		
				leak_data[point_to_change_list[i][j]] = [float(leak_data[point_to_change_list[i][j]][0]) + 0.000001, leak_data[point_to_change_list[i][j]][1], leak_data[point_to_change_list[i][j]][2]]
		
		
		
		#print(raw_data[159])
		
		
		#if raw_data[159][0] == 295573:
		
		#	print('yes')
		
		#sys.exit()
				
				
				
				
		
		#normal = data.normalise_data(combined_data)

		#Number of data points variable for use in the DBSCAN module
		n_points = len(combined_data)
		
		#print(n_points)

		#Calculating the average (mu) and standard deviation (sig) of the imported data
		mu = data.get_mu(True)
		sig = data.get_sigma(True)
		
		#print([(295488 - mu[0])/sig[0], (664680 - mu[1])/sig[1]])


		
		halmer_data = Halma_Data(leak_data, combined_data)
		
		final_data, maybe_data = Matrix(raw_data)
		
		
		
		node_xy = []
		node_material = []
	
	
		for i in range(len(node_info)):
		
			node_xy.append(node_info[i][1])
			node_material.append(node_info[i][2])
		
		
		
		
		node_tree = cKDTree(node_xy)
		
		data_xy = []
		
		for i in range(len(raw_data)):
		
			data_xy.append([raw_data[i][0], raw_data[i][1]])
			
			
		node_dist, node_index = node_tree.query(data_xy)
		
		logger_info = []
		normalised_logger_info = []
		
		for i in range(len(raw_data)):
		
			logger_info.append([data_xy[i], node_material[node_index[i]]])
			normalised_logger_info.append([[(data_xy[i][0]-mu[0])/sig[0], (data_xy[i][1]-mu[1])/sig[1]], node_material[node_index[i]]])
		
		
		#print(np.array(logger_info))
		
		
		
		
		
		
		
		#raw_data = data.get_Data()
		
		expected_n_pois = round(n_points/4)
		
		if expected_n_pois < 1:
		
			expected_n_pois = 1
		
		n_pois = 0
		
		ratio_factor = 0.90
		level_factor = 0.95
		
		plastic_ratio = 0.85
		plastic_level = 0.85
		
		
		true_outliers_list = []
		red_outliers_list = []
		plastic_outliers_list = []
		boundary_valve_list = []
		#print(z)
		#print(min_z_value)
		
		#print(expected_n_pois)

		
		while n_pois < expected_n_pois:
		
		
			#Variable to analyse all data held in the database and return an array of the values which marks the top x% of the data
			#See database module for details
			z = data.get_min_z(ratio_factor)
			
			
			#Normalising using same process standard scalar uses 
			min_z_value = (z[0] - mu[2])/sig[2]
			
			#Reassigning variable to get another z[1]  
			z = data.get_min_z(level_factor)
		
		
			plastic_min_z = data.get_min_z(plastic_ratio)[0]
			plastic_z = data.get_min_z(plastic_level)
		
			#print('ratio: %s, level: %s' %(plastic_min_z, plastic_z[1]))

			
			true_outliers, red_outliers, POIs = Transform_Outliers(combined_data, raw_data, xy_data, mu, sig, z, min_z_value)
			
			
			#n_red = 0
			#n_true = 0
			
			combined_red_array = []
			combined_true_array =[]
			
			for i in range(len(red_outliers)):
			
				#n_red += len(red_outliers[i])
				
				for j in range(len(red_outliers[i])):
				
					combined_red_array.append(red_outliers[i][j])
			
			for i in range(len(true_outliers)):
			
				#n_true += len(true_outliers[i])
			
				for j in range(len(true_outliers[i])):
				
					combined_true_array.append(true_outliers[i][j])
			
			
			#print(np.array(combined_true_array))
			
			
			combined_true_array = np.array(combined_true_array)
			combined_red_array = np.array(combined_red_array)
			
			#print(data.get_min_z(ratio_factor)[0], data.get_min_z(ratio_factor)[1])
			#print(combined_red_array)
			
			
			combined_true_array = Remove_Plastic(normalised_logger_info, combined_true_array)
			combined_red_array = Remove_Plastic(normalised_logger_info, combined_red_array)
			
			
			
			plastic_outliers = Plastic_Outliers(raw_data, logger_info, plastic_z, plastic_min_z)
			
			
			
			
			n_pois = len(combined_true_array) + len(combined_red_array) + len(plastic_outliers)
			
			true_outliers_list.append(combined_true_array)
			red_outliers_list.append(combined_red_array)
			plastic_outliers_list.append(plastic_outliers)
			
			
			#print(red_outliers)
			#print(n_pois)
			#print(ratio_factor)
			
			ratio_factor -= 0.05
			level_factor -= 0.05
			
			plastic_ratio -= 0.05
			plastic_level -= 0.05
			
			if len(true_outliers_list) >= 6:
			
				break
			
			
		#sys.exit()
		#print(n_pois)

		
		true_quality_array = []
		red_quality_array = []
		plastic_qualtiy_array = []
		
		for i in range(len(true_outliers_list)):
		
			true_quality_array.append([])
			red_quality_array.append([])
			plastic_qualtiy_array.append([])
		
		
		
		j = len(true_quality_array)-1
		
		
		for i in range(len(true_quality_array)):
		
			if i == j:
				
				true_quality_array[j - i] = true_outliers_list[0]
				red_quality_array[j - i] = red_outliers_list[0]
				plastic_qualtiy_array[j - i] = plastic_outliers_list[0]
		
		
		
			else:
				
				true_quality_array[j - i] = difference(true_outliers_list[j-i], true_outliers_list[j-(i+1)])
				red_quality_array[j - i] = difference(red_outliers_list[j-i], red_outliers_list[j-(i+1)])
				plastic_qualtiy_array[j - i] = difference(plastic_outliers_list[j-i], plastic_outliers_list[j-(i+1)])
		
		#print(np.array(quality_array))
		
		#print(plastic_qualtiy_array)
		#for i in range(len(quality_array)):
		
		#	for j in range(len(quality_array[i])):
			
		true_outliers = Reverse_standard_scalar2(data, true_quality_array)
		red_outliers = Reverse_standard_scalar2(data, red_quality_array)

		#print(test)
		
			
		#sys.exit()
			
			



		#####################################################################################################
		
		#Confidence calculating

		#####################################################################################################


		all_data = data.get_data()
		
		
		#p_space_true_outliers = Reverse_standard_scalar(data, true_outliers)
		#p_space_red_outliers = Reverse_standard_scalar(data, red_outliers)
		#p_space_prv_POIs = Reverse_standard_scalar(data, [prv_POIs])
		#p_space_halmer = halmer_data

		
		data_points = []
		confidence = 0
		distance = []
		#material = 0

		
		for i in range(len(all_data)):
			
			if all_data[i][3] == 0:
			
				ratio = 0
				
			else:
			
				ratio = all_data[i][2]/all_data[i][3]
				
			profile = "" + str(all_data[i][2]) + '/' + str(all_data[i][3])

			data_points.append([all_data[i][0], all_data[i][1], ratio, confidence, [], profile, logger_info[i][1]])
				
			

		#total_points = [len(true_outliers, len(red_outliers), len([p_space_halmer]), len([final_data]), len([maybe_data])]
		
		#print(red_outliers)
		
		
		combined_POIs = [true_outliers, red_outliers, [halmer_data, final_data, maybe_data], plastic_qualtiy_array]
		
		values = [[6.1, 5.1, 4.1, 3.1, 2.1, 1.1], [5.2, 4.2, 3.2, 2.2, 2.2, 1.2], [1, 6, 3], [6.3, 5.3, 4.3, 3.3, 2.3, 1.3]]

		test = True
		#print(red_outliers)
		
		for i in range(len(combined_POIs)):
		
		
			for l in range(len(combined_POIs[i])):
		
				indices = np.arange(len(combined_POIs[i][l]))
		
				visited_list = []
		
				for j in range(len(indices)):
				
					#combine = True
				
					try:
						POI_point = [combined_POIs[i][l][indices[j]][0], combined_POIs[i][l][indices[j]][1], round(combined_POIs[i][l][indices[j]][2]/combined_POIs[i][l][indices[j]][3], 6)]
					
					except IndexError:
						POI_point = [combined_POIs[i][l][indices[j]][0], combined_POIs[i][l][indices[j]][1], round(combined_POIs[i][l][indices[j]][2], 6)]
						#combine = False
					#POI_point = [combined_POIs[i][l][indices[j]][0], combined_POIs[i][l][indices[j]][1]]
					
					#print(POI_point)
					
					index = []
				
					for k in range(len(all_data)):
					
						#if combine:
						data_point = [all_data[k][0], all_data[k][1], round(all_data[k][2]/all_data[k][3], 6)]
					
						#else:
							#data_point = [all_data[k][0], all_data[k][1], all_data[k][2]]
						#data_point = [all_data[k][0], all_data[k][1]]
						
						#if test:
						#	print(data_point)
						
						if np.array_equal(POI_point, data_point) :
							
							#if test:
							#	print('yep')
							#	test = False
							index.append([k, all_data[k][2]])
					
					
					
					index = sorted(index, key = lambda index:index[1], reverse=True)
					
					
					if len(index) > 1 :
						
						for m in range(len(index)):

						
							if not index[m][0] in visited_list:
						
								
								data_points[index[m][0]][3] += round(values[i][l])
								
								data_points[index[m][0]][4].append(values[i][l])
								
								visited_list.append(index[m][0])


					elif len(index) == 1:
					
						data_points[index[0][0]][3] += round(values[i][l])
						
						data_points[index[0][0]][4].append(values[i][l])

						
					

		#print('\nnewcount\n')
		cou = 0
					
		for i in range(len(data_points)):
		
			if data_points[i][3] > 10 :
						
				data_points[i][3] = 10
		
		if data_points[i][3] >= 1 :
			
				cou += 1


		#print('\nTotal POIs = %s\n' %cou)


		self.data_points = data_points
		
		#print(np.array(data_points))
		
		# for i in range(len(data_points)):
		
			# if data_points[i][0] == 295587:
			
				# print(data_points[i])
		
		
		#sys.exit()
		
		
	def get_algorithm_data(self):

		return self.data_points
	
	
	
	
	



