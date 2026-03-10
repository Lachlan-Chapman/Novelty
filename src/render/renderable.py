import pygame
import math

from core.window import WINDOW
from core.vector import Vec2

class Renderable:
	def __init__(self):
		self._color = (255, 255, 0)

	def setColor(self, p_color) -> None:
		self._color = p_color

	def draw(self, p_position: Vec2, p_theta: float) -> None:
		pass #for invisible entities

class CircleRenderable(Renderable):
	def __init__(
		self,
		p_radius: float
	):
		Renderable.__init__(self)
		self._radius: float = p_radius

	def draw(self, p_position: Vec2, p_theta: float) -> None:
		pygame.draw.circle(
			WINDOW.screen,
			self._color,
			(int(p_position.x), int(p_position.y)),
			self._radius
		)

class RectangleRenderable(Renderable):
	def __init__(
			self,
			p_size: Vec2
		):
		Renderable.__init__(self)
		self._size: Vec2 = p_size

	def draw(self, p_position: Vec2, p_theta: float) -> None:
		surface = pygame.Surface(
			(
				int(self._size.x),
				int(self._size.y)
			),
			pygame.SRCALPHA
		)
		surface.fill(self._color)
		
		degrees = math.degrees(-p_theta)
		rotated_surface = pygame.transform.rotate(surface, degrees)
		rotated_rect = rotated_surface.get_rect(
			center = (
				int(p_position.x),
				int(p_position.y)
			)
		)
		WINDOW.screen.blit(
			source = rotated_surface,
			dest = rotated_rect
		)