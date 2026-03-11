import math
from core.time import TIME
from core.window import WINDOW
from core.vector import Vec2

from physics.collision import Collider, CircleCollider
from render.renderable import CircleRenderable

from entities.entity import Entity, Actor
from gameplay.munition import Munition

#wrapper around munition children types into a fluid entity type
class Projectile(Actor):
	def __init__(
		self,
		p_munition: Munition,
		p_position: Vec2,
		p_rotation: float | None = None,
		p_direction: Vec2 | None = None,
		p_ignoreColliders: set[Collider] | None = None
	):
		theta = math.atan2(p_direction.y, p_direction.x)
		Actor.__init__(
			self,
			p_position = p_position,
			p_rotation = p_rotation,
			p_direction = p_direction,
			p_speed = p_munition._speed,
			p_health = p_munition._penetrationLimit,
			p_damage = p_munition._damage
		)
		self._transform.size = Vec2(p_munition._radius, p_munition._radius)

		self._collider = CircleCollider(
			p_radius = p_munition._radius,
			p_ignoreColliders = p_ignoreColliders
		)

		self._renderer = CircleRenderable(p_munition._radius)

		self._traversalBehaviour = p_munition.traversalBehaviour
		

	def update(self) -> None: #travel along the initial direction
		self.offsetPosition(self._traversalBehaviour(self._transform)) #use the bound munitions instance to update the bullet
		
		#then the entity itself handles if its in a valid spot etc
		if self._transform.position.x <= 0 or self._transform.position.x >= WINDOW.width:
			self.malive = False
		if self._transform.position.y <= 0 or self._transform.position.y >= WINDOW.height:
			self.malive = False

	def onCollisionEnter(self, p_other: Entity) -> None:
		if isinstance(p_other, Actor):
			p_other.applyDamage(self._damage)
			self.applyDamage(1) #removes one from the amount of times it can collide again
