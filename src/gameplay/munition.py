from core.vector import Vec2
from entities.entity import KinematicEntity, Actor
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
		self._penetrationCount = 0

	def onCollisionEnter(self, p_other: Actor) -> None:
		p_other.damage()
		self._alive = False
class Bullet(Munition):
	def __init__(self, p_startPosition: Vec2, p_direction: Vec2):
		
		self.m_direction = p_direction

	def updatePosition(self):
		self.m_position += self.m_direction * self.m_speed * TIME.m_deltaTime
		if self.m_position.x <= 0 or self.m_position.x >= WINDOW.m_width:
			self.m_alive = False
		if self.m_position.y <= 0 or self.m_position.y >= WINDOW.m_height:
			self.m_alive = False

	def damage(self, p_damage):
		CircleEntity.damage(self, 1.0) #health is collision count so just strip away one collision

	