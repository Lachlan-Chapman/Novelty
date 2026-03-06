import pygame

from src.vector import Vec2
from src.entity import RectangleEntity
from src.weapon import Weapon


from src.time import TIME
from src.window import WINDOW

class Player(RectangleEntity):
	def __init__(self, p_position: Vec2, p_dimensions: Vec2, p_speed: float = 100, p_health: float = 1000.0, p_damage: float = 0, p_maxWeaponCount: int = 3):
		super().__init__(
			p_position,
			p_dimensions,
			p_speed,
			p_health,
			p_damage
		)
		self.m_maxWeaponCount = p_maxWeaponCount
		self.m_currentWeapon = 0
		self.m_weapons = []
	
	def addWeapon(self, p_weapon: Weapon):
		if len(self.m_weapons) < self.m_maxWeaponCount:
			self.m_weapons.append(p_weapon)

	def move(self, p_keys):
		move = Vec2()
		#get keyboard input directions
		if p_keys[pygame.K_w]:
			move.y -= 1.0
		if p_keys[pygame.K_a]:
			move.x -= 1.0
		if p_keys[pygame.K_s]:
			move.y += 1.0
		if p_keys[pygame.K_d]:
			move.x += 1.0
		move *= self.m_speed * TIME.m_deltaTime
		move_prime = self.m_position + move
		if move_prime == self.m_position: #idk if float error will make this always false | but no movement shouldnt bother updating position and there on geometry
			return
		
		#screen boundary check using center only cuz shape isnt decided to add ether half dimensions or radius
		if move_prime.x < 0:
			move_prime.x = 0
		if move_prime.x > WINDOW.m_width:
			move_prime.x = WINDOW.m_width

		if move_prime.y < 0:
			move_prime.y = 0
		if move_prime.y > WINDOW.m_height:
			move_prime.y = WINDOW.m_height
		
		self.setPosition(move_prime) #go via this interface so it updates geometry 

	def shoot(self, p_keys):
		if p_keys[pygame.K_SPACE]:
			if len(self.m_weapons) > 0:
				self.m_weapons[self.m_currentWeapon].shoot(self) #creates bullet from this position




	