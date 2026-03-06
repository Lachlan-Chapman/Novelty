from src.vector import Vec2
class Weapon:
	def __init__(self, p_name: str = "Weapon", p_bulletDamage: float = 10, p_bulletSpeed: float = 100.0, p_fireRate: float = 1.0,  p_magazineSize: int = 10.0, p_reloadTime: float = 3.0):
		self.m_name = p_name
		self.m_bulletSpeed = p_bulletSpeed
		self.m_fireRate = p_fireRate
		self.m_magazineSize = p_magazineSize
		self.m_bulletCount = p_magazineSize
		self.m_reloadTime = p_reloadTime


	def shoot(self, p_direction: Vec2):
		print(f"{self.m_name} Shoots")
		#raise NotImplementedError #child must create specific shoot, no default shots

from src.entity import Entity
from src.bullet import Projectile, Bullet
from src.entityRegistry import ENTITY_REGISTRY

class Pistol(Weapon):
	def __init__(self, p_projectile: Projectile):
		self.m_fireRate = 1.0
		self.m_magazineSize = 2.0
		self.m_reloadTime = 3.0
		self.m_projectile = p_projectile
	
	def shoot(self, p_shooter: Entity):
		projectile = self.m_projectile(
			p_shooter.m_position,
			p_shooter.getDirection()
		)
		projectile.ownedBy(p_shooter)
		ENTITY_REGISTRY.add(projectile)