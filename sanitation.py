import geopandas as gpd
import pandas as pd
import numpy as np
import shapely.geometry as sh


#Class to check that data is within the expected DMA with option to include buffer zone
class DataCheck():

	def __init__(self, dma_id):
	
		#Read DMA .shp file
		file = r'.shp\DMAs\DMAs.shp'
		dmas = gpd.read_file(file)

		#Extract DMA IDs and geometrys
		ref = dmas['reference'].tolist()
		geo = dmas['geometry'].tolist()

		#Create polygon/multi-polygon of DMA outline after finding desired DMA's geometry
		try:

			polygon = sh.Polygon(geo[ref.index(dma_id)])
		
		except NotImplementedError:
		
			
			polygon = sh.MultiPolygon(geo[ref.index(dma_id)])
		
		
		self.polygon = polygon


	#Check that every coordinate in data lies within the DMA + buffer boundary
	def check_data(self, data, buff):
	
	
		#data must have form:
		#data = [[x1, y1]
		#		,[x2, y2]
		#		,[x3, y3]
		#		,...]
			
		new_data = []
		error_indices = []
		
		for i in range(len(data)):
		
			coords = [float(data[i][0]), float(data[i][1])]
		
			point = sh.Point(coords)
			
			poly = self.polygon.buffer(buff)

			contains_point = poly.contains(point)
			
			if contains_point:
			
				new_data.append(data[i])
				
			else:
			
				error_indices.append(i)
	
		#Returns sanitised data and a list of coordinates which were found to be outwith the DMA
		return [new_data, error_indices]
		
		
	#Check whether a single (x, y) coordinate is within the DMA
	def check_point(self, point, buff):
	
		poly = self.polygon.buffer(buff)
	
		contains_point = poly.contains(sh.Point(point))
		
		#Returns True/False
		return contains_point
		
		
		
	def get_polygon(self):
	
		return self.polygon
		
	def get_polygon_with_buffer(self, buff):
	
		return self.polygon.buffer(buff)





