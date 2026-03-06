from src.vector import Vec2
from src.entity import CircleEntity
class Bullet(CircleEntity):
	def __init__(self, p_startPosition: Vec2, p_direction: Vec2, p_damage: float, p_speed: float, p_penetration: float = 2):
		super().__init__(p_startPosition, p_speed, p_penetration, p_damage)
		self.m_direction = p_direction #should be normalised | relying on caller to do that step as direction calcualations may be normalised inherintly
		
	def takeDamage(self, p_damage):
		self.m_health -= 1 #treating health as collision count so bullets pass through m_health objects before dying

	def updatePosition(self, p_deltaTime): #bullet handles it own position setting. other entities should spawn it and then forget about it
		self.m_position += self.m_direction * p_deltaTime

	