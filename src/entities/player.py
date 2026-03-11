import pygame
from pygame.key import ScancodeWrapper
import math

from core.vector import Vec2


from entities.entity import Entity, Actor

from core.time import TIME
from core.window import WINDOW

from physics.collision import RectangleCollider
from render.renderable import RectangleRenderable

from gameplay.munition import Bullet, Missile, Pellet
from gameplay.weapon import Weapon, MissileLauncher, Shotgun


from systems.armory import Armory
from systems.entity_registry import ENTITY_REGISTRY


class Player(Actor):
	def __init__(
		self,
		p_rotationSpeed: float,
		p_health: float,
		p_damage: float,
		p_size: Vec2
	):
		Actor.__init__(
			self,
			p_position = Vec2(
				WINDOW.width // 2,
				WINDOW.height // 2
			),
			p_rotation = 0.0, #centered at the screen never translates
			p_speed = p_rotationSpeed,
			p_health = p_health,
			p_damage = p_damage
		)
		self._transform.size = p_size
		self._collider = RectangleCollider(p_size)

		self._renderer = RectangleRenderable(p_size)
		
		direction = Vec2(
			math.cos(self._transform.rotation),
			math.sin(self._transform.rotation)
		)
		self._armory: Armory = Armory(
			p_maxWeaponCount = 3,
			p_barrelPosition = self._transform.position + (direction * self._transform.size.magnitude),
			p_barrelDirection = direction
		)

	def onCollisionEnter(self, p_other: Entity):
		if isinstance(p_other, Actor):
			p_other.applyDamage(p_other.damage)

	def handleRotationInput(self, p_keys: ScancodeWrapper) -> None:
		theta = 0.0
		
		if p_keys[pygame.K_a]:
			theta -= self._speed
		if p_keys[pygame.K_d]:
			theta += self._speed
		self.offsetRotation(theta * TIME.deltaTime) #adjust to be rotating speed per second
		
		direction = Vec2(
			math.cos(self._transform.rotation),
			math.sin(self._transform.rotation)
		)
		self._armory.updateBarrel(
			p_position = self._transform.position + (direction * self._transform.size.magnitude),
			p_direction = direction
		)

	def handleArmoryInput(self, p_keys: ScancodeWrapper) -> None:
		if p_keys[pygame.K_SPACE]:
			self._armory.shoot(p_ignoreColliders = set([self._collider]))
			

	def handleInput(self, p_keys: ScancodeWrapper) -> None:
		#rotation
		self.handleRotationInput(p_keys)
		#shooting
		self.handleArmoryInput(p_keys)

	def draw(self):
		super().draw()
		self._armory._barrel.draw() #player has to handle the visual representation of the barrel

PLAYER = Player(
	p_rotationSpeed = math.pi,
	p_health = 500.0,
	p_damage = 100.0,
	p_size = Vec2(WINDOW.width / 25, WINDOW.width / 25)
)

if PLAYER._renderer is not None:
	PLAYER._renderer.setColor((255, 0, 0))

# player._armory.addWeapon(
# 	p_weapon = Weapon(
# 		p_magazineSize = 5,
# 		p_shotCooldown = 1,
# 		p_reloadSpeed = 2
# 	)
# )
# player._armory.addAmmo(Bullet, 100)

# PLAYER._armory.addWeapon(
# 	p_weapon = MissileLauncher(
# 		p_magazineSize = 5,
# 		p_shotCooldown = 1,
# 		p_reloadSpeed = 2,
# 		p_targetFOV = math.pi/2
# 	)
# )
# PLAYER._armory.addAmmo(Missile, 100)

PLAYER._armory.addWeapon(
	p_weapon = Shotgun(
		p_magazineSize = 5,
		p_shotCooldown = 1,
		p_reloadSpeed = 2,
		p_spreadAngle = math.pi * 2/3,
		p_pelletCount = 7
	)
)
PLAYER._armory.addAmmo(Pellet, 100)
ENTITY_REGISTRY.add(PLAYER)



	