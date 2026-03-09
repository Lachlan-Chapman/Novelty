from core.vector import Vec2
from entities.entity import KinematicEntity, Entity, Actor
from core.time import TIME
from core.window import WINDOW

class Munition(KinematicEntity):
	def __init__(
		self,
		p_damage: float,
		p_speed: float,
		p_penetrationLimit: int = 1
	):
		self._damage: float = p_damage
		self._speed: float = p_speed
		self._penetrationLimit: int = p_penetrationLimit

	def onCollisionEnter(self, p_other: Entity) -> None:
		if isinstance(p_other, Actor):
			p_other.applyDamage(self._damage)
		self._alive = False

#bullet type configuration
class Bullet(Munition):
	def __init__(self, p_position: Vec2, p_direction: Vec2):
		Munition.__init__(
			self,
			p_damage = 100.0,
			p_speed = 50.0,
			p_penetrationLimit = 1
		)
		self._position: Vec2 = p_position
		self._direction: Vec2 = p_direction

	def updatePosition(self):
		self._position += self._position * self._speed * TIME.deltaTime
		if self._position.x <= 0 or self._position.x >= WINDOW.m_width:
			self.m_alive = False
		if self._position.y <= 0 or self._position.y >= WINDOW.m_height:
			self.m_alive = False

	def penetrated(self):
		self._penetrationLimit -= 1