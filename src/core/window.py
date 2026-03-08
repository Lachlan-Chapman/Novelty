import pygame
class Window:
	def __init__(
		self,
		p_width: int,
		p_height: int,
		p_name: str = "Novelty"
	):
		self.m_width: int = p_width
		self.m_height: int = p_height
		p_name: str = p_name

		self.m_screen = pygame.display.set_mode((p_width, p_height))
		pygame.display.set_caption(p_name)

WINDOW: Window = Window(
	p_width = 960,
	p_height = 540,
	p_name = "Novelty | Genisis"
)