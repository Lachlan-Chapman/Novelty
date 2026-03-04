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

class RectangleRenderable(Renderable):
	def __init__(self, p_dimensions: Vec2):
		super().__init__()
		self.m_dimensions = p_dimensions

	def draw(self, p_screen, p_position: Vec2):
		pygame.draw.rect(
			p_screen,
			self.m_color,
			(
				p_position.x - self.m_dimensions.x * 0.5,
				p_position.y - self.m_dimensions.y * 0.5,
				self.m_dimensions.x, self.m_dimensions.y
			)
		)