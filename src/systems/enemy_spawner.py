import random
import math

from core.time import TIME
from core.vector import Vec2
from core.utils import clamp

from entities.player import Player
from entities.enemy import Enemy

from gameplay.munition import Bullet
from gameplay.weapon import Weapon

from systems.entity_registry import ENTITY_REGISTRY

class EnemySpawner:
	def __init__(
		self,
		p_target: Player,
		p_spawnSpeed: float,
		p_spawnRadius: float
	):
		self._target: Player = p_target
		self._spawnRadius: float = p_spawnRadius

		self._spawnSpeed: float = p_spawnSpeed
		self._spawnFinish: bool = False
		self._spawnFinishTime: float = 0.0

		self._enemySpeed: float = 200.0

		self._spawnCount = 0
		
	def canSpawn(self) -> bool:
		self._spawnFinish = TIME.time >= self._spawnFinishTime
		return self._spawnFinish

	def spawnEnemy(self) -> bool:
		if not self.canSpawn():
			return False
		
		speed = self._enemySpeed * (self._spawnCount * 0.3)
		speed = clamp(speed, 20, speed)
		speed = self._enemySpeed

		self._spawnSpeed = clamp(
			self._spawnSpeed,
			2,
			1 / (self._spawnCount + 1)
		)

		random_theta = random.random() * math.tau
		spawn_location = self._target._transform.position + Vec2(
			math.cos(random_theta),
			math.sin(random_theta)
		) * self._spawnRadius
		ENTITY_REGISTRY.add(
			Enemy(
				p_position = spawn_location,
				p_radius = 20,
				p_speed = speed,
				p_health = 100.0,
				p_damage = 100.0,
				p_target = self._target
			)
		)
		self._spawnCount += 1
		self._spawnFinishTime = TIME.time + self._spawnSpeed
		return True