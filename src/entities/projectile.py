import math
from core.time import TIME
from core.window import WINDOW
from core.vector import Vec2

from physics.collision import Collider, CircleCollider
from render.renderable import CircleRenderable

from entities.entity import Entity, Actor
from gameplay.munition import Munition, Bullet, Missile, Pellet

#wrapper around munition children types into a fluid entity type
class Projectile(Actor):
	def __init__(
		self,
		p_munition: Munition,
		p_position: Vec2,
		p_rotation: float | None = None,
		p_direction: Vec2 | None = None,
		p_ignoreColliders: set[Collider] | None = None,
	):
		Actor.__init__(
			self,
			p_position = p_position.copy,
			p_rotation = p_rotation,
			p_direction = p_direction,
			p_speed = p_munition.speed,
			p_health = p_munition.penetrationLimit,
			p_damage = p_munition.damage
		)
		self._transform.size = Vec2(p_munition.radius, p_munition.radius)

		self._collider = CircleCollider(
			p_radius = p_munition.radius,
			p_ignoreColliders = p_ignoreColliders
		)

		self._renderer = CircleRenderable(p_munition.radius)
		
	def update(self) -> None: #travel along the initial direction
		super().update()

		#then the entity itself handles if its in a valid spot etc
		if self._transform.position.x <= 0 or self._transform.position.x >= WINDOW.width:
			self.malive = False
		if self._transform.position.y <= 0 or self._transform.position.y >= WINDOW.height:
			self.malive = False

	def onCollisionEnter(self, p_other: Entity) -> None:
		if isinstance(p_other, Actor):
			p_other.applyDamage(self._damage)
			self.applyDamage(1) #removes one from the amount of times it can collide again

class BulletProjectile(Projectile):
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float | None = None,
		p_direction: Vec2 | None = None,
		p_ignoreColliders: set[Collider] | None = None,
		p_munition: Munition = Bullet()
	):
		Projectile.__init__(
			self,
			p_munition = p_munition,
			p_position = p_position,
			p_rotation = p_rotation,
			p_direction = p_direction,
			p_ignoreColliders = p_ignoreColliders
		)

	def updatePosition(self): #straight line bullet behaviour by default
		self.offsetPosition(self._direction * self._speed * TIME.deltaTime)


class MisslieProjectile(Projectile):
	def __init__(
		self,
		p_target: Entity,
		p_position: Vec2,
		p_rotation: float | None = None,
		p_direction: Vec2 | None = None,
		p_ignoreColliders: set[Collider] | None = None,
		p_munition: Munition = Missile()
	):
		Projectile.__init__(
			self,
			p_munition = p_munition,
			p_position = p_position,
			p_rotation = p_rotation,
			p_direction = p_direction,
			p_ignoreColliders = p_ignoreColliders
		)
		self._target: Entity = p_target

	def update(self) -> None:
		if self._target is not None and not self._target.alive:
			self._target = None #free the reference should prevent memory leaks and turn missile to dumb fire
		
		self.lookAt(self._target) #set rotation and direction toward the target
		
		self.offsetPosition(self._direction * self._speed * TIME.deltaTime) #move toward the target
		super().update()

class PelletProjectile(BulletProjectile):
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float | None = None,
		p_direction: Vec2 | None = None,
		p_ignoreColliders: set[Collider] | None = None,
		p_munition: Munition = Pellet()
	):
		BulletProjectile.__init__(
			self,
			p_position = p_position,
			p_rotation = p_rotation,
			p_direction = p_direction,
			p_ignoreColliders = p_ignoreColliders,
			p_munition = p_munition
		)