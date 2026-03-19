import pygame
from entities.player import PLAYER
from core.vector import Vec2
from ui.widgets import ProgressBar, Text
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

		self._weaponText: Text = Text(
			p_position = toScreenSpace(Vec2(0.05, 0.95)),
			p_size = toScreenSpace(Vec2(0, 0)),
			p_color = (255, 255, 255),
			p_font = None,
			p_fontSize = 40
		)

	def drawHealth(self) -> None:
		self._healthBar.setValue(PLAYER.health / PLAYER.maxHealth)
		self._healthBar.draw()

	def drawArmory(self) -> None:
		current_weapon = PLAYER._armory.currentWeapon
		weapon_name = current_weapon.__class__.__name__
		magazine = current_weapon.bullets
		stockpile = PLAYER._armory.ammo[current_weapon._munition]
		self._weaponText.setValue(f"{weapon_name}: {magazine}/{stockpile}")
		self._weaponText.draw()

	def draw(self) -> None:
		self.drawHealth()
		self.drawArmory()

