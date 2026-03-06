import pygame
from src.vector import Vec2

from src.collision import Collider
from src.renderable import CircleRenderable, RectangleRenderable
class Entity:
	def __init__(self, p_position: Vec2, p_speed: float = 100, p_health: float = 100.0):
		self.m_collider = Collider()
		self.m_position = p_position
		self.m_speed = p_speed
		self.m_health = p_health
		self.m_alive = True
		self.m_shape = "base"

		self.m_dirty_geometry = True #immediate update when called upon

	def setRotation(self, p_theta: float): #rotation in radians
		self.m_theta = p_theta
		self.m_dirty_geometry = True

	def setPosition(self, p_position: Vec2):
		self.m_position = p_position
		self.m_dirty_geometry = True

	def collideWith(self, p_other):
		did_collide = self.m_collider.overlaps(self, p_other)
		#print(f"{self.m_shape} + {p_other.m_shape} {did_collide} collided")
		if did_collide:
			p_other.m_renderable.setColor((0, 255, 0))
		else:
			p_other.m_renderable.setColor((255, 0, 0))
		return did_collide

class CircleEntity(Entity):
	def __init__(self, p_position: Vec2, p_radius: float, p_speed: float = 100.0, p_health: float = 100.0):
		super().__init__(p_position, p_speed, p_health)
		self.m_shape = "circle"
		self.m_renderable = CircleRenderable(p_radius)
		self.m_radius = p_radius



	def draw(self, p_screen):
		self.m_renderable.draw(p_screen, self.m_position)

import math
class RectangleEntity(Entity):
	def __init__(self, p_position: Vec2, p_dimensions: Vec2, p_speed: float = 100.0, p_health: float = 100.0):
		super().__init__(p_position, p_speed, p_health)
		self.m_shape = "rectangle"
		self.m_renderable = RectangleRenderable(p_dimensions)
		self.m_dimensions = p_dimensions
		self.m_halfDimensions = 0.5 * p_dimensions
		
		self.m_theta = math.pi * 0.5 #looking up so width and height make sense
		self.m_axisX = Vec2(math.cos(self.m_theta), math.sin(self.m_theta)) #atomic vectors i and j to determine the rotation
		self.m_axisY = Vec2(-math.sin(self.m_theta), math.cos(self.m_theta))

		self.m_dirty_geometry = True
		

	def draw(self, p_screen):
		self.m_renderable.draw(p_screen, self.m_position, self.m_theta)

	def updateGeometry(self):
		if not self.m_dirty_geometry:
			return #no need to clean them leave state as is
		
		#generate vertices
		print("Updating Geometry")
		self.m_vertices = [
			Vec2(-self.m_halfDimensions.x, self.m_halfDimensions.y), #top left
			Vec2(self.m_halfDimensions.x, self.m_halfDimensions.y), #top right
			Vec2(self.m_halfDimensions.x, -self.m_halfDimensions.y), #bottom right
			Vec2(-self.m_halfDimensions.x, -self.m_halfDimensions.y) #bottom left
		]

		#get reusable sin cos for current theta
		cos_theta = math.cos(self.m_theta)
		sin_theta = math.sin(self.m_theta)
		for vertex in self.m_vertices: #rotate all points then put back into world space
			x = vertex.x
			y = vertex.y
			vertex.x = (x * cos_theta) - (y * sin_theta) + self.m_position.x
			vertex.y = (x * sin_theta) + (y * cos_theta) + self.m_position.y
		
		#reuse sin and cos to create local x and y axis of unit length
		self.m_axes = [
			Vec2(cos_theta, sin_theta),
			Vec2(-sin_theta, cos_theta)
		]
		self.m_dirty_geometry = False #regardless after this the geometry is clean

	def getEdgeNormals(self):
		return self.m_axes

	def project(self, p_axis: Vec2) -> Vec2:
		min_projection = float("inf")
		max_projection = -float("inf")

		for vertex in self.m_vertices: #project and track min and max
			projection = vertex.dot(p_axis)
			if projection < min_projection:
				min_projection = projection
			if projection > max_projection:
				max_projection = projection
		return Vec2(min_projection, max_projection)
		