import pygame
from core.window import WINDOW
from core.vector import Vec2i
from core.utils import toScreenSpace

class Widget:
	def __init__(
		self,
		p_position: Vec2i,
		p_size: int,
		p_value: str | int | float | None = None
	):
		self._position: Vec2i = p_position
		self._size: int = p_size
		self._value: str | int | float | None = p_value

	def setValue(self, p_value: str | int | float) -> None:
		self._value = p_value
	
	def draw(self) -> None:
		pass

class Sprite(Widget):
	def __init__(
		self,
		p_position: Vec2i,
		p_size: int,
		p_path: str
	):
		Widget.__init__(
			self,
			p_position = p_position,
			p_size = p_size,
			p_value = p_path
		)
		self._image: pygame.Surface = pygame.image.load(p_path).convert_alpha()

	def draw(self):
		WINDOW.screen.blit(self._image, self._position.tuple)


class Text(Widget):
	def __init__(
		self,
		p_position: Vec2i,
		p_size: int,
		p_color: tuple[int, int, int],
		p_font: str | None = None,
		*,
		p_fontSize: int,
		p_text: str | None = None,
	):
		Widget.__init__(
			self,
			p_position = p_position,
			p_size = p_size,
			p_value = p_text
		)
		self._color = p_color
		self._font: pygame.Font = pygame.font.SysFont(p_font, p_fontSize)
		self._value: str = self._value if self._value is not None else ""
	
	def draw(self) -> None:
		text_surface = pygame.font.render(self._value, True, self._color)
		WINDOW.screen.blit(text_surface, self._position.tuple)



class ProgressBar(Widget):
	def __init__(
		self,
		p_position: Vec2i,
		p_size: Vec2i,
		p_borderSize: int,
		p_outterColor: tuple[int, int, int],
		p_middleColor: tuple[int, int, int],
		p_innerColor: tuple[int, int, int]
	):
		Widget.__init__(
			self,
			p_position = p_position,
			p_size = p_size
		)
		self._borderSize: int = p_borderSize
		self._outterColor: tuple[int, int, int] = p_outterColor
		self._middleColor: tuple[int, int, int] = p_middleColor
		self._innerColor: tuple[int, int, int] = p_innerColor
		
	def draw(self) -> None:
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
				(self._size.x - (2* self._borderSize)) * self._value,
				self._size.y - (2 * self._borderSize),
			)
		)