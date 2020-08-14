
from math import sqrt, floor
import pandas as pd

#OSGB36
#EPSG:27700

#The Ordinance Survey open source map of Great Britain (OS OpenMap - Local) comes as a series of .tif files separated into
#folders corresponding to which British National Grid tile they are located in. The files show a section of map 5km by 5km.

#BNG tiles separate Great Britain into 100km by 100km squares. 
#The .tif files are provided with titles corresponding to which 5km by 5km tile they represent.
#The file names have the form SJ89NE.tif

#SJ = 100km by 100km BNG tile 
#89 = 10km by 10km tile within SJ
#SE = bottom right 5km by 5km tile within SJ89

#The last 2 letters in the title can be SW, SE, NW, NE to represent North, East, South and West

#This class finds which map tile a point is located within a returns a list of filenames for easy lookup



def _numbers_to_letters(point, letters_list, xcoord, ycoord):

	#point has form [123456, 123456]
	x = point[0]
	y = point[1]
	
	#x1 and y1 represent the first digits of x and y
	x1 = floor(x/100000)
	y1 = floor(y/100000)
	
	
	#Finding the BNG tile letters which correspond to the first digits of point
	for i in range(len(letters_list)):
	
		if xcoord[i] == x1 and ycoord[i] == y1:
		
			letters = letters_list[i]
			
			
			
	#Finding the second digits	
	x2 = floor(x/10000) - x1*10
	y2 = floor(y/10000) - y1*10
	
	#Finding the third digits
	x3 = floor(x/1000) - (x1*100 + x2*10)
	y3 = floor(y/1000) - (y1*100 + y2*10)
	
	#The third digits are used to find which quadrant the point lies in
	if x3 >= 5:
		if y3 >= 5:
			quadrant = 'NE'
		else:
			quadrant = 'SE'
	else:
		if y3 >= 5:
			quadrant = 'NW'
		else:
			quadrant = 'SW'
			
	
	#The BNG letters, second digits and quadrant letters are combined to make the tile filename where the point can be found
	map_string = letters + str(x2) + str(y2) + quadrant
	
	return map_string
	
	
class MapStrings():

	def __init__(self):
	
		#Read the .csv which contains the list of BNG letters and their corresponding numbers
		reference_file = r'.shp\Maps\Grid Letters to Numbers.csv'

		reference = pd.read_csv(reference_file)

		self.letters = reference['Grid Letters'].tolist()
		self.xcoord = reference['X'].tolist()
		self.ycoord = reference['Y'].tolist()




	def get_map_strings(self, ext):
	
	
		letters = self.letters
		xcoord = self.xcoord
		ycoord = self.ycoord

		#List of points to find which tile they lie in. This is the extent of the DMA which sometimes can be greater the 10km
		#That means there is potential for a tile to be missed and not displayed
		points = [[ext[0], ext[1]], [ext[2], ext[1]], [ext[2], ext[3]], [ext[0], ext[3]]]

		map_string_list = []

			
		y_tile_match = False
		
		final_x = points[1][0]
		final_y = points[2][1]

		start_x = points[0][0]

		point = points[0]

		increase = 5000

		#In order to make sure all tiles are displayed point is increased by 5km every time until it lies in the same tile as the final x point 
		#The same is done for the final y point 
		while y_tile_match == False:

			x_tile_match = False
			
			point[0] = start_x
			
			#print(point[0])
			
			while x_tile_match == False:
			
				#print(point)
				
				map_string = _numbers_to_letters(point, letters, xcoord, ycoord)
				
				map_string_list.append(map_string)
				
				if floor(point[0]/5000) == floor(final_x/5000):
				
					#print(point)
				
					x_tile_match = True
					
					if floor(point[1]/5000) == floor(final_y/5000):
				
						y_tile_match = True
						
				point[0] += 5000
				
			point[1] += 5000
				


		return map_string_list
