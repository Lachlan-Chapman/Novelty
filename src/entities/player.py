import pygame
from pygame.key import ScancodeWrapper
import math

from core.vector import Vec2


from entities.entity import Entity, Actor
from gameplay.weapon import Weapon

from core.time import TIME
from core.window import WINDOW

from physics.collision import Collider, RectangleCollider
from render.renderable import Renderable, RectangleRenderable

from systems.armory import Armory

class Player(Actor):
	def __init__(
		self,
		p_health: float,
		p_damage: float,
		p_size: Vec2
	):
		Actor.__init__(
			self,
			p_position = Vec2(
				WINDOW.width // 2,
				WINDOW.height // 2
			),
			p_rotation = 0, #centered at the screen never translates
			p_velocity = Vec2(0.0, 0.0),
			p_angularVelocity = 0.0,
			p_health = p_health,
			p_damage = p_damage
		)

		self._collider: Collider = RectangleCollider(p_size)
		self._renderer: Renderable = RectangleRenderable(p_size)
		self._armory: Armory = Armory(p_maxWeaponCount = 3)

	def handleRotationInput(self, p_keys: ScancodeWrapper) -> None:
		theta = 0.0
		if p_keys[pygame.K_a]:
			theta -= self.m_rotationSpeed
		if p_keys[pygame.K_d]:
			theta += self.m_rotationSpeed
		self.offsetRotation(theta * TIME.deltaTime) #adjust to be rotating speed per second
		
		direction = Vec2(
			math.cos(self._transform.rotation),
			math.sin(self._transform.rotation)
		)
		self._armory.updateBarrel(
			p_position = self._transform.position + (direction * self._transform.size.magnitude * 1.25),
			p_direction = direction
		)

	def handleArmoryInput(self, p_keys: ScancodeWrapper) -> None:
		if p_keys[pygame.K_SPACE]:
			self._armory.shoot()
			if len(self.m_weapons) > 0:
				self.m_weapons[self.m_currentWeapon].shoot(self) #creates bullet from this position

	def handleInput(self, p_keys: ScancodeWrapper) -> None:
		#rotation
		self.handleRotationInput(p_keys)
		#shooting
		self.handleArmoryInput(p_keys)

	def draw(self):
		super().draw()
		self._armory._barrel.draw() #player has to handle the visual representation of the barrel



	