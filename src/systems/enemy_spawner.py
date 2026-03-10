import random
import math
from core.vector import Vec2
from entities.player import Player
from gameplay.munition import Bullet
from gameplay.weapon import Weapon
from entities.enemy import Enemy
from systems.entity_registry import ENTITY_REGISTRY
from core.time import TIME
class EnemySpawner:
	def __init__(self, p_target: Player, p_spawnSpeed: float, p_spawnRadius: float):
		self.m_target = p_target
		self.m_spawnRadius = p_spawnRadius

		self.m_spawnSpeed = p_spawnSpeed
		self.m_finishSpawn = False
		self.m_spawnFinishTime = 0.0

		self.m_enemySpeed = 20.0
	def spawn(self):
		pass
		

	def spawnEnemy(self):
		self.m_finishSpawn = TIME.time >= self.m_spawnFinishTime
		if self.m_finishSpawn:
			random_theta = random.random() * math.tau
			spawn_location = self.m_target.m_position + Vec2(
				math.cos(random_theta),
				math.sin(random_theta)
			) * self.m_spawnRadius


			self.m_spawnFinishTime = TIME.time + self.m_spawnSpeed