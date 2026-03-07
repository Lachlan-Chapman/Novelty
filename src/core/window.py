import pygame
class Window:
	def __init__(self, p_width: int, p_height: int, p_name: str = "Novelty"):
		self.m_width = p_width
		self.m_height = p_height
		self.m_screen = pygame.display.set_mode((p_width, p_height))
		pygame.display.set_caption("Pygame Heartbeat")

WINDOW = Window(
	p_width = 960,
	p_height = 540,
	p_name = "Novelty | Genisis"
)