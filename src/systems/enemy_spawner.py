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

		self._enemySpeed: float = 20.0
		
	def canSpawn(self) -> bool:
		self._spawnFinish = TIME.time >= self._spawnFinishTime
		return self._spawnFinish

	def spawnEnemy(self) -> bool:
		if not self.canSpawn():
			return False
		
		random_theta = random.random() * math.tau
		spawn_location = self._target._transform.position + Vec2(
			math.cos(random_theta),
			math.sin(random_theta)
		) * self._spawnRadius
		ENTITY_REGISTRY.add(
			Enemy(
				p_position = spawn_location,
				p_speed = 20,
				p_health = 100.0,
				p_damage = 100.0,
				p_target = self._target
			)
		)
		self._spawnFinishTime = TIME.time + self._spawnSpeed
		return True