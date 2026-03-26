import pygame
from core.vector import Vec2, Vec2i
from core.window import WINDOW
from core.time import TIME
from core.controls import BINDINGS, Actions

from ui.widgets import Text
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
		self._timerText = Text(
			p_position = Vec2i(10, 10),
			p_color = (255, 255, 255),
			p_fontSize= 36
		)

	def drawGameOver(self):
		game_over_text = Text(
			p_position = Vec2i(WINDOW.width/2, WINDOW.height/2),
			p_color = (255, 0, 0),
			p_fontSize = 50,
			p_text = "GAME OVER"
		)
		reset_text = Text(
			p_position = Vec2i(WINDOW.width/3, WINDOW.height * 2/3),
			p_color = (255, 0, 0),
			p_fontSize = 50,
			p_text = f"Press R To Reset"
		)
		exit_text = Text(
			p_position = Vec2i(WINDOW.width * 2/3, WINDOW.height * 2/3),
			p_color = (255, 0, 0),
			p_fontSize = 50,
			p_text = f"Press ESC To Exit"
		)
		game_over_text.draw()
		reset_text.draw()
		exit_text.draw()

	def draw(self):
		self._HUD.draw()
		self._timerText.setValue(f"{TIME._totalTime:.2f}s")
		self._timerText.draw()

GUI = GraphicalUserInterface()
