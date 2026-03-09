from core.time import TIME
from core.window import WINDOW
from core.vector import Vec2
from core.transform import Transform

from entities.entity import KinematicEntity

class Munition(KinematicEntity):
	def __init__(
		self,
		p_position: Vec2,
		p_direction: Vec2,
		p_radius: float | None = None,
		p_damage: float | None = None,
		p_speed: float | None = None,
		p_penetrationLimit: int | None = None
	):
		self._position: Vec2 = p_position
		self._direction: float = p_direction
		self._radius: float = p_radius if p_radius is not None else 0.0
		self._damage: float = p_damage if p_damage is not None else 0.0
		self._speed: float = p_speed if p_speed is not None else 0.0
		self._penetrationLimit: int = p_penetrationLimit if p_penetrationLimit is not None else 0

	def updateTransform(self, p_transform: Transform) -> None:
		pass


#bullet type configuration
class Bullet(Munition):
	def __init__(self, p_position: Vec2, p_direction: Vec2):
		Munition.__init__(
			self,
			p_position = p_position,
			p_direction = p_direction,
			p_damage = 100.0,
			p_speed = 50.0,
			p_penetrationLimit = 1
		)

	def updateTransform(self, p_transform: Transform) -> None: #the traversal behaviour of our munition
		p_transform.position += p_transform.position * self._speed * TIME.deltaTime