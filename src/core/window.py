import pygame
from core.console import CONSOLE
class Window:
	def __init__(
		self,
		p_width: int,
		p_height: int,
		p_name: str = "Novelty"
	):
		self._scalingOS: float = 1
		self._width: int = int(p_width * self._scalingOS)
		self._height: int = int(p_height * self._scalingOS)
		self._name: str = p_name


		self._screen: pygame.Surface = pygame.display.set_mode((self._width, self._height), pygame.RESIZABLE)
		CONSOLE.info(f"Game Window Initialized {self._screen.get_size()}")
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

	@property
	def screen(self) -> pygame.Surface:
		return self._screen

screen_size = pygame.display.Info()
WINDOW: Window = Window(
	p_width = screen_size.current_w // 1.5,
	p_height = screen_size.current_h // 1.5,
	p_name = "Novelty | Genisis"
)