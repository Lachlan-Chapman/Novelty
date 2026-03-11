import math
from core.time import TIME

from physics.collision import Collider

from entities.entity import Entity
from entities.enemy import Enemy
from entities.projectile import Projectile, BulletProjectile, MisslieProjectile

from gameplay.munition import Munition, Bullet, Missile
from systems.entity_registry import ENTITY_REGISTRY


class Weapon:
	def __init__(
		self,
		p_munition: type[Munition],
		p_magazineSize: int,
		p_shotCooldown: float,
		p_reloadSpeed: float
	):
		self._munition: type[Munition] = p_munition
		self._magazineSize = p_magazineSize
		self._bulletCount: int = p_magazineSize

		#how long to wait for each event to finish
		self._reloadSpeed: float = p_reloadSpeed
		self._shotCooldown: float = p_shotCooldown

		#state trackers
		self._isReloading: bool = False
		self._isShooting: bool = False

		#global time when these events finish
		self._reloadFinish: float = 0.0
		self._shotFinish: float = 0.0

	def reload(self) -> None:
		self._isReloading = True
		self._reloadFinish = TIME.time + self._reloadSpeed
		self._bulletCount = self._magazineSize

	def canShoot(self) -> bool:
		self._isReloading = TIME.time < self._reloadFinish
		self._isShooting = TIME.time < self._shotFinish
		return(
			not self._isReloading
			and not self._isShooting
			and self._bulletCount > 0
		)
	
	def createProjectile(self, p_barrel: Entity, p_ignoreColliders: list[Collider]) -> Projectile:
		pass


	def shoot(self, p_barrel: Entity, p_friendlies: list[Collider]) -> Projectile | None:
		if not self.canShoot():
			return None

		self._isShooting = True
		self._shotFinish = TIME.time + self._shotCooldown
		self._bulletCount -= 1

		return self.createProjectile(
			p_barrel = p_barrel,
			p_ignoreColliders = p_friendlies
		)

	#GETTERS to return currently tracked state
	@property
	def bullets(self) -> int:
		return self._bulletCount
	
	@property
	def magazine(self) -> int:
		return self._magazineSize
	@property
	def munition(self) -> type[Munition]:
		return self._munition
	
	@property
	def requestingReload(self):
		return self._bulletCount <= 0
	
	@property
	def reloading(self) -> bool:
		return self._isReloading

	@property 
	def shooting(self) -> bool:
		return self._isShooting

class Pistol(Weapon):
	def __init__(
		self,
		p_magazineSize: int,
		p_shotCooldown: float,
		p_reloadSpeed: float,
		p_targetFOV: float
	):
		Weapon.__init__(
			self,
			p_munition = Bullet,
			p_magazineSize = p_magazineSize,
			p_shotCooldown = p_shotCooldown,
			p_reloadSpeed = p_reloadSpeed
		)
		self._targetFOV = p_targetFOV

	def findTarget(self, p_barrel: Entity) -> Projectile | None:
		target: Enemy | None = None
		
		enemies = ENTITY_REGISTRY.getEntities(Enemy)
		closest_distance = float("inf")
		for enemy in enemies: #get all enemies that are within the FOV
			to_enemy = enemy.position - p_barrel.position
			alignment = p_barrel.direction.dot(to_enemy.unit)
			
			if alignment >= math.cos(self._targetFOV / 2):
				enemy_distance = to_enemy.magnitude
				if enemy_distance < closest_distance: #store closest enemy within the FOV
					closest_distance = enemy_distance
					target = enemy
		return target
	
	def createProjectile(self, p_barrel: Entity, p_ignoreColliders: list[Collider]) -> Projectile:
		return BulletProjectile(
			p_position = p_barrel.position,
			p_direction = p_barrel.direction,
			p_ignoreColliders = p_ignoreColliders
		)

	def shoot(self, p_barrel: Entity, p_friendlies: list[Collider]) -> Projectile | None:
		return super().shoot(
			p_barrel = p_barrel,
			p_friendlies = p_friendlies
		)



#missile launcher finds target
#creates the missile projectile with targeting
#uses the missile munition config to control the targeting behaviour
class MissileLauncher(Weapon):
	def __init__(
		self,
		p_munition: type[Munition],
		p_magazineSize: int,
		p_shotCooldown: float,
		p_reloadSpeed: float,
		p_targetFOV: float
	):
		Weapon.__init__(
			self,
			p_munition = p_munition,
			p_magazineSize = p_magazineSize,
			p_shotCooldown = p_shotCooldown,
			p_reloadSpeed = p_reloadSpeed
		)
		self._targetFOV = p_targetFOV

	def findTarget(self, p_barrel: Entity) -> Projectile | None:
		target: Enemy | None = None
		
		enemies = ENTITY_REGISTRY.getEntities(Enemy)
		closest_distance = float("inf")
		for enemy in enemies: #get all enemies that are within the FOV
			to_enemy = enemy.position - p_barrel.position
			alignment = p_barrel.direction.dot(to_enemy.unit)
			
			if alignment >= math.cos(self._targetFOV / 2):
				enemy_distance = to_enemy.magnitude
				if enemy_distance < closest_distance: #store closest enemy within the FOV
					closest_distance = enemy_distance
					target = enemy
		return target
	
	def createProjectile(self, p_barrel, p_ignoreColliders):
		return MisslieProjectile(
			p_target = self.findTarget(p_barrel),
			p_position = p_barrel.position,
			p_rotation = p_barrel.rotation,
			p_direction = p_barrel.direction,
			p_ignoreColliders = p_ignoreColliders
		)

	def shoot(self, p_barrel: Entity, p_friendlies: list[Collider]) -> Projectile | None:
		return super().shoot(
			p_barrel = p_barrel,
			p_friendlies = p_friendlies
		)
