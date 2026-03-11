import math
from core.utils import randomRange
from core.time import TIME
from core.vector import Vec2
from physics.collision import Collider
from render.renderable import LineRenderable

from entities.entity import Entity
from entities.enemy import Enemy
from entities.projectile import Projectile, BulletProjectile, MisslieProjectile, PelletProjectile

from gameplay.munition import Munition, Bullet, Missile, Pellet
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

		self._debugRenderable = LineRenderable(
			p_magnitude = 200.0,
			p_width = 2.0
		)

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
	
	def createProjectile(self, p_barrel: Entity, p_ignoreColliders: list[Collider]) -> list[Projectile]:
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

	def debugDraw(self, p_barrel: Entity) -> None:
		self._debugRenderable.draw(p_barrel.position, p_barrel.rotation)

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
	
	def createProjectile(self, p_barrel: Entity, p_ignoreColliders: list[Collider]) -> list[Projectile]:
		return [BulletProjectile(
			p_position = p_barrel.position,
			p_direction = p_barrel.direction,
			p_ignoreColliders = p_ignoreColliders
		)]

	def shoot(self, p_barrel: Entity, p_friendlies: list[Collider]) -> Projectile | None:
		return super().shoot(
			p_barrel = p_barrel,
			p_friendlies = p_friendlies
		)

class MissileLauncher(Weapon):
	def __init__(
		self,
		p_magazineSize: int,
		p_shotCooldown: float,
		p_reloadSpeed: float,
		p_targetFOV: float
	):
		Weapon.__init__(
			self,
			p_munition = Missile,
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
	
	def createProjectile(self, p_barrel, p_ignoreColliders) -> list[Projectile]:
		return [MisslieProjectile(
			p_target = self.findTarget(p_barrel),
			p_position = p_barrel.position,
			p_rotation = p_barrel.rotation,
			p_direction = p_barrel.direction,
			p_ignoreColliders = p_ignoreColliders
		)]
	
	def debugDraw(self, p_barrel: Entity) -> None:
		super().debugDraw(p_barrel)
		half_theta = self._targetFOV / 2
		left_theta = p_barrel.rotation - half_theta
		right_theta = p_barrel.rotation + half_theta
		self._debugRenderable.draw(p_barrel.position, left_theta)
		self._debugRenderable.draw(p_barrel.position, right_theta)
		
	
	def shoot(self, p_barrel: Entity, p_friendlies: list[Collider]) -> Projectile | None:
		return super().shoot(
			p_barrel = p_barrel,
			p_friendlies = p_friendlies
		)

class Shotgun(Weapon):
	def __init__(
		self,
		p_magazineSize: int,
		p_shotCooldown: float,
		p_reloadSpeed: float,
		p_spreadAngle: float,
		p_pelletCount: int
	):
		Weapon.__init__(
			self,
			p_munition = Pellet,
			p_magazineSize = p_magazineSize,
			p_shotCooldown = p_shotCooldown,
			p_reloadSpeed = p_reloadSpeed
		)
		self._spreadAngle = p_spreadAngle
		self._pelletCount = p_pelletCount

	def createProjectile(self, p_barrel, p_ignoreColliders) -> list[Projectile]:
		pellets = []
		half_theta = self._spreadAngle / 2
		
		ignore_pellets = set(p_ignoreColliders) if p_ignoreColliders is not None else set()
		for _i in range(self._pelletCount):
			theta = randomRange(
				p_min = p_barrel.rotation - half_theta,
				p_max = p_barrel.rotation + half_theta
			)
			direction = Vec2(math.cos(theta), math.sin(theta))
			pellet = PelletProjectile(
				p_position = p_barrel.position,
				p_rotation = None,
				p_direction = direction,
				p_ignoreColliders = ignore_pellets
			)
			ignore_pellets.add(pellet.collider)
			pellets.append(
				pellet
			)
		return pellets
	
	def debugDraw(self, p_barrel: Entity) -> None:
		super().debugDraw(p_barrel)
		half_theta = self._spreadAngle / 2
		left_theta = p_barrel.rotation - half_theta
		right_theta = p_barrel.rotation + half_theta
		self._debugRenderable.draw(p_barrel.position, left_theta)
		self._debugRenderable.draw(p_barrel.position, right_theta)
		
	
	def shoot(self, p_barrel: Entity, p_friendlies: list[Collider]) -> Projectile | None:
		return super().shoot(
			p_barrel = p_barrel,
			p_friendlies = p_friendlies
		)