import pygame
from core.window import WINDOW
from core.vector import Vec2i
class ProgressBar:
	def __init__(
		self,
		p_position: Vec2i,
		p_size: Vec2i,
		p_borderSize: int,
		p_outterColor: tuple[int, int, int],
		p_middleColor: tuple[int, int, int],
		p_innerColor: tuple[int, int, int]
	):
		self._position: Vec2i = p_position
		self._size: Vec2i = p_size
		self._borderSize: int = p_borderSize
		self._outterColor: tuple[int, int, int] = p_outterColor
		self._middleColor: tuple[int, int, int] = p_middleColor
		self._innerColor: tuple[int, int, int] = p_innerColor
		
	def draw(self, p_percentage: float) -> None:
		#outter bar
		pygame.draw.rect(
			WINDOW.screen,
			self._outterColor,
			(
				self._position.x,
				self._position.y,
				self._size.x,
				self._size.y,
			)
		)

		#negative inner bar
		pygame.draw.rect(
			WINDOW.screen,
			self._middleColor,
			(
				self._position.x + self._borderSize,
				self._position.y + self._borderSize,
				(self._size.x - (2* self._borderSize)),
				self._size.y - (2 * self._borderSize),
			)
		)

		#inner bar
		pygame.draw.rect(
			WINDOW.screen,
			self._innerColor,
			(
				self._position.x + self._borderSize,
				self._position.y + self._borderSize,
				(self._size.x - (2* self._borderSize)) * p_percentage,
				self._size.y - (2 * self._borderSize),
			)
		)