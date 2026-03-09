from gameplay.weapon import Weapon
from gameplay.munition import Munition
class Armory:
	def __init__(
		self,
		p_maxWeaponCount: int,
		p_weapons: list[Weapon] | None = None
	):
		self._maxWeaponCount = p_maxWeaponCount
		self._weapons: list[Weapon] = p_weapons if p_weapons is not None else []

		self._currentWeapon: int = 0
		self._ammo: dict[type[Munition], int]

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
	def shoot(self) -> None:
		self._weapons[self._currentWeapon].shoot()
 
	#GETTERS
	@property
	def weapons(self) -> list[Weapon]:
		return self._weapons
	
	def ammo(self) -> dict[type[Munition], int]:
		return self._ammo

	@property
	def currentWeapon(self) -> Weapon | None:
		if len(self._weapons) == 0:
			return None
		return self._weapons[self._currentWeapon]
