
import math
from src.vector import Vec2
from src.entity import Entity, CircleEntity
from src.weapon import Weapon
from src.time import TIME
class Enemy(Entity):
	def __init__(self, p_target: Entity):
		self.m_target = p_target
	
	def target(self, p_target: Entity):
		self.m_target = p_target

class CircleEnemy(CircleEntity, Enemy):
	def __init__(
		self, 
		p_target: Entity,
		p_position: Vec2 = Vec2(0.0, 0.0),
		p_radius: float = 10,
		p_speed: float = 10,
		p_rotationSpeed: float = math.pi,
		p_health: float = 100.0,
		p_damage: float = 100.0

	):
		Enemy.target(self, p_target = p_target)
		CircleEntity.__init__(
			self,
			p_position = p_position,
			p_radius = p_radius,
			p_speed = p_speed,
			p_rotationSpeed = p_rotationSpeed,
			p_health = p_health,
			p_damage = p_damage
		)
		self.m_weapon = None

	def updatePosition(self): #moves toward target
		target_position = self.m_target.m_position.normalise()
		self.offsetPosition(
			target_position * self.m_speed * TIME.m_deltaTime
		)
	
	def updateRotation(self): #looks at target
		direction = self.m_target.m_position - self.m_position
		theta = math.atan2(direction.y, direction.x)
		self.setRotation(theta)

	def update(self):
		CircleEntity.update(self = self)
		self.shoot()
	
	
	def addWeapon(self, p_weapon: Weapon):
		p_weapon.ownedBy(self)
		self.m_weapon = p_weapon

	def shoot(self):
		if not self.m_weapon is None:
			self.m_weapon.shoot(self)

	


	