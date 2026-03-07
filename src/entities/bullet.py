from src.vector import Vec2
from src.entity import Entity, CircleEntity
from src.time import TIME
from src.window import WINDOW
class Projectile:
	def __init__(self, p_type: str = "base"):
		self.m_type = p_type

	def updatePosition(self): #bullet handles it own position setting. other entities should spawn it and then forget about it
		raise NotImplementedError


class Bullet(CircleEntity, Projectile):
	def __init__(self, p_startPosition: Vec2, p_direction: Vec2):
		CircleEntity.__init__(
			self,
			p_position = p_startPosition,
			p_radius = 5,
			p_speed = 200,
			p_health = 1,
			p_damage = 100.0
		)

		Projectile.__init__(
			self,
			p_type = "bullet",
		)

		self.m_direction = p_direction

	def updatePosition(self):
		self.m_position += self.m_direction * self.m_speed * TIME.m_deltaTime
		if self.m_position.x <= 0 or self.m_position.x >= WINDOW.m_width:
			self.m_alive = False
		if self.m_position.y <= 0 or self.m_position.y >= WINDOW.m_height:
			self.m_alive = False

	def damage(self, p_damage):
		CircleEntity.damage(self, 1.0) #health is collision count so just strip away one collision

	