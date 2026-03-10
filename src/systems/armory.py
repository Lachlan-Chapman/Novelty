import math



from core.vector import Vec2
from core.transform import Transform

from physics.collision import Collider
from render.renderable import RectangleRenderable


from entities.entity import Entity
from entities.projectile import Projectile

from gameplay.weapon import Weapon
from gameplay.munition import Munition


from systems.entity_registry import ENTITY_REGISTRY

class Armory:
	def __init__(
		self,
		p_maxWeaponCount: int,
		p_weapons: list[Weapon] | None = None,
		p_barrelPosition: Vec2 | None = None,
		p_barrelDirection: Vec2 | None = None
	):
		self._maxWeaponCount = p_maxWeaponCount
		self._weapons: list[Weapon] = p_weapons if p_weapons is not None else []

		self._currentWeapon: int = 0
		self._ammo: dict[type[Munition], int]

		self._barrel: Entity = Entity(
			p_position = p_barrelPosition,
			p_rotation = math.atan2(p_barrelDirection.y, p_barrelDirection.x)
		)
		self._barrel._renderer = RectangleRenderable(
			p_size = Vec2(15.0, 10.0)
		)

	#UPDATE BARREL LOCATION
	def updateBarrel(self, p_position: Vec2, p_direction: Vec2):
		self._barrel._transform.position = p_position
		self._barrel._transform.rotation = math.atan2(p_direction.y, p_direction.x)
		self._barrel.draw()

	#UPDATE STORE
	def addAmmo(self, p_munition: type[Munition], p_amount: int) -> None:
		self._ammo[p_munition] = self._ammo.get(p_munition, 0) + p_amount

	def addWeapon(self, p_weapon: Weapon) -> None:
		if len(self._weapons) < self._maxWeaponCount:
			self._weapons.append(p_weapon)
	
	#WEAPON CYCLE
	def nextWeapon(self) -> None:
		self._currentWeapon = (self._currentWeapon + 1) % len(self._weapons)

	def previousWeapon(self) -> None:
		self._currentWeapon = (self._currentWeapon - 1) % len(self._weapons)

	#FIRING
	def shoot(
		self,
		p_ignoreColliders: set[Collider] | None = None
	) -> None:
		weapon = self._weapons[self._currentWeapon]
		if weapon.shoot(): #attemp shoot | if true, the weapon has shot and updated internall state
			direction = Vec2(math.cos(self._barrel.rotation), math.sin(self._barrel.rotation))
			projectile = Projectile(
				weapon.munition( #entity wrapper around munition config
					p_position = self._barrel.position,
					p_direction = direction
				),
				p_ignoreColliders = p_ignoreColliders
			)
			ENTITY_REGISTRY.add(projectile)
		
		if weapon.requestingReload and not weapon.reloading: #has the weapon exhasuted its magazine
			if self._ammo.get(weapon.munition, 0) > 0:  #do we have ammo in the armory to reload the gun with?
				self._ammo[weapon.munition] -= 1
				weapon.reload()

	#GETTERS
	@property
	def weapons(self) -> list[Weapon]:
		return self._weapons
	
	@property
	def ammo(self) -> dict[type[Munition], int]:
		return self._ammo

	@property
	def currentWeapon(self) -> Weapon | None:
		if len(self._weapons) == 0:
			return None
		return self._weapons[self._currentWeapon]
