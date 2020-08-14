

from math import sqrt

#Vector Class to create rectangles out of 2 (x, y) points with width size/2

#2 Dimensional 

#Calculates dot product of two vectors
def dot(vector_a, vector_b):

	product = 0

	if len(vector_a) == len(vector_b):
	
		for i in range(len(vector_a)):
		
			product += vector_a[i] * vector_b[i]
			
	else:
	
		raise TypeError('Vectors must have equal dimensions')
			
	return product

#Calculates cross product of two vectors
def cross(vector_a, vector_b):



	if len(vector_a) == len(vector_b):
	
		
		k = vector_a[0]*vector_b[1] - vector_a[1]*vector_b[0]
		
		
	else:
	
		raise TypeError('Vectors must have equal dimensions')
			

			
	return k
		
#Returns whether cross product is positive of negative
def cross_sign(vector_a, vector_b):


	positive = True

	if len(vector_a) == len(vector_b):
	
		
		k = -1*(vector_a[0]*vector_b[1] - vector_a[1]*vector_b[0])
		
		
	else:
	
		raise TypeError('Vectors must have equal dimensions')
			
			
	if k >= 0:
	
		positive = True
		
	else:
	
		positive = False
			
			
	return positive
	

#Vector Class to create rectangles out of 2 (x, y) points with width size/2

class Rectangle():

	def __init__(self, point_a, point_b, size):
	
		#Creating vector which points from a to b
		vector = [(point_b[0] - point_a[0]), (point_b[1] - point_a[1])]

		#Calculating vector length
		length = sqrt(vector[0]**2 + vector[1]**2)

		#Creating unit vector
		unit_vector = [((1/length) * vector[0]), ((1/length) * vector[1])]

		#Array which creates a perpendicluar vector to any 2D vector
		perp_matrix = [[0, -1], [1, 0]]

		#Creating perpendicluar unit vector
		perp_unit_vector = [perp_matrix[0][1] * unit_vector[1], perp_matrix[1][0] * unit_vector[0]]


		#By adding 2 opposite perpendicluar unit vectors to each point this creates the 4 points needed for a rectangle
		#Multiplying each unit vector by size creates a rectangle with width size/2 centred around the original vector
		rectangle = [[(size*perp_unit_vector[0] + point_a[0]), (size*perp_unit_vector[1] + point_a[1])],
					 [(-1*size*perp_unit_vector[0] + point_a[0]), (-1*size*perp_unit_vector[1] + point_a[1])],
					 [(-1*size*perp_unit_vector[0] + point_b[0]), (-1*size*perp_unit_vector[1] + point_b[1])],
					 [(size*perp_unit_vector[0] + point_b[0]), (size*perp_unit_vector[1] + point_b[1])]]

	

		self.rectangle = rectangle
		
	def get_rectangle(self):
	
		return self.rectangle

	#An attempt to find whether a point is contained by the rectangle
	#Currently unused by ADA
	def within_rectangle(self, point):
	
	
		rectangle = self.rectangle
		
		for i in range(len(rectangle)):
		
			j = i + 1
		
			if j >= len(rectangle):
			
				j = 0
		
			vector_a = [rectangle[j][0] - rectangle[i][0], rectangle[j][1] - rectangle[i][1]]
			
			vector_b = [point[0] - rectangle[i][0], point[1] - rectangle[i][1]]
			
			
			within = cross_sign(vector_a, vector_b)
			
			if not within:
				
				#print(vector_a)
				#print(vector_b)
				break
		
		
		return within
