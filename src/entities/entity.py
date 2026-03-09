import math

from core.window import WINDOW
from core.console import CONSOLE
from core.vector import Vec2
from core.transform import Transform

from physics.collision import Collider, CircleCollider, RectangleCollider
from render.renderable import Renderable, CircleRenderable, RectangleRenderable

class Entity:
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float
	):
		self._transform: Transform = Transform(
			p_position = p_position,
			p_rotation = p_rotation
		) 
		
		self._id: int | None = None #used for collision pairing, ENTITY_REGISTRY sets this so only enetiies registerd will be apart of the actaul game

		self._collider: Collider | None = None
		self._renderable: Renderable | None = None
		self._dirtyGeometry = True

	def _set_id(self, p_id: int) -> None:
		if self._id is not None:
			CONSOLE.warn("Entity ID already set")
			return
		self._id = p_id

	#ROTATION SETTERS
	def setRotation(self, p_theta: float) -> None: #rotation in radians NEED TO CONVERT TO DEG if for some reason something requires it (pygame renderer)
		self._transform.rotation = p_theta
		self._transform.rotation = self._transform.rotation % math.tau
		self._dirtyGeometry = True

	def offsetRotation(self, p_delta: float) -> None: #doesnt set but adds the delta rotation
		self.setRotation(self._transform.rotation + p_delta)

	#POSITION SETTERS
	def setPosition(self, p_position: Vec2) -> None: #sets exact position in screen coordinates
		self._transform.position = p_position
		self._dirtyGeometry = True

	def offsetPosition(self, p_delta: Vec2) -> None: #doesnt set but adds the direction
		self.setPosition(self._transform.position + p_delta)

	#INTERNAL UPDATES
	def updateRotation(self) -> None: #for internally handled changes for AI or some function
		pass

	def updatePosition(self) -> None: #for if the entity has its own internal position handling IE AI or a projectile
		pass

	def update(self) -> None:
		self.updatePosition()
		self.updateRotation()

	#COLLISIONS
	def updateGeometry(self) -> None:
		if not self._dirtyGeometry:
			return
		if self._collider is not None:
			self._collider.updateTransform(self._transform)
		self._dirtyGeometry = False

	def overlaps(self, p_other: "Entity") -> bool:
		if self._collider is None:
			CONSOLE.error("Entity collider not set")
			return False
		if p_other._collider is None:
			CONSOLE.error("Other entity collider not set")
			return False
		return self._collider.overlaps(p_other._collider)
	
	def onCollisionEnter(self, p_other: "Entity") -> None: #allows for custom handling on how to act with differnet entity collision combos IE bullet with ship and ship with bullet etc
		pass

	#RENDERING
	def draw(self) -> None:
		if self._renderable is not None:
			self._renderable.draw(self._transform.position, self._transform.rotation)

	#GETTERS
	@property
	def position(self) -> Vec2:
		return self._transform.position
	
	@property
	def rotation(self) -> float:
		return self._transform.rotation
	
	@property
	def id(self) -> int | None:
		return self._id

	#DEBUGGING
	def drawCollision(self) -> None:
		if self._collider is not None and self._renderable is not None:
			if self._collider.collisionCount > 0:
				self._renderable.setColor((0, 255, 0))
			else:
				self._renderable.setColor((255, 0, 0))

class KinematicEntity(Entity):
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float,
		p_velocity: Vec2 | None = None,
		p_angularVelocity: float | None = None
	):
		Entity.__init__(
			self,
			p_position = p_position,
			p_rotation = p_rotation
		)
		self._velocity: Vec2 = p_velocity if p_velocity is not None else Vec2(0.0, 0.0)
		self._angularVelocity: float = p_angularVelocity if p_angularVelocity is not None else 0.0

class Actor(KinematicEntity):
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float,
		p_velocity: Vec2 | None,
		p_angularVelocity: float | None,
		p_health: float,
		p_damage: float
	):
		KinematicEntity.__init__(
			self,
			p_position = p_position,
			p_rotation = p_rotation,
			p_velocity = p_velocity,
			p_angularVelocity = p_angularVelocity
		)
		self._health: float = p_health
		self._damage: float = p_damage
	
	@property
	def health(self) -> float:
		return self._health

	@property
	def damage(self) -> float:
		return self._damage
	

class CircleEntity(Actor): 
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float,
		p_velocity: Vec2 | None,
		p_angularVelocity: float | None,
		p_health: float,
		p_damage: float,
		p_radius: float,
	):
		Actor.__init__(
			self,
			p_position = p_position,
			p_rotation = p_rotation,
			p_velocity = p_velocity,
			p_angularVelocity = p_angularVelocity,
			p_health = p_health,
			p_damage = p_damage
		)
		self._transform.size = Vec2(p_radius, p_radius)
		self._collider: Collider = CircleCollider(p_radius)
		self._renderable: Renderable = CircleRenderable(p_radius)

class RectangleEntity(Actor):
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float,
		p_velocity: Vec2 | None,
		p_angularVelocity: float | None,
		p_health: float,
		p_damage: float,
		p_size: Vec2,
	):
		Actor.__init__(
			self,
			p_position = p_position,
			p_rotation = p_rotation,
			p_velocity = p_velocity,
			p_angularVelocity = p_angularVelocity,
			p_health = p_health,
			p_damage = p_damage
		)
		self._transform.size = p_size
		self._collider: Collider = RectangleCollider(p_size)
		self._renderable: Renderable = RectangleRenderable(p_size)
	
		self._vertices = []

	def updateGeometry(self) -> None:
		if not self._dirtyGeometry:
			return
		if self._collider is not None:
			self._collider.updateTransform(self._transform)
		self._dirtyGeometry = False

	def getEdgeNormals(self) -> tuple[Vec2, Vec2]:
		return self._axisI, self._axisJ


		