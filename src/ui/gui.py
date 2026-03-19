import pygame
from core.vector import Vec2
from core.window import WINDOW

from ui.hud import HeadsUpDisplay
class GraphicalUserInterface:
	def __init__(
		self,
	):
		self._scale: Vec2 = Vec2( #all elements live in a noramlised rect IE 4K screen is 1.77:1 (16/9 : 1)
			WINDOW.width / WINDOW.height,
			1
		)
		pygame.font.init()

		self._HUD = HeadsUpDisplay()

	def draw(self):
		self._HUD.draw()

GUI = GraphicalUserInterface()
