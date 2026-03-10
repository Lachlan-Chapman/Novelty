import math
from core.time import TIME
from core.window import WINDOW
from core.vector import Vec2

from physics.collision import Collider, CircleCollider
from render.renderable import CircleRenderable

from entities.entity import Entity, Actor
from gameplay.munition import Munition

class Projectile(Actor):
	def __init__(
		self,
		p_munition: Munition,
		p_ignoreColliders: set[Collider] | None = None
	):
		Actor.__init__(
			self,
			p_position = p_munition._position,
			p_rotation = math.atan2(p_munition._direction.y, p_munition._direction.x),
			p_velocity = p_munition._speed,
			p_angularVelocity = 0.0,
			p_health = p_munition._penetrationLimit,
			p_damage = p_munition._damage
		)
		self._transform.size = Vec2(p_munition._radius, p_munition._radius)
		self._direction = p_munition._direction

		self._traversalBehaviour = p_munition.updateTransform

		self._collider = CircleCollider(
			p_radius = p_munition._radius,
			p_ignoreColliders = p_ignoreColliders
		)

		self._renderer = CircleRenderable(p_munition._radius)
		

	def update(self) -> None: #travel along the initial direction
		self._traversalBehaviour(self._transform) #use the bound munitions instance to update the bullet
		
		#then the entity itself handles if its in a valid spot etc
		if self._transform.position.x <= 0 or self._transform.position.x >= WINDOW.width:
			self.m_alive = False
		if self._transform.position.y <= 0 or self._transform.position.y >= WINDOW.height:
			self.m_alive = False

	def onCollisionEnter(self, p_other: Entity) -> None:
		if isinstance(p_other, Actor):
			p_other.applyDamage(self._damage)
			self.applyDamage(1) #removes one from the amount of times it can collide again
