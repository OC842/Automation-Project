import numpy as np


#Class for connecting to the MySQL database and retrieving data
class DatabaseData():

	#Connect to database a retrieve all data for specified dma, run and project id
	def __init__(self, dma_id, checker, cnx, run, project_id):


		self.cnx = cnx
		cursor = cnx.cursor()

		#If run = 0 retrieve all data for dma and project id
		if run == 0:
		
			query = ("SELECT * FROM data WHERE dma_id = %s and project_id = %s")
			
			values = (dma_id, project_id)
		
		#Else retrieve data for specific run
		else:
			query = ("SELECT * FROM data WHERE dma_id = %s and run = %s and project_id = %s")
			
			values = (dma_id, run, project_id)

		#Execute SQL
		cursor.execute(query, values)
		#Retrieve data
		raw_data = cursor.fetchall()
		
		#If no data found raise error to be handled
		if len(raw_data) == 0:
		
			raise ValueError
		




		data = []
		leak_data = []
		date = []
		
		#Separate data into data (x, y, level, spread) and leak data (x, y, 'Y' or 'N') and date
		for i in range(len(raw_data)):
		
			data.append([raw_data[i][2], raw_data[i][3], raw_data[i][4], raw_data[i][5]])
			
			leak_data.append([raw_data[i][2], raw_data[i][3], raw_data[i][6]])
			
			date.append(raw_data[i][8])
			


		#Sanitising data - making sure all data point lie within DMA
		data, errors = checker.check_data(data, 10)
		leak_data, leak_errors = checker.check_data(leak_data, 10)
		

		#If no data lies within DMA raise error to be handled
		if len(data) == 0:
		
			raise AttributeError
		

		#Making data accessible to get functions
		self.dma_id = dma_id
		self.coordinates = data
		self.date = date
		self.leaks = leak_data
	
	#Return data
	def get_data(self):
	
		return self.coordinates
			
	#Return mean of data set
	#combine boolean sets whether the level and spread values are combined or not
	def get_mu(self, combine):
	
		mu = np.average(self.coordinates, 0)
		
		if combine == True:
		
			data = self.coordinates
			x = []
			
			for i in range(len(data)):
			
				if(data[i][3] == 0):
				
					ls = 0
				else:
					ls = data[i][2]/data[i][3]
				
				#print(ls)
			
				x.append([data[i][0], data[i][1], ls])
		
			
			
			mu = np.average(x, 0)
		
		return mu
		
	#Return standard deviation of data set
	#combine boolean sets whether the level and spread values are combined or not
	def get_sigma(self, combine):
	
		sigma = np.std(self.coordinates, 0)
		
		if combine == True:
		
			data = self.coordinates
			x = []
			
			for i in range(len(data)):
			
				if(data[i][3] == 0):
				
					ls = 0
				else:
					ls = data[i][2]/data[i][3]
				
				#print(ls)
			
				x.append([data[i][0], data[i][1], ls])
		
			
			
			sigma = np.std(x, 0)
		
		return sigma
		
		
	#Get data with the level and spread values combined into a ratio
	def get_combined_data(self):
	
		data = self.coordinates
		x = []
		
		#print(data[0][2])
		#print(data[0][3])
		
		for i in range(len(data)):
		
			if(data[i][3] == 0):
			
				ls = 0
			else:
				ls = data[i][2]/data[i][3]
			
			#print(ls)
		
			x.append([data[i][0], data[i][1], ls])
			
		
		return x
		
	#Return xy data
	def get_xy_data(self):

		data = self.coordinates
		xy_values = []
		
		for i in range(len(data)):
		
					
			xy_values.append(np.array([data[i][0], data[i][1]]))
		
		return xy_values
		
	#Return leak data
	def get_leak_data(self):
	
		return self.leaks
		
	#Calculate the ratio and level values which the 'mult' percentile
	#e.g. if mult = 0.9 this function would return the value at the 90th percentile
	def get_min_z(self, mult):
	
		cnx = self.cnx

		cursor = cnx.cursor()
		
		query = ("SELECT level, spread FROM data")
		
		cursor.execute(query, )

		all_data = cursor.fetchall()
		
		ratio = []
		level = []
		
		for i in range(len(all_data)):
		
			if all_data[i][1] == 0:
			
				val = 0
				
			else:
		
				val = all_data[i][0]/all_data[i][1]
		
			ratio.append(val)
			
			level.append(all_data[i][0])
				
		#sorting arrays
		ratio = np.sort(np.array(ratio))
		level = np.sort(np.array(level))
		
		min_ratio = ratio[int(len(ratio)*mult)]
		
		min_level = level[int(len(level)*mult)]
		
		return [min_ratio, min_level]
		
		
	
		
		
	
	
