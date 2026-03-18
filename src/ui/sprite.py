SPRITE_PATH = "res/sprite"

import pygame
from core.window import WINDOW
from core.vector import Vec2

class Sprite:
	def __init__(
		self,
		p_path: str,
		p_position: Vec2,
		p_scale: float
	):
		self._image: pygame.Surface = pygame.image.load(p_path).convert_alpha()
		self._position = p_position
		self._scale = p_scale

	def draw(self):
		WINDOW.screen.blit(self._image, (int(self._position.x), int(self._position.y)))