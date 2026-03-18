
from core.time import TIME
from core.vector import Vec2
from render.renderable import CircleRenderable
from entities.entity import Actor

class Particle(Actor):
	def __init__(
		self,
		p_position: float,
		p_direction: Vec2,
		p_speed: float,
		p_lifeTime: float,
		p_radius: float
	):
		Actor.__init__(
			self,
			p_position = p_position,
			p_direction = p_direction,
			p_speed = p_speed,
			p_health = p_lifeTime,
			p_damage = 0.0
		)
		self._renderer = CircleRenderable(p_radius)

	def updatePosition(self):
		self.offsetPosition(self._direction * TIME.deltaTime)

	def update(self):
		super().update()
		self.applyDamage(TIME.deltaTime)
