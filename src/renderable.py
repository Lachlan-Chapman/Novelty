import pygame
from src.vector import Vec2
class Renderable:
	def __init__(self):
		self.m_color = (255, 255, 0)

	def setColor(self, p_color):
		self.m_color = p_color

class CircleRenderable(Renderable):
	def __init__(self, p_radius: float):
		super().__init__()
		self.m_radius = p_radius

	def draw(self, p_screen, p_position: Vec2):
		pygame.draw.circle(
			p_screen,
			self.m_color,
			(int(p_position.x), int(p_position.y)),
			self.m_radius
		)

import math
class RectangleRenderable(Renderable):
	def __init__(self, p_dimensions: Vec2):
		super().__init__()
		self.m_dimensions = p_dimensions

	def draw(self, p_screen, p_position: Vec2, p_theta: float):
		dimensions = Vec2(
			int(self.m_dimensions.x),
			int(self.m_dimensions.y)
		)
		surface = pygame.Surface((dimensions.x, dimensions.y), pygame.SRCALPHA)
		surface.fill(self.m_color)
		angle_deg = -(p_theta - math.pi * 0.5) * 57.29577951308232 #pygame uses degs for some reaso | ALSO pygame treats 0 degrees as upright?? not to the right?? so we have to offset so it makes sense. in screen coords going theta 0 -> 2pi it should rotate clockwise cuz y is down
		rotated_surface = pygame.transform.rotate(surface, angle_deg)
		rotated_rect = rotated_surface.get_rect(
			center = (
				int(p_position.x),
				int(p_position.y)
			)
		)
		p_screen.blit(rotated_surface, rotated_rect)