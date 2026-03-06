import pygame
from src.vector import Vec2

from src.collision import Collider
from src.renderable import CircleRenderable, RectangleRenderable
from src.window import WINDOW
class Entity:
	def __init__(self, p_position: Vec2 = Vec2(0.0), p_speed: float = 100, p_rotationSpeed: float = 0.5, p_health: float = 1000.0, p_damage: float = 0):
		self.m_collider = Collider()
		self.m_position = p_position
		self.m_direction = Vec2()
		self.m_dirty_geometry = True #immediate update when called upon

		self.m_owner = None #allows for friendly fire control | allows for bullets to not kill the shooter
		self.m_collisionCount = 0 #how many objects it colliding with at a given frame
		self.m_identity = None #used for collision pairing, ENTITY_REGISTRY sets this so only enetiies registerd will be apart of the actaul game

		self.m_damage = p_damage
		self.m_speed = p_speed
		self.m_rotationSpeed = p_rotationSpeed
		
		self.m_health = p_health
		self.m_alive = True
		
		self.m_shape = "base"

	def setRotation(self, p_theta: float): #rotation in radians NEED TO CONVERT TO DEG if for some reason something requires it (pygame renderer)
		self.m_theta = p_theta
		self.m_dirty_geometry = True

	def offsetRotation(self, p_delta: float): #doesnt set but adds the delta rotation
		self.m_theta += p_delta
		self.m_dirty_geometry = True

	def setPosition(self, p_position: Vec2): #sets exact position in screen coordinates
		self.m_position = p_position
		self.m_dirty_geometry = True

	def updatePosition(self): #for if the entity has its own internal position handling IE AI or a projectile
		pass

	def offsetPosition(self, p_delta: Vec2): #doesnt set but adds the direction
		self.m_position += p_delta
		self.m_dirty_geometry = True

	def collideWith(self, p_other):
		return self.m_collider.overlaps(self, p_other)
	
	def damage(self, p_damage: float):
		self.m_health -= p_damage
		if self.m_health <= 0:
			self.m_alive = False

	def heal(self, p_health: float):
		self.m_health += p_health
		if self.m_health > 0:
			self.m_alive = True

	def onCollisionEnter(self, p_other: "Entity"): #allows for custom handling on how to act with differnet entity collision combos IE bullet with ship and ship with bullet etc
		if isinstance(p_other, Entity):
			p_other.damage(self.m_damage) #default enemies that run into one another just hurt each other

	def getDirection(self):
		self.m_direction = Vec2(
			math.cos(self.m_theta),
			math.sin(self.m_theta)
		)
		return self.m_direction
	
	def ownedBy(self, p_other: "Entity"):
		if isinstance(p_other, Entity):
			self.m_owner = p_other #register the owner

	def drawCollision(self):
		if self.m_collisionCount > 0:
			self.m_renderable.setColor((0, 255, 0))
		else:
			self.m_renderable.setColor((255, 0, 0))

	def draw(self):
		raise NotImplementedError
	
class CircleEntity(Entity):
	def __init__(self, p_position: Vec2, p_radius: float, p_speed: float = 100.0, p_rotationSpeed: float = 10, p_health: float = 100.0, p_damage: float = 0):
		super().__init__(
			p_position = p_position,
			p_speed = p_speed,
			p_health = p_health,
			p_damage = p_damage
		)
		self.m_shape = "circle"
		self.m_renderable = CircleRenderable(p_radius)
		self.m_radius = p_radius

	def draw(self):
		self.m_renderable.draw(WINDOW.m_screen, self.m_position)

import math
class RectangleEntity(Entity):
	def __init__(self, p_position: Vec2, p_dimensions: Vec2, p_speed: float = 100.0, p_rotationSpeed: float = 0.5, p_health: float = 100.0, p_damage: float = 0):
		super().__init__(
			p_position = p_position,
			p_speed = p_speed,
			p_rotationSpeed= p_rotationSpeed,
			p_health = p_health,
			p_damage = p_damage
		)
		self.m_shape = "rectangle"
		self.m_renderable = RectangleRenderable(p_dimensions)
		self.m_dimensions = p_dimensions
		self.m_halfDimensions = 0.5 * p_dimensions
		
		self.m_theta = math.pi * 0.5 #looking up so width and height make sense
		self.m_axisX = Vec2(math.cos(self.m_theta), math.sin(self.m_theta)) #atomic vectors i and j to determine the rotation
		self.m_axisY = Vec2(-math.sin(self.m_theta), math.cos(self.m_theta))

		self.m_dirty_geometry = True
		

	def draw(self):
		self.m_renderable.draw(WINDOW.m_screen, self.m_position, self.m_theta)

	def updateGeometry(self):
		if not self.m_dirty_geometry:
			return #no need to clean them leave state as is
		
		#generate vertices
		#print("Updating Geometry")
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
		