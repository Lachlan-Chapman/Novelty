import pygame
import math

from core.vector import Vec2
from core.utils import toDegrees
from core.window import WINDOW

to_degrees = 180 / math.pi

class Renderable:
	def __init__(self):
		self.m_color = (255, 255, 0)

	def setColor(self, p_color):
		self.m_color = p_color

	def draw(self, p_position: Vec2, p_theta: float):
		pass #for invisible entities

class CircleRenderable(Renderable):
	def __init__(self, p_radius: float):
		Renderable.__init__(self = self)
		self.m_radius = p_radius

	def draw(self, p_position: Vec2, p_theta: float ):
		pygame.draw.circle(
			WINDOW.m_screen,
			self.m_color,
			(int(p_position.x), int(p_position.y)),
			self.m_radius
		)

class RectangleRenderable(Renderable):
	def __init__(self, p_dimensions: Vec2):
		Renderable.__init__(self = self)
		self.m_dimensions = p_dimensions

	def draw(self, p_position: Vec2, p_theta: float):
		dimensions = Vec2(
			int(self.m_dimensions.x),
			int(self.m_dimensions.y)
		)
		surface = pygame.Surface((dimensions.x, dimensions.y), pygame.SRCALPHA)
		surface.fill(self.m_color)
		
		degrees = toDegrees(-p_theta)

		rotated_surface = pygame.transform.rotate(surface, degrees)
		rotated_rect = rotated_surface.get_rect(
			center = (
				int(p_position.x),
				int(p_position.y)
			)
		)
		WINDOW.m_screen.blit(rotated_surface, rotated_rect)