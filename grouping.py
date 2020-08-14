import geopandas as gpd

import pandas as pd
import numpy as np
import networkx as nx
from math import sqrt
from scipy.spatial import cKDTree
import sys

import shapely.geometry as sh
import lib.base.vectors as vector


#from data_sanitation_module import data_check

#Function for converting material ids from the shape file
def mains_material_convert(x):  
    if x==5:  
        return 'DI'  
    elif x==10:  
        return 'CI'  
    elif x==12:  
        return 'DIL'  
    elif x==13:  
        return 'CIL'
    elif x==15:  
        return 'SI'
    elif x==20:  
        return 'ST'
    elif x==25:  
        return 'GS'
    elif x==30:  
        return 'CU'
    elif x==35:  
        return 'PB'
    elif x==40:  
        return 'AC'
    elif x==45:  
        return 'PSC'
    elif x==50:  
        return 'GRP'
    elif x==55:  
        return 'uPVC'
    elif x==56:  
        return 'PVCU'
    elif x==57:  
        return 'PVC'
    elif x==60:  
        return 'POLY'
    elif x==65:  
        return 'AK'
    elif x==70:  
        return 'MDPE'
    elif x==75:  
        return 'HDPE'
    elif x==80:  
        return 'HPPE'
    elif x==85:  
        return 'FC'
    elif x==90:  
        return 'RC'
    elif x==95:  
        return 'HEP30'
    elif x==100:  
        return 'L'
    elif x==105:  
        return 'BR'
    elif x==110:  
        return 'MOPVC'
    elif x==115:  
        return 'P'
    elif x==120:  
        return 'GI'
    elif x==125:  
        return 'PC'
    elif x==135:  
        return 'FAHDPE'
    elif x==150:  
        return 'IB'
    elif x==160:  
        return 'SPC'
    elif x==165:  
        return 'MAC-Reg'
    elif x==167:  
        return 'MAC-Ran'
    elif x==170:  
        return 'RC'
    elif x==175:  
        return 'CONC'
    elif x==200:  
        return 'Other'
    elif x==210:  
        return 'Unknown'
    elif x==215:  
        return 'TPL'
    elif x==220:  
        return 'Puritan'
    elif x==0:  
        return 'Null'
    else:  
        return x 


#Function to test whether a section of main is plastic
def is_plastic(x):

	#Plastic types
	plastic_list = ['AK', 'HDPE', 'HPPE', 'MDPE', 'POLY', 'Puritan', 'PVC', 'PVCU', 'uPVC']

	plastic = False

	if x in plastic_list:
	
		plastic = True
		
	return plastic


#Function to test whether a section of main is metallic	
def is_metallic(x):
		
	#Metallic types
	metallic_list = ['CI', 'CU', 'DI', 'DIL', 'SI', 'ST']
	
	metallic = False
		
	if x in metallic_list:
	
		metallic = True
		
	return metallic	
	
	
#Function for converting operation ids from the shape file
def operation_convert(x):  
    if x==10:  
        return 'Proposed'  
    elif x==11:  
        return 'Planned'  
    elif x==20:  
        return 'Accepted'  
    elif x==21:  
        return 'Adopted'
    elif x==30:  
        return 'In Use'
    elif x==40:  
        return 'Isolated'
    elif x==50:  
        return 'Abandoned'
    elif x==51:  
        return 'Removed'
    elif x==60:  
        return 'Unknown'
    elif x==61:  
        return 'Not Applicable'
    elif x==9999:  
        return 0
    elif x==0:  
        return ''
    else:  
        return x 	


#Function to test whether section of main is operational
def is_operational(x):

	#Types of non operation
	operation_list = ['Proposed', 'Planned', 'Abandoned', 'Removed', 'Not Applicable']
	
	operational = True
	
	if x in operation_list:
	
		operational = False
		
	return operational


#Function for calculating the distance between 2 points
def distance(point_a, point_b):

	dist = sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)
	
	return dist
	


	
#This class is used to group POIs using a mathematical graph of water mains information

class Grouper():

	def __init__(self, dma_id, checker):

		#Location of Mains .shp file
		mains_file = r'.shp\Mains\Mains.shp'

		#database = database_data(dma_id)
		
		
		#checker = data_check(dma_id)

		dma_outline = checker.get_polygon().buffer(10)
		
		poly = checker.get_polygon()
		
		extent = poly.bounds

		#new_data_points = database.get_Data()
		
		
		
		
		
		
		print('\nReading Shape File')
		
		
		
		
		
		
		
		data = gpd.read_file(mains_file, dma_outline)

		#print(data)


		#dma = data['associated'].tolist()
		

		df = pd.DataFrame(data)

		geo = df#.loc[lambda df: df['associated'] == '%s / %s' %(dma_id, name)]

		#df.to_csv(r'C:\Users\ochambers\Documents\Leakage\Mains_Output.csv', index = False)

		line_strings = geo['geometry'].tolist()
		
		material_list = geo['material'].tolist()
		operation = geo['operationa'].tolist()


		#print(line_strings[0])

		node_list = []
		node_material = []
		
		plastic_nodes = []
		metallic_nodes = []
		other_nodes = []

		#print([min_x, min_y])
		#print([max_x, max_y])


		a = 0
		c = 0

		for i in range(len(line_strings)):
		
		
			if is_plastic(mains_material_convert(material_list[i])):
			
				material = 'Plastic'
				
			elif is_metallic(mains_material_convert(material_list[i])):
			
				material = 'Metallic'
				
			else:
			
				material = 'Other'
		

			j = 0

			line = np.array(list(line_strings[i].coords))
			
			#if i == 9:
			#	print(line)
			
			if is_operational(operation_convert(operation[i])): 
			
				while j < len(line):
				
					if not checker.check_point(line[j], 10):
					#if line[j][0] > max_x or line[j][0] < min_x:
					
						line = np.delete(line, j, 0)
						
						a += 1
						c += 1
						
					else:
					
						j += 1
						c += 1
						
				#if i == 9:
				#	print(line)

				node_list.append(line)
				node_material.append(material)
				
				if material == 'Plastic':
				
					plastic_nodes.append(line)
					
				if material == 'Metallic':
				
					metallic_nodes.append(line)
					
				if material == 'Other':
				
					other_nodes.append(line)

		nodes = node_list

		#print(c)
		#print(a)
		#print(len(nodes))

		#sys.exit()

		string_list = []
		plastic_string_list = []
		metallic_string_list = []
		other_string_list = []

		for i in range(len(nodes)):
			
			if len(nodes[i]) >= 2:
			
				string_list.append(sh.LineString(tuple(map(tuple, nodes[i]))))
			
			
		for i in range(len(plastic_nodes)):
			
			if len(plastic_nodes[i]) >= 2:
			
				plastic_string_list.append(sh.LineString(tuple(map(tuple, plastic_nodes[i]))))
				
				
		for i in range(len(metallic_nodes)):
			
			if len(metallic_nodes[i]) >= 2:
			
				metallic_string_list.append(sh.LineString(tuple(map(tuple, metallic_nodes[i]))))
				
		for i in range(len(other_nodes)):
			
			if len(other_nodes[i]) >= 2:
			
				other_string_list.append(sh.LineString(tuple(map(tuple, other_nodes[i]))))
			
		#print(string_list[0])

		#print(len(nodes[0]))
		#print(len(nodes[1]))


		All_nodes = {'geometry' : string_list}
		
		plastic_data = {'geometry' : plastic_string_list}
		metallic_data = {'geometry' : metallic_string_list}
		other_data = {'geometry' : other_string_list}


		frame = pd.DataFrame(data = All_nodes)

		geo = gpd.GeoDataFrame(frame)
		
		
		# map_stringa = Map_Strings()
		
		# map_string_list = map_stringa.get_map_strings(extent)
		
		# print(map_string_list)
		
		# folder = r'C:\Users\ochambers\Documents\Leakage\Shape Files\Map\Tiff'
		
		
		# fig = plt.figure(1, figsize = (6.4, 3.6))
		# ax = fig.add_subplot()
		
			
		# for i in range(len(map_string_list)):
		
			# letters = map_string_list[i][0] + map_string_list[i][1]
			
			# file = folder + '\\' + letters + '\\' + map_string_list[i] + '.tif'
			
			
			# my_image = georaster.SingleBandRaster(file)
			
			
			# img=plt.imread(file)
			
			# #print(file)
			
			# plt.imshow(img, extent=my_image.extent, alpha = 0.6)
		
		
		
		
		
		
		
		
		self.p_geo = gpd.GeoDataFrame(pd.DataFrame(data = plastic_data))#.plot(ax = ax, color = 'xkcd:light blue')
		self.m_geo = gpd.GeoDataFrame(pd.DataFrame(data = metallic_data))#.plot(ax = ax, color = 'blue')
		self.o_geo = gpd.GeoDataFrame(pd.DataFrame(data = other_data))#.plot(ax = ax, color = 'black')

		# ax.scatter(address_xy[:,0], address_xy[:,1], s = 2, color = 'black')
		
		
		# for i in range(len(valve_info)):
		
		
			# valve_marker = MarkerStyle("s")
			# valve_marker._transform.scale(1, 3)
			# valve_marker._transform.rotate_deg(valve_info[i][4])
		
			# ax.scatter(valve_info[i][0], valve_info[i][1], s = 10, marker = valve_marker, color = 'pink', edgecolors = 'k')
		
		print('Building Graph')

		k = 0
		old_k = 0

		G = nx.Graph()

		linestring_complete = True

		repeated = False

		points = []

		#print(nodes[0][0])

		c = 0

		for i in range(len(nodes)):

			for j in range(len(nodes[i])):
			
			
				for l in range(len(points)):

					if np.array_equal(nodes[i][j], points[l][1]):
					
						repeated = True
						
						repeated_index = l
						

				
				if repeated == False:
				
					
				
					points.append([k, nodes[i][j], node_material[i]])
				
					if linestring_complete == True:
					
						G.add_node(k)
						
						linestring_complete = False
				
					else:
					
						G.add_node(k)
						G.add_edge(k, old_k, weight = distance(points[k][1], points[old_k][1]))
						#print([k, old_k])
						
						
					old_k = k
					k += 1

				else:
				
					if linestring_complete == False:
					
					
						G.add_edge(repeated_index, old_k, weight = distance(points[repeated_index][1], points[old_k][1]))
						
						old_k = repeated_index
					
					else:
				
						old_k = repeated_index
						
						linestring_complete = False
					#k += 1
				
				c += 1

				repeated = False

			linestring_complete = True
			
			
		
		#self.checker = checker
		
		self.dma_id = dma_id

		self.G = G
		self.points = points
		
		#self.address_data = address_data
		
		self.poly = poly
		

		
		
	def get_node_info(self):
	
		return self.points


	def analyse_pois(self, algorithm_data, new_data_points, address_data, bv_data):
	
		points = self.points
		G = self.G
		
		#address_data = self.address_data
		
		
		
		
		
		
		print('Analysing POIs')

		node_xy_coords = []
		
		#print(points)

		for i in range(len(points)):

			node_xy_coords.append([points[i][1][0], points[i][1][1]])


		node_tree = cKDTree(node_xy_coords)
		
		
		
		bv_xy = []
		
		for i in range(len(bv_data)):
		
			bv_xy.append([bv_data[i][0], bv_data[i][1]])
		
		bv_tree = cKDTree(bv_xy)
		
		
		dist, bv_nearest_node_index = node_tree.query(bv_xy)
		
		
		
		
		

		#algorithm_data = POIs(dma_id).get_algorithm_data()

		algorithm_pois = []


		algorithm_xy = []

		for i in range(len(algorithm_data)):

			algorithm_xy.append([algorithm_data[i][0], algorithm_data[i][1]])

		
		dist, nearest_node_index = node_tree.query(algorithm_xy)


		for i in range(len(nearest_node_index)):
			
			algorithm_data[i].append(nearest_node_index[i])
			
			
			
			
		for i in range(len(algorithm_data)):
		
			algorithm_point = [algorithm_data[i][0], algorithm_data[i][1]]
		
			bv_neighbours = bv_tree.query_ball_point(algorithm_point, 25)
			
			
			add_bv_factor = False
			
			for j in range(len(bv_neighbours)):
			
				try:
					path = nx.shortest_path(G, source = algorithm_data[i][7], target = bv_nearest_node_index[bv_neighbours[j]], weight = 'weights')
				
				except nx.exception.NetworkXNoPath:
					pass
					#print('nope')
				
				else:
		
					path_length = 0
					
					for j in range(len(path)-1):
					
						path_length += distance(node_xy_coords[path[j]], node_xy_coords[path[j+1]])
						
						#print(path_length)
						
						if path_length > 25:
							
							break
		
					if path_length <= 25:
					
						add_bv_factor = True
						
			if add_bv_factor:
			
				#print('yes')
			
				ratio = algorithm_data[i][5].split('/')
				
				level = int(ratio[0])
				spread = int(ratio[1])
			
				if algorithm_data[i][6] == 'Plastic':
				
					if level >= 9 and level/spread >= 1.5:
			
						algorithm_data[i][3] += 3
						
						if algorithm_data[i][3] > 10:
							algorithm_data[i][3] = 10

				else:
				
					if level >= 11 and level/spread >= 1.66666666666667:
			
						algorithm_data[i][3] += 3
						
						if algorithm_data[i][3] > 10:
							algorithm_data[i][3] = 10

				

		poi_index = []

		for i in range(len(algorithm_data)):
		
			if algorithm_data[i][3] >= 1:
			
				algorithm_pois.append(list(algorithm_data[i]))
		
				poi_index.append([len(poi_index), algorithm_xy[i], nearest_node_index[i]])



		#print(len(poi_index))



		algorithm_poi_xy = []
		algorithm_normal_xy = []

		for i in range(len(algorithm_data)):

			if algorithm_data[i][3] >= 1:

				algorithm_poi_xy.append([algorithm_data[i][0], algorithm_data[i][1]])
				
			if algorithm_data[i][3] == 0:
			
				algorithm_normal_xy.append([algorithm_data[i][0], algorithm_data[i][1]])


		#print(algorithm_poi_xy)

		if len(algorithm_poi_xy) > 0:

			algorithm_poi_tree = cKDTree(algorithm_poi_xy)

			algorithm_normal_tree = cKDTree(algorithm_normal_xy)



		poi_rad = 100
		main_rad = 5

		logger_neighbours = []

		#print(len(algorithm_pois))
		#print(len(poi_index))

		for i in range(len(algorithm_pois)):

			
			neighbours = algorithm_poi_tree.query_ball_point(algorithm_poi_xy[i], poi_rad)
			
			#if i == 5:
			#	print(neighbours)
			
			if len(neighbours) > 1:
			
				add_set = False
				indice_set = set()
				indice_set.add(poi_index[i][0])
				
				#if i == 1:
				#	print(neighbours)
			
				for j in range(len(neighbours)):
				
				
					if not np.array_equal(poi_index[neighbours[j]][0], poi_index[i][0]):
					
						
						continue_analysis = True
						
						path_distance = 0
						
						try:
							path = nx.shortest_path(G, source = poi_index[i][2], target = poi_index[neighbours[j]][2], weight = 'weights')
						
						except nx.exception.NetworkXNoPath:
							
							continue_analysis = False
							
							#print([i, neighbours[j]])
							
						else:
						
							#if i == 1:
							#	print(path)
						
							path_points = []
							
							#print(len(path))
							if len(path) == 1:
							
								path_points.append(node_xy_coords[path[0]])

							else:
								for k in range(len(path)):

									path_points.append(node_xy_coords[path[k]])
									
									if k < len(path) - 1:
									
										halfway_point = [(node_xy_coords[path[k+1]][0] + node_xy_coords[path[k]][0])/2,
														 (node_xy_coords[path[k+1]][1] + node_xy_coords[path[k]][1])/2]
										
										
										
										halfway_radius = distance(node_xy_coords[path[k]], node_xy_coords[path[k+1]]) + 2*main_rad
										
										
										node_neighbours = algorithm_normal_tree.query_ball_point(halfway_point, halfway_radius)
										
										#print(node_xy_coords[path[k]])
										#print(node_xy_coords[path[k+1]])
										
										rect = vector.Rectangle(node_xy_coords[path[k]], node_xy_coords[path[k+1]], main_rad)
										
										poly = sh.Polygon(rect.get_rectangle())
										
										#if i == 1:
										
										#	print(node_neighbours)
										
										for l in range(len(node_neighbours)):
										
										
											if poly.contains(sh.Point(algorithm_normal_xy[node_neighbours[l]])):
											
											
												if distance(algorithm_normal_xy[node_neighbours[l]], poi_index[i][1]) > 2*main_rad and distance(algorithm_normal_xy[node_neighbours[l]], poi_index[neighbours[j]][1]) > 2*main_rad:
													
													#if i == 1:
													#	print([i, algorithm_normal_xy[node_neighbours[l]]])
													continue_analysis = False
													break
									
								
								
								
								
									if distance(node_xy_coords[path[k]], poi_index[i][1]) > main_rad and distance(node_xy_coords[path[k]], poi_index[neighbours[j]][1]) > main_rad:
									
										node_neighbours = algorithm_normal_tree.query_ball_point(node_xy_coords[path[k]], main_rad)
										
										
										#poly = Rectangle(node_xy_coords[path[k-1]], node_xy_coords[path[k]], 5)
												
												
										
										
										
										if len(node_neighbours) > 0:
										
											#if i == 1:
											
												#for v in node_neighbours:
												
													#print([i, algorithm_normal_xy[v], '2'])
													#print(path[k])
													#print(node_xy_coords[path[k]])
													
											continue_analysis = False
											break
						
						#if i == 1:
						#	print('yep')
						
						if continue_analysis:
							
							#print(path_points)
						
							if len(path_points) == 1:
							
								ratio = 1
						
							else:
							
						
								for k in range(len(path_points)):

									if k == 0:
										
										node_node_vector = [path_points[k+1][0] - path_points[k][0], path_points[k+1][1] - path_points[k][1]]
										node_point_vector = [poi_index[i][1][0] - path_points[k][0], poi_index[i][1][1] - path_points[k][1]]
										

										path_distance += sqrt(vector.cross(node_node_vector, node_point_vector)**2)/sqrt(node_node_vector[0]**2 + node_node_vector[1]**2)
									
									
									elif k == 1:
									
										node_distance = distance(path_points[k], path_points[k-1])
									
										point_distance = sqrt(vector.dot(node_node_vector, node_point_vector)**2)/sqrt(node_node_vector[0]**2 + node_node_vector[1]**2)
									
										dot_prod = vector.dot(node_node_vector, node_point_vector)
									
										path_distance += node_distance - (point_distance * dot_prod/sqrt(dot_prod**2))
									
									
									else:
									
										path_distance += distance(path_points[k], path_points[k-1])
										
								
								#print(path)
								
								#print(poi_index[neighbours[j]][2])
								
								k = len(path_points) - 1
								
								#print(path)
								
								node_node_vector = [path_points[k-1][0] - path_points[k][0], path_points[k-1][1] - path_points[k][1]]
								node_point_vector = [poi_index[neighbours[j]][1][0] - path_points[k][0], poi_index[neighbours[j]][1][1] - path_points[k][1]]

								path_distance += sqrt(vector.cross(node_node_vector, node_point_vector)**2)/sqrt(node_node_vector[0]**2 + node_node_vector[1]**2)
								
								dot_prod = vector.dot(node_node_vector, node_point_vector)
								
								path_distance -= sqrt(vector.dot(node_node_vector, node_point_vector)**2)/sqrt(node_node_vector[0]**2 + node_node_vector[1]**2) * dot_prod/sqrt(dot_prod**2)
										
								#print(path_distance)
								
								displacement = distance(poi_index[i][1], poi_index[neighbours[j]][1])
								
								#print(path_distance)
								#print(displacement)
								
								#ratio = (path_distance/displacement) * (1 - 2/path_distance)
								
								ratio = (0.002*path_distance**2 + path_distance)/displacement 
								
								#print(i, ratio)
								
							if ratio < 2:
							
								indice_set.add(poi_index[neighbours[j]][0])
								
								add_set = True
								
								
							elif displacement <= 20 and len(path) < 5:
							
								indice_set.add(poi_index[neighbours[j]][0])
								
								add_set = True
								
							elif path_distance <= 15:
							
								indice_set.add(poi_index[neighbours[j]][0])
								
								add_set = True
								
							#if i == 1:# or i == 15 or i == 16 or i == 19:
								
							#	print([i, poi_index[neighbours[j]], ratio, path_distance, displacement])
								

				
				if add_set:
					logger_neighbours.append(indice_set)
					
				
				
				
				
		i = 0
		j = 1

		#print(logger_neighbours)

		logger_neighbours = np.array(logger_neighbours)

		if len(logger_neighbours) < 2:

			i = j + 1

		while i < j:

			#print(logger_neighbours[i])

			if logger_neighbours[i] == logger_neighbours[j] or logger_neighbours[i] <= logger_neighbours[j]:
			
				logger_neighbours = np.delete(logger_neighbours, i, 0)
				
				j = i + 1
				
				
			elif logger_neighbours[i] >= logger_neighbours[j]:
			
				logger_neighbours = np.delete(logger_neighbours, j, 0)
			
			
			else:

				j += 1
				
			
			#print(logger_neighbours)
			#print([i, j])
			
			if j >= len(logger_neighbours):
			
				 i += 1
				 
				 j = i + 1
				 
			if i >= len(logger_neighbours) - 1:
			
				break


		#print(logger_neighbours)

		group_points = []

		for i in range(len(logger_neighbours)):

			group_list = list(logger_neighbours[i])
			
			
			path_set = set()
			
			x = 0
			y = 0
			
			#print(group_list)
			
			for j in range(len(group_list)):
			
				x += poi_index[group_list[j]][1][0]
				y += poi_index[group_list[j]][1][1]
				
			
				# if j == 0:
					# continue
			
				# if not poi_index[group_list[j]][2] in path_set:
			
					# path = nx.shortest_path(G, source = poi_index[group_list[0]][2], target = poi_index[group_list[j]][2], weight = 'weights')
			
					# path_set = path_set.union(set(path))
					
				# else:
					# continue
				
				#print(path_set)
				
			y = y/len(group_list)
			x = x/len(group_list)

			# eligible_nodes = []
			
			# path_list = list(path_set)
			
			# for j in range(len(path_set)):
			
				# eligible_nodes.append(node_xy_coords[path_list[j]])
				
			# #print(eligible_nodes)
				
			# eligible_node_tree = cKDTree(eligible_nodes)
			
			point = [x, y]
			
			#dist, nearest_eligible_node = eligible_node_tree.query(point)

			#group_points.append(np.array([node_xy_coords[path_list[nearest_eligible_node]], group_list]))
			
			group_points.append([point, group_list])
		
		#print(group_points)
		
		POI_list = group_points
			
			
		#group_points = np.array(group_points)


		grouped_logger_indices = set()

		for i in range(len(logger_neighbours)):

			grouped_logger_indices = grouped_logger_indices.union(logger_neighbours[i])

		grouped_logger_indices = list(grouped_logger_indices)

		#print(grouped_logger_indices)

		groups = []


		for i in range(len(grouped_logger_indices)):

			groups.append(poi_index[grouped_logger_indices[i]][1])




		groups = np.array(groups)


		all_logger_indices = set()

		for i in range(len(poi_index)):

			all_logger_indices.add(poi_index[i][0])


		lone_logger_indices = list(all_logger_indices.difference(grouped_logger_indices))


		#print(all_logger_indices)
		#print(lone_logger_indices)


		threshold_confidence = 2

		final_POIs = []

		#print(group_points[0][1])

		for i in range(len(group_points)):

			confidence = 0

			for j in range(len(group_points[i][1])):
			
				confidence += algorithm_pois[int(group_points[i][1][j])][3]
				
				#Mains Material Averaging goes here if needed
				
			if confidence > 10:
			
				confidence = 10
				
			if confidence >= threshold_confidence:

				#final_POIs.append([group_points[i][0][0], group_points[i][0][1], confidence, group_points[i][1], 'Group', algorithm_pois[int(group_points[i][1][j])][6]])
				final_POIs.append([group_points[i][0][0], group_points[i][0][1], confidence, group_points[i][1], 'Group', 'Group'])
			
		#print(algorithm_pois[12])
			
		for i in range(len(lone_logger_indices)):

			if algorithm_pois[lone_logger_indices[i]][3] >= threshold_confidence:

				final_POIs.append([poi_index[lone_logger_indices[i]][1][0], poi_index[lone_logger_indices[i]][1][1], algorithm_pois[lone_logger_indices[i]][3], [], algorithm_pois[lone_logger_indices[i]][5], algorithm_pois[lone_logger_indices[i]][6]])





		#final_POIs = np.array(final_POIs)

		print('Number of POIs: %s' %len(final_POIs))
		
		
		address_data = np.array(address_data)
		
		self.address_data = address_data
		
		#print(address_data)
		
		address_xy = []
		
		for i in range(len(address_data)):
		
			address_xy.append([address_data[i][0], address_data[i][1]])
			
		#print(address_xy)
		
		address_tree = cKDTree(address_xy)
		
		final_POIs_xy = []
		
		for i in range(len(final_POIs)):
		
			final_POIs_xy.append([final_POIs[i][0], final_POIs[i][1]])
		
		try:
			nearest_address_distance, nearest_address_index = address_tree.query(final_POIs_xy)
		except ValueError:
			self.nearest_address_index = []
			nearest_address_index = []
		else:
			self.nearest_address_index = nearest_address_index
		
		for i in range(len(final_POIs)):
		
			#final_POIs[i] = list(final_POIs[i])
			
			#print(address_data[nearest_address_index[i]][0])
			#print(nearest_address_distance[i])
		
			final_POIs[i].append(address_data[nearest_address_index[i]][2])
			final_POIs[i].append(round(nearest_address_distance[i]))
		
	
		
		#print(final_POIs)
		

		
		
		#self.p_geo = p_geo
		#self.m_geo = m_geo
		#self.o_geo = o_geo		
		
		#self.algorithm_data = algorithm_data
		self.final_POIs = final_POIs		
		self.poi_index = poi_index

		#self.checker = checker
		
		#self.dma_id = dma_id
		
		#self.database = database
		
		data_list = []
		
		for i in range(len(final_POIs)):
		
			data_list.append([final_POIs[i][0], final_POIs[i][1], 'POI', final_POIs[i][2], final_POIs[i][4], final_POIs[i][5], final_POIs[i][6], final_POIs[i][7]])
			
			
			for j in range(len(final_POIs[i][3])):
			
				#print(final_POIs[i][3])
			
				data_list.append([poi_index[int(final_POIs[i][3][j])][1][0], poi_index[int(final_POIs[i][3][j])][1][1], 'sub-POI', algorithm_pois[int(final_POIs[i][3][j])][3], algorithm_pois[int(final_POIs[i][3][j])][5], algorithm_pois[int(final_POIs[i][3][j])][6], '', ''])
				
				
		
		self.poi_data_list = np.array(data_list)
		poi_data_list = np.array(data_list)
		
		#print(poi_data_list)
				
		for i in range(len(new_data_points)):
		
			point = [new_data_points[i][0], new_data_points[i][1]]
			
			duplicate = False
			
			for j in range(len(data_list)):
			
				data_list_point = [data_list[j][0], data_list[j][1]]
				
			
				if np.array_equal(point, data_list_point):
				
					#print(point)
					#print(data_list_point)
				
					duplicate = True
					break
					
			if not duplicate:
			
				data_list.append([new_data_points[i][0], new_data_points[i][1], 'Normal', 0, '', '', '', ''])
			
			
		data_list = np.array(data_list)
		self.address_xy = np.array(address_xy)
		
		self.final_POIs = final_POIs
		self.poi_index = poi_index
		
		return data_list, poi_data_list, final_POIs, poi_index, nearest_address_index
		
		
	
	def get_mains(self):
	
		return [self.m_geo, self.p_geo, self.o_geo]

