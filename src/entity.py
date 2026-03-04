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

	def collideWith(self, p_other):
		did_collide = self.m_collider.overlaps(self, p_other)
		print(f"{self.m_shape} {did_collide} collided")
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

	def draw(self, p_screen):
		self.m_renderable.draw(p_screen, self.m_position, self.m_theta)

	def setRotation(self, p_theta: float): #rotation in radians
		self.m_theta = p_theta