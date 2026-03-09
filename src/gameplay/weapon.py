from core.time import TIME
from gameplay.munition import Munition

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

	def shoot(self) -> bool:
		if not self.canShoot():
			return False
		
		self._isShooting = True
		self._shotFinish = TIME.time + self._shotCooldown
		self._bulletCount -= 1

		if self._bulletCount <= 0:
			self.reload()
		return True

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
	def reloading(self) -> bool:
		return self._isReloading

	@property 
	def shooting(self) -> bool:
		return self._isShooting