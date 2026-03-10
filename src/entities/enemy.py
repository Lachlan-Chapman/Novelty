import math
from core.vector import Vec2
from entities.entity import Entity
from gameplay.weapon import Weapon
from core.time import TIME
class Enemy(Entity):
	def __init__(self, p_target: Entity):
		self.m_target = p_target
	
	def target(self, p_target: Entity):
		self.m_target = p_target