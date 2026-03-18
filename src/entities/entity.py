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
		p_rotation: float | None = None,
		p_direction: Vec2 | None = None
	):
		if p_direction is not None and p_rotation is not None:
			direction = p_direction
			rotation = p_rotation
		elif p_direction is None and p_rotation is not None:
			direction = Vec2(math.cos(p_rotation), math.sin(p_rotation))
			rotation = p_rotation
		elif p_rotation is None and p_direction is not None:
			direction = p_direction
			rotation = math.atan2(p_direction.y, p_direction.x)
		else:
			direction = Vec2(1.0, 0.0)
			rotation = 0.0
			
		self._transform: Transform = Transform(
			p_position = p_position,
			p_rotation = p_rotation
		) 

		self._direction = direction
		self._transform.rotation = rotation
		
		self._id: int | None = None #used for collision pairing, ENTITY_REGISTRY sets this so only enetiies registerd will be apart of the actaul game
		self._alive = True

		self._collider: Collider = Collider()
		self._collider.canCollide(False)
		self._renderer: Renderable | None = None
		self._dirtyGeometry = True

	def setId(self, p_id: int) -> None:
		if self._id is not None:
			CONSOLE.warn("Entity ID already set")
			return
		self._id = p_id

	#ROTATION SETTERS
	def setDirection(self, p_direction: Vec2) -> None:
		self._direction = p_direction
		self.setRotation(math.atan2(p_direction.y, p_direction.x))
		self._dirtyGeometry = True

	def offsetDirection(self, p_delta: Vec2) -> None:
		self.setDirection(self._direction + p_delta)

	def lookAt(self, p_target: "Entity | None") -> None:
		if p_target is None:
			return
		
		self.setDirection(
			(p_target.position - self.position).unit
		)

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

	def onCollisionExit(self, p_other: "Entity") -> None:
		pass
	
	#RENDERING
	def draw(self) -> None:
		if self._renderer is not None:
			self._renderer.draw(self._transform.position, self._transform.rotation)

	#GETTERS
	@property
	def position(self) -> Vec2:
		return self._transform.position
	
	@property
	def rotation(self) -> float:
		return self._transform.rotation
	
	@property
	def direction(self) -> Vec2:
		return self._direction
	
	@property
	def id(self) -> int | None:
		return self._id
	
	@property
	def alive(self) -> bool:
		return self._alive
	
	@property
	def collider(self) -> Collider:
		return self._collider

	#DEBUGGING
	def drawCollision(self) -> None:
		if self._collider is not None and self._renderer is not None:
			if self._collider.collisionCount > 0:
				self._renderer.setColor((0, 255, 0))
			else:
				self._renderer.setColor((255, 0, 0))

class KinematicEntity(Entity):
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float | None = None,
		p_direction: Vec2 | None = None, #this way we can take either rotation or velocity
		p_speed: float = 0.0
	):
		Entity.__init__(
			self,
			p_position = p_position,
			p_rotation = p_rotation,
			p_direction = p_direction
		)
		self._speed = p_speed

class Actor(KinematicEntity):
	def __init__(
		self,
		p_position: Vec2,
		p_rotation: float | None = None,
		p_direction: Vec2 | None = None,
		*,
		p_speed: float,
		p_health: float,
		p_damage: float
	):
		KinematicEntity.__init__(
			self,
			p_position = p_position,
			p_rotation = p_rotation,
			p_direction = p_direction,
			p_speed = p_speed
		)
		self._maxHealth: float = p_health
		self._health: float = p_health
		self._damage: float = p_damage
	
	def applyDamage(self, p_damage: float) -> None:
		self._health -= p_damage
		if self._health <= 0:
			self._alive = False

	@property
	def maxHealth(self) -> float:
		return self._maxHealth

	@property
	def health(self) -> float:
		return self._health

	@property
	def damage(self) -> float:
		return self._damage
	
