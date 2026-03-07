from src.vector import Vec2
from src.time import TIME
from src.entity import Entity, RectangleEntity
from src.bullet import Projectile, Bullet
class Weapon(RectangleEntity):
	def __init__(self, p_name: str = "Weapon", p_projectile: Projectile = Bullet, p_shootSpeed: float = 1.0,  p_magazineSize: int = 10.0, p_reloadSpeed: float = 3.0):
		super().__init__(
			p_position = Vec2(0.0, 0.0),
			p_dimensions = Vec2(5.0, 10.0)
		)
		self.m_name = p_name

		self.m_projectile = p_projectile

		self.m_shootSpeed = p_shootSpeed
		self.m_finishedShooting = False
		self.m_shootFinishTime = 0.0

		self.m_magazineSize = p_magazineSize
		self.m_bulletCount = p_magazineSize

		self.m_reloadSpeed = p_reloadSpeed #how long to reload
		self.m_finishedReloading = False
		self.m_reloadFinishTime = 0.0
		
		self.m_collider.canCollide(False) #purely visual, for the time being no collision | entity registry has no concept of barrel, its on the player to render and handle

	#in case custom weapons need to created on the fly
	def configure(self, p_name: str, p_shootSpeed: float, p_magazineSize: int, p_reloadSpeed):
		self.m_name = p_name
		self.m_shootSpeed = p_shootSpeed
		self.m_magazineSize = p_magazineSize
		self.m_reloadSpeed = p_reloadSpeed
	def reload(self):
		self.m_reloadFinishTime = TIME.m_totalTime + self.m_reloadSpeed
		self.m_bulletCount = self.m_magazineSize

	def shoot(self, p_shooter: Entity):
		#make these local if no need to debug
		self.m_finishedReloading = TIME.m_totalTime >= self.m_reloadFinishTime
		self.m_finishedShooting = TIME.m_totalTime >= self.m_shootFinishTime
		if self.m_finishedReloading and self.m_finishedShooting:
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

class Pistol(Weapon): #default config for pistol
	def __init__(self):
		super().__init__(
			p_name = "Pistol",
			p_projectile = Bullet,
			p_shootSpeed = 1,
			p_magazineSize = 2,
			p_reloadSpeed = 3
		)
	
	
			