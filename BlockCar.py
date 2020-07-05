import pygame
import math

class BlockCar():
	def __init__(self, bounds:list, size:list=[100,50]):
		self.pos = [10, bounds[1]//2]
		self.speed = [0, 0]
		self.bounds = bounds
		self.colorloc = 0
		self.size:list = size

		self.max_acc = 0.00075 
		self.max_speed = 1.25
		self.firction = 0.001
		self.bounce = 0.75

		self.color = (0,100,255)
		self.tip_color = (50,0,0)

		self.rotation = 0
		self.rotspeed = 0
		self.stall_rotpower = math.pi / 7e4
		self.rotpower = self.stall_rotpower
		self.rotfriction = 0.995
		self.max_rotspeed = 0.015

	def update_loc(self):
		self.rotspeed = self._clamp(self.rotspeed, self.max_rotspeed)
		self.rotation += self.rotspeed
		self.rotspeed *= self.rotfriction

		# Calc the current rotation speed
		dirspeed = math.sqrt(self.speed[0]**2 + self.speed[1]**2)
		max_decrease = self.stall_rotpower/1.8

		self.rotpower = self.stall_rotpower - min(self._map(dirspeed, 0, 0.5, 0, max_decrease) , max_decrease)

		self.pos[0] += self.speed[0]
		self.pos[1] += self.speed[1]

		self.speed = [x * (1-self.firction) for x in self.speed]

		self.edge_collision()

	def rotate_to_wall(self, collision_axis:int):

		# Calculate the direction of rotation
		corrected_angle = self.rotation % math.pi
		axis_multiplier = -1 if collision_axis == 1 else 1
		direction = (-1 if corrected_angle > math.pi/2 else 1) * axis_multiplier
		
		#Caluclate the force of rotation
		rot_const = .006
		# The faster it goes, more angle correction
		speed_r = math.sqrt(self.speed[0]**2 + self.speed[1]**2) 
		# The more non-grid the angle is, more correction
		angle_offset = (abs(self.rotation % (math.pi / 4) - (math.pi/4))**3)*5 + 0.2
		force = rot_const * (speed_r / angle_offset)

		self.rotspeed += direction * force

	def edge_collision(self):
		# Collision axis
		# -1 : No collision
		# 0 : X axis collision
		# 1 : Y axis collision
		collisionAxis = -1
		points = self.get_points(self.rotation)
		safe_space = 1

		x_coordinates = [point[0] for point in points]
		y_coordinates = [point[1] for point in points]
		min_maxs = [min(x_coordinates),
					max(x_coordinates),
					min(y_coordinates),
					max(y_coordinates)]

		if min_maxs[0] <= 0: #Left
			collisionAxis = 0
			self.pos[0] += -min_maxs[0]

		elif min_maxs[1] >= self.bounds[0]: #Right
			collisionAxis = 0
			self.pos[0] -= (min_maxs[1] - self.bounds[0])

		if min_maxs[2] <= 0: #Top
			collisionAxis = 1
			self.pos[1] += -min_maxs[2]

		elif max(y_coordinates) >= self.bounds[1]: #Bottom
			collisionAxis = 1
			self.pos[1] -= (min_maxs[3] - self.bounds[1])

		if collisionAxis != -1:
			self.speed[collisionAxis] *= -self.bounce
			self.rotate_to_wall(collisionAxis)

	def get_points(self, start_ang:float=0):
		r = math.hypot(self.size[0]/2, self.size[1]/2)

		center = (self.pos[0]+self.size[0]//2, self.pos[1]+self.size[1]//2)
		angles = [
			math.atan2( (self.size[1]/2),(self.size[0]/2) ),
			math.atan2( -(self.size[1]/2),(self.size[0]/2) ),
			math.atan2( -(self.size[1]/2),-(self.size[0]/2) ),
			math.atan2( (self.size[1]/2),-(self.size[0]/2) )
		]

		points = []
		for box_ang in angles:
			ang = box_ang + start_ang
			points.append(
				(center[0] + r * math.cos(ang), center[1] + r * math.sin(ang))
			)

		# Round the points
		points = [(int(point[0]), int(point[1])) for point in points]
		return points

		return [(self.pos[0], self.pos[1]),
				(self.pos[0]+self.size[0], self.pos[1]),
				(self.pos[0]+self.size[0], self.pos[1]+self.size[1]),
				(self.pos[0], self.pos[1]+self.size[1])]

	def draw(self, screen: pygame.display):
		points = self.get_points(self.rotation)
		# Draw the rect
		pygame.draw.polygon(screen, self.color, points)
		# Draw the head
		pygame.draw.line(screen, self.tip_color, points[0], points[1], 3)			
		
	def drive(self, keys:dict):
		if keys[pygame.K_a]: #left
			self.rotspeed -= self.rotpower
		if keys[pygame.K_d]: #left
			self.rotspeed += self.rotpower

		if keys[pygame.K_w]:
			fpower = self.max_acc
		else:
			fpower = 0

		acc = [fpower * math.cos(self.rotation), fpower * math.sin(self.rotation)]

		self.speed = [self.speed[i] + acc[i] for i in range(2)]
		self.speed = [self._clamp(x, self.max_speed) for x in self.speed]

		# Break
		breakf = 0.996
		if keys[pygame.K_SPACE]:
			self.speed = [s*breakf for s in self.speed]
			self.rotspeed *= breakf

	@staticmethod
	def _clamp(value:float, min_max:float):
		if value > min_max:
			return min_max
		elif value < -min_max:
			return -min_max
		else:
			return value

	@staticmethod
	def _map(n, start1, stop1, start2, stop2):
		return ((n-start1)/(stop1-start1))*(stop2-start2)+start2
