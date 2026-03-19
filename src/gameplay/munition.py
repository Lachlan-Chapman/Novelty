import math

from core.time import TIME
from core.window import WINDOW
from core.vector import Vec2
from core.transform import Transform

class Munition:
	def __init__(
		self,
		p_radius: float | None = None,
		p_damage: float | None = None,
		p_speed: float | None = None,
		p_penetrationLimit: int | None = None
	):
		self._radius: float = p_radius if p_radius is not None else 0.0
		self._damage: float = p_damage if p_damage is not None else 0.0
		self._speed: float = p_speed if p_speed is not None else 0.0
		self._penetrationLimit: int = p_penetrationLimit if p_penetrationLimit is not None else 0

	def traversalBehaviour(self, p_transform: Transform) -> Vec2:
		return Vec2(0.0, 0.0)

	@property
	def radius(self) -> float:
		return self._radius
	
	@property
	def damage(self) -> float:
		return self._damage
	
	@property
	def speed(self) -> float:
		return self._speed
	
	@property
	def penetrationLimit(self) -> int:
		return self._penetrationLimit

#munition configurations
class Bullet(Munition):
	def __init__(self):
		Munition.__init__(
			self,
			p_radius = 2.5,
			p_damage = 100.0,
			p_speed = 550.0,
			p_penetrationLimit = 1
		)

class Missile(Munition):
	def __init__(self):
		Munition.__init__(
			self,
			p_radius = 7.5,
			p_damage = 50.0,
			p_speed = 450.0,
			p_penetrationLimit = 1
		)

class Pellet(Munition):
	def __init__(self):
		Munition.__init__(
			self,
			p_radius = 4,
			p_damage = 100.0 / 7, #7 pellets defined hardcoded here | not great
			p_speed = 500.0,
			p_penetrationLimit = 1
		)