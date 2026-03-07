from src.player import Player
from src.enemy import Enemy
class EnemySpawner:
	def __init__(self, p_target: Player):
		self.m_target = p_target

	def spawnEnemy(self, p_enemy: Enemy):
		pass