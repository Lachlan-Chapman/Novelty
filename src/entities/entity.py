import pygame
import math

from core.window import WINDOW
from core.console import CONSOLE
from core.vector import Vec2

from physics.collision import Collider
from render.renderable import Renderable, CircleRenderable, RectangleRenderable

class Entity:
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float
	):
		self._position: Vec2 = p_position
		self._rotation: float = p_rotation
		
		self._id: int | None = None #used for collision pairing, ENTITY_REGISTRY sets this so only enetiies registerd will be apart of the actaul game

		self._collider: Collider | None = None
		self._renderable: Renderable | None = None
		self._dirtyGeometry = True

	def _set_id(self, p_id: int) -> None:
		if self._id is not None:
			CONSOLE.warn("Entity ID already set")
			return
		self._id = p_id

	#ROTATION SETTERS
	def setRotation(self, p_theta: float) -> None: #rotation in radians NEED TO CONVERT TO DEG if for some reason something requires it (pygame renderer)
		self._rotation = p_theta
		self._rotation = self._rotation % math.tau
		self._dirtyGeometry = True

	def offsetRotation(self, p_delta: float) -> None: #doesnt set but adds the delta rotation
		self.setRotation(self._rotation + p_delta)

	#POSITION SETTERS
	def setPosition(self, p_position: Vec2) -> None: #sets exact position in screen coordinates
		self._position = p_position
		self._dirtyGeometry = True

	def offsetPosition(self, p_delta: Vec2) -> None: #doesnt set but adds the direction
		self.setPosition(self._position + p_delta)

	#INTERNAL UPDATES
	def updateRotation(self) -> None: #for internally handled changes for AI or some function
		pass

	def updatePosition(self) -> None: #for if the entity has its own internal position handling IE AI or a projectile
		pass

	def update(self) -> None:
		self.updatePosition()
		self.updateRotation()

	#COLLISIONS
	def overlaps(self, p_other: "Entity") -> bool:
		if self._collider is None:
			CONSOLE.error("Entity collider not set")
			return False
		if p_other._collider is None:
			CONSOLE.error("Other entity collider not set")
			return False
		return self._collider.overlaps(p_other._collider)
	
	def onCollisionEnter(self, p_other: "Entity") -> None: #allows for custom handling on how to act with differnet entity collision combos IE bullet with ship and ship with bullet etc
		pass

	#RENDERING
	def draw(self) -> None:
		if self._renderable is not None:
			self._renderable.draw(self._position, self._rotation)

	#GETTERS
	@property
	def position(self) -> Vec2:
		return self._position
	
	@property
	def rotation(self) -> float:
		return self._rotation
	
	@property
	def id(self) -> int | None:
		return self._id

	#DEBUGGING
	def drawCollision(self) -> None:
		if self._collider is not None and self._renderable is not None:
			if self._collider.m_collisionCount > 0:
				self._renderable.setColor((0, 255, 0))
			else:
				self._renderable.setColor((255, 0, 0))

class CircleEntity(Entity): 
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float,
		p_health: float,
		p_damage: float,
		p_radius: float,
		p_speed: float = 100.0,
		p_rotationSpeed: float = 10,
	):
		Entity.__init__(
			self = self,
			p_position = p_position,
			p_rotation = p_rotation,
			p_health = p_health,
			p_damage = p_damage
		)
		self.m_radius: float = p_radius
		self.m_speed: float = p_speed
		self.m_renderable: Renderable = CircleRenderable(p_radius)

	def draw(self):
		self.m_renderable.draw(WINDOW.m_screen, self.m_position)

class RectangleEntity(Entity):
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float,
		p_health: float,
		p_damage: float,
		p_dimensions: Vec2,
		p_speed: float,
		p_rotationSpeed: float
	):
		Entity.__init__(
			self = self,
			p_position = p_position,
			p_rotation = p_rotation,
			p_health = p_health,
			p_damage = p_damage
		)

		self.m_dimensions = p_dimensions
		self.m_halfDimensions = 0.5 * p_dimensions
		self.m_renderable = RectangleRenderable(p_dimensions)
		
		self.m_theta = math.pi * 0.5 #looking up so width and height make sense
		self.m_axisX = Vec2(math.cos(self.m_theta), math.sin(self.m_theta)) #atomic vectors i and j to determine the rotation
		self.m_axisY = Vec2(-math.sin(self.m_theta), math.cos(self.m_theta))

		

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
		