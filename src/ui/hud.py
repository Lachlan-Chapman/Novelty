import pygame
from entities.player import PLAYER
from core.vector import Vec2
from ui.progress_bar import ProgressBar
from core.utils import toScreenSpace
class HeadsUpDisplay:
	def __init__(self):

		self._healthBar: ProgressBar = ProgressBar(
			p_position = toScreenSpace(Vec2(0.05, 0.05)),
			p_size = toScreenSpace(Vec2(0.2, 0.05)),
			p_borderSize = toScreenSpace(0.006),
			p_outterColor = (255, 255, 255),
			p_middleColor = (255, 0, 0),
			p_innerColor = (0, 255, 0)
		)

	def drawHealth(self) -> None:
		health_percentage = PLAYER.health / PLAYER.maxHealth
		self._healthBar.draw(health_percentage)

	def draw(self) -> None:
		self.drawHealth()

