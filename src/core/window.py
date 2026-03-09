import pygame
class Window:
	def __init__(
		self,
		p_width: int,
		p_height: int,
		p_name: str = "Novelty"
	):
		self._width: int = p_width
		self._height: int = p_height
		self._name: str = p_name

		self.m_screen = pygame.display.set_mode((p_width, p_height))
		pygame.display.set_caption(p_name)

	@property
	def width(self) -> int:
		return self._width

	@property
	def height(self) -> int:
		return self._height
	
	@property
	def name(self) -> str:
		return self._name

WINDOW: Window = Window(
	p_width = 960,
	p_height = 540,
	p_name = "Novelty | Genisis"
)