from lib.database_data import DatabaseData
from lib.grouping import Grouper
from lib.mapping import Map
from lib.pois import POIs
from lib.sanitation import DataCheck

import mysql.connector
import pandas as pd
import numpy as np
from datetime import date
import sys, os

ratio_factor = 0
level_factor = 0

folder = 'Output'

cnx = mysql.connector.connect(user='root', password='database1', host='127.0.0.1', database='dld')

cursor = cnx.cursor()

query = ("SELECT * FROM dmas WHERE project_id = 3 and dma_id = 'DMA004162'")#P1 = 'Outstanding'")#


cursor.execute(query)

dmas = cursor.fetchall()


#do = False
do = True



if do:

	for i in range(len(dmas)):
	

		print('\n' + str(dmas[i][2]))
		
		dma_id = dmas[i][2]
		
		name = dmas[i][1]

		dma_name = name[0:len(name)-3]
		
		
		directory = folder + '\\' + dma_name + dma_id
		gis_directory = directory + r'\GIS'
		
		if not os.path.exists(directory):
			os.makedirs(directory)
			
		if not os.path.exists(gis_directory):
			os.makedirs(gis_directory)
		
		
		
		
		

		project_id = dmas[i][5]
		
		checker = DataCheck(dma_id)
		
		#Grh = Graph(dma_id, checker, mains_shape_file_path)
		#G, points = Grh.get_Graph()
		
		
		dma_outline = checker.get_polygon().buffer(10)
	

		algorithm = Grouper(dma_id, checker)
		
		mains = algorithm.get_mains()

		points = algorithm.get_node_info()
		
		
		
		map = Map(directory, checker, mains)
		
		address_data = map.get_address_data()
		
		bv_data = map.get_bv_data()
		
		
		
		
		for k in range(dmas[i][4] + 1):
		
			#k = dmas[i][4]
		
			run = k + 1
			
			if k >= dmas[i][4]:
			
				run = 0

			try:
				database = DatabaseData(dma_id, checker, cnx, run, project_id)
			
			except ValueError:
			
				print('No data for %s run %s, project %s' %(dma_id, run, project_id))
				continue
				
			except AttributeError:
			
				print('No data within DMA boundary for %s run %s, project %s\nPlease check data.' %(dma_id, run, project_id))
				continue


			#pois = POIs(dma_id, ratio_factor, level_factor, database).get_algorithm_data()
			pois = POIs(dma_id, points, database).get_algorithm_data()
			
			raw_data = database.get_data()

			#algorithm = Grouper(dma_id, pois, database, checker, mains_shape_file_path, Grh, G, points)
			
			data_list, poi_data_list, final_POIs, poi_index, nearest_address_index = algorithm.analyse_pois(pois, raw_data, address_data, bv_data)


			filename = dma_name + dma_id + ' Run ' + str(run)

			if k >= dmas[i][4]:
			
				filename = dma_name + dma_id + ' Full Analysis '




			#poi_data_list = algorithm.get_poi_data_list()
				
			
			poi_id_list = []
			
			print('Uploading data')	
			
			for j in range(len(poi_data_list)):
			
				ratio_string = poi_data_list[j][4]
				
				if ratio_string == 'Group':
				
					level = 'Group'
					spread = 'Group'
					ratio = 'Group'
				
				else:
					ratio_array = ratio_string.split("/")
					
					#ratio_array = ratio_array[1].split('/')
					
					level = ratio_array[0]
					spread = ratio_array[1]
					
					ratio = round(float(level)/float(spread), 5)
				
				#print(ratio)
			
				if poi_data_list[j][2] == 'POI':
				
					
					if j < len(poi_data_list) - 1:
					
						if poi_data_list[j+1][2] == 'POI':
						
							sub_POI = False
							
						else:
					
							sub_POI = True
			
					elif j == len(poi_data_list) - 1:
					
						sub_POI = False
					
					else:
						sub_POI = True
						
					job_booked = 'TBC'
			
					values = (dma_id, str(poi_data_list[j][0]), str(poi_data_list[j][1]), level, spread, ratio, str(poi_data_list[j][3]), ratio_factor, level_factor, run, sub_POI, date.today(), str(project_id))
					
					
					query = ("SELECT * FROM pois WHERE dma_id = %s and x = %s and y = %s and level = %s and spread = %s and confidence = %s and ratio_threshold = %s and level_threshold = %s and run = %s and project_id = %s")
		
					test_for_duplicate = (dma_id, str(poi_data_list[j][0]), str(poi_data_list[j][1]), level, spread, str(poi_data_list[j][3]), ratio_factor, level_factor, run, project_id)
				
					cursor.execute(query, test_for_duplicate)
				
					match = cursor.fetchall()
					
					#print(match)
					
					if len(match) == 0:
					
				
						query = ("INSERT INTO pois (dma_id, x, y, level, spread, ratio, confidence, ratio_threshold, level_threshold, run, sub_POI, date_created, project_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
						
						#print(values)
						
						cursor.execute(query, values)
						
						query = ("SELECT poi_id FROM pois ORDER BY poi_id DESC LIMIT 1")
				
						cursor.execute(query)

						poi_id = cursor.fetchall()
						
						poi_id_list.append(poi_id[0][0])
						
					else:
					
						poi_id_list.append(match[0][0])
						
						#print(match[0][0])
					
					#print(values)
					
					#cursor.execute(query, values)
					
					#cnx.commit()
				
				
				
				elif poi_data_list[j][2] == 'sub-POI':
				
				
					query = ("SELECT poi_id FROM pois ORDER BY poi_id DESC LIMIT 1")
				
					cursor.execute(query)

					poi_id = cursor.fetchall()
				
					values = (dma_id, str(poi_data_list[j][0]), str(poi_data_list[j][1]), level, spread, ratio, str(poi_data_list[j][3]), ratio_factor, level_factor, run, str(poi_id[0][0]), date.today(), str(project_id))
					
					
					
					query = ("SELECT * FROM sub_pois WHERE dma_id = %s and x = %s and y = %s and level = %s and spread = %s and confidence = %s and ratio_threshold = %s and level_threshold = %s and run = %s and project_id = %s")
		
					test_for_duplicate = (dma_id, str(poi_data_list[j][0]), str(poi_data_list[j][1]), level, spread, str(poi_data_list[j][3]), ratio_factor, level_factor, run, project_id)
				
					cursor.execute(query, test_for_duplicate)
				
					match = cursor.fetchall()
					
					#print(match)
					
					if len(match) == 0:
					
						query = ("INSERT INTO sub_pois (dma_id, x, y, level, spread, ratio, confidence, ratio_threshold, level_threshold, run, poi_id, date_created, project_id) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
						#print(values)
						cursor.execute(query, values)
					
					#cnx.commit()
					
					poi_id_list.append('')
					
				else:
				
					poi_id_list.append('')
			

			poi_ids_for_GIS = list(poi_id_list)
			
			#algorithm.output_results_with_poi_id(gis_directory, filename, pois_only, poi_ids_for_GIS, data_list)
		
			#algorithm.output_with_map(directory, filename, poi_id_list, pois, data_list)
			
			mapping_data = [pois, final_POIs, poi_index, nearest_address_index, data_list, poi_id_list]
			
			map.add_features(filename, mapping_data)

		
		map.close_fig()
		
		query = ("UPDATE dmas SET P1 = 'Complete' WHERE dma_id = %s;")
			
		print(dmas[i])
			
		value = (dmas[i][2],)

		cursor.execute(query, value)
		
		#cnx.commit()
		
	a = input('Press Enter to commit...')	
	cnx.commit()
	
	cursor.close()
	cnx.close()
		
else:

	dma_id = 'DMA005295'

	checker = data_check(dma_id, dma_shape_file_path)



	database = database_data(dma_id, checker, cnx, 1)

	name = database.get_DMA_name(dma_id)

	dma_name = name[0:len(name)-3]



	pois = POIs(dma_id, ratio_factor, level_factor, database).get_algorithm_data()

	algorithm = Graph(dma_id, pois, database, checker, mains_shape_file_path)



	filename = dma_name + dma_id + str(output_file)


	#algorithm.output_results(directory, filename, pois_only)

	algorithm.output_with_map(directory, filename, pois_only, poi_id_list)

	algorithm.show_graph()
		



	
	

