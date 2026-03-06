from src.vector import Vec2
from src.time import TIME
from src.entity import Entity
class Weapon:
	def __init__(self, p_name: str = "Weapon", p_shootSpeed: float = 1.0,  p_magazineSize: int = 10.0, p_reloadSpeed: float = 3.0):
		self.m_name = p_name

		self.m_shootSpeed = p_shootSpeed
		self.m_finishedShooting = False
		self.m_shootFinishTime = 0.0

		self.m_magazineSize = p_magazineSize
		self.m_bulletCount = p_magazineSize

		self.m_reloadSpeed = p_reloadSpeed #how long to reload
		self.m_finishedReloading = False
		self.m_reloadFinishTime = 0.0

	def reload(self):
		self.m_reloadFinishTime = TIME.m_totalTime + self.m_reloadSpeed
		self.m_bulletCount = self.m_magazineSize
		print(f"Finish Reloading @ {self.m_reloadFinishTime}")

	def shoot(self, p_shooter: Entity):
		#make these local if no need to debug
		self.m_finishedReloading = TIME.m_totalTime >= self.m_reloadFinishTime
		self.m_finishedShooting = TIME.m_totalTime >= self.m_shootFinishTime
		if self.m_finishedReloading and self.m_finishedShooting:
			print(f"{p_shooter.__class__.__name__} Shoots")
			self.m_shootFinishTime = TIME.m_totalTime + self.m_shootSpeed
			self.m_bulletCount -= 1 #we shot so our magazine now drops

			#create and register whatever we are shooting
			projectile = self.m_projectile(
				p_shooter.m_position,
				p_shooter.getDirection()
			)
			projectile.ownedBy(p_shooter)
			ENTITY_REGISTRY.add(projectile)
		if self.m_bulletCount <= 0:
			self.reload()

from src.entity import Entity
from src.bullet import Projectile, Bullet
from src.entityRegistry import ENTITY_REGISTRY

class Pistol(Weapon):
	def __init__(self, p_projectile: Projectile):
		super().__init__(
			"Pistol",
			p_shootSpeed = 1,
			p_magazineSize = 2,
			p_reloadSpeed = 3
		)
		self.m_projectile = p_projectile
	
	
			