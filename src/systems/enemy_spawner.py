import random
import math
from core.vector import Vec2
from entities.player import Player
from entities.bullet import Bullet
from gameplay.weapon import Weapon
from entities.enemy import Enemy, CircleEnemy
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
		
		if self.m_finishSpawn:
			enemy = CircleEnemy(
				p_target = self.m_target
			)
			enemy.addWeapon(p_weapon = Weapon(

			))
			self.spawnEnemy(CircleEnemy)

			enemy = CircleEnemy(
				None
			)
		enemy_weapon = Weapon(
			"Enemy Turret",
			p_shootSpeed = 1,
			p_magazineSize = 5,
			p_reloadSpeed = 0 #once out of ammo thats it defined by the shoot function
		)
		

	def spawnEnemy(self):
		self.m_finishSpawn = TIME.time >= self.m_spawnFinishTime
		if self.m_finishSpawn:
			random_theta = random.random() * math.tau
			spawn_location = self.m_target.m_position + Vec2(
				math.cos(random_theta),
				math.sin(random_theta)
			) * self.m_spawnRadius

			
			self.m_spawnSpeed *= 0.95 #decrease exponentially since it self referential
			if self.m_spawnSpeed < 0.25:
				self.m_spawnSpeed = 0.25
			enemy = CircleEnemy(
				p_target = self.m_target,
				p_position = spawn_location,
				p_speed = self.m_enemySpeed
			)
			self.m_enemySpeed *= 1.0085


			enemy.addWeapon(Weapon(
				p_name = "Enemy Turret",
				p_projectile = Bullet,
				p_shootSpeed = 0,
				p_magazineSize = 0, #no shooting capabilities rn
				p_reloadSpeed = 5
			))
			ENTITY_REGISTRY.add(enemy)

			self.m_spawnFinishTime = TIME.time + self.m_spawnSpeed