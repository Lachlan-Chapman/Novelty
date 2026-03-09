import pygame
import math

from core.vector import Vec2
from entities.entity import RectangleEntity
from gameplay.weapon import Weapon

from core.time import TIME
from core.window import WINDOW

class Player(RectangleEntity):
	def __init__(self, p_position: Vec2, p_dimensions: Vec2, p_speed: float = 100, p_rotationSpeed: float = 0.5, p_health: float = 1000.0, p_damage: float = 0, p_maxWeaponCount: int = 3):
		RectangleEntity.__init__(
			self,
			p_position = p_position,
			p_dimensions = p_dimensions,
			p_speed = p_speed,
			p_rotationSpeed = p_rotationSpeed,
			p_health = p_health,
			p_damage = p_damage
		)
		self.m_maxWeaponCount = p_maxWeaponCount
		self.m_currentWeapon = 0
		self.m_weapons = []
		self.setRotation(math.tau * 0.75)

	def damage(self, p_damage):
		RectangleEntity.damage(self, p_damage = p_damage)
		if self.m_health <= 0:
			print(f"You Lasted: {TIME.m_totalTime}s")
	
	def addWeapon(self, p_weapon: Weapon):
		if len(self.m_weapons) < self.m_maxWeaponCount:
			p_weapon.ownedBy(self) #this entity now controls the guns position and things for rendering
			self.m_weapons.append(p_weapon)


	def move(self, p_keys):
		theta = 0.0
		#get keyboard input directions
		if p_keys[pygame.K_a]:
			theta -= self.m_rotationSpeed
		if p_keys[pygame.K_d]:
			theta += self.m_rotationSpeed
		theta *= TIME.m_deltaTime #adjust to be rotating speed per second
		theta_prime = self.m_theta + theta
		theta_prime = theta_prime % math.tau #wrap to be from [0, 2pi)

		self.setRotation(theta_prime)
	def shoot(self, p_keys):
		if p_keys[pygame.K_SPACE]:
			if len(self.m_weapons) > 0:
				self.m_weapons[self.m_currentWeapon].shoot(self) #creates bullet from this position


	def draw(self):
		RectangleEntity.draw(self) #draw player as normal
		#based on theta and position and size set the barrel location
		if len(self.m_weapons) > 0:
			weapon = self.m_weapons[self.m_currentWeapon]
			weapon.setPosition(self.m_position + self.getDirection() * self.m_dimensions.y) #creates bullet from this position
			weapon.setRotation(self.m_theta)
			weapon.draw()



	