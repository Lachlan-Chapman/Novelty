import math
from core.time import TIME
from core.vector import Vec2

from physics.collision import CircleCollider
from render.renderable import CircleRenderable

from entities.entity import Entity, Actor

from gameplay.weapon import Weapon

class Enemy(Actor):
	def __init__(
		self,
		p_position: Vec2,
		p_radius: float,
		p_speed: float,
		p_health: float,
		p_damage: float,
		p_target: Entity | None = None
	):
		self._target: Entity | None = p_target
		rotation = 0.0
		if p_target is not None:
			to_target = self.targetDirection(p_target)
			rotation = math.atan2(to_target.y, to_target.x)
		Actor.__init__(
			self,
			p_position = p_position,
			p_rotation = rotation,
			p_velocity = None,
			p_angularVelocity = None,
			p_health = p_health,
			p_damage = p_damage
		)
		self._transform.size = Vec2(30, 30)
		self._speed: float = p_speed
		self._collider = CircleCollider(30)
		self._renderer = CircleRenderable(30)

	def updatePosition(self) -> None:
		if self._target is not None:
			to_target = (self._target._transform.position - self._transform.position).unit
			self.offsetPosition(
				to_target * self._speed * TIME.deltaTime
			)
	
	def setTarget(self, p_target: Entity):
		self._target = p_target

	def targetDirection(self, p_target: Entity) -> Vec2:
		if self._target is None:
			return Vec2(0.0, 0.0)
		return (self._target._transform.position - p_target._transform.position).unit

