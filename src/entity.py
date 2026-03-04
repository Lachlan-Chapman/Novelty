import pygame
from src.vector import Vec2
class CircleRenderable:
	def __init__(self, p_radius: float):
		self.m_radius = p_radius
		self.m_color = (255, 0, 0)

	def setColor(self, p_color):
		self.m_color= p_color

	def draw(self, p_screen, p_position: Vec2):
		pygame.draw.circle(
			p_screen,
			self.m_color,
			(int(p_position.x), int(p_position.y)),
			self.m_radius
		)

from src.collision import CircleCollider
class Player:
	def __init__(self, p_position: Vec2, p_radius: float, p_speed: float, p_health: float = 100.0):
		self.m_renderable = CircleRenderable(p_radius)
		self.m_collider = CircleCollider(p_position, p_radius)
		
		self.m_speed = p_speed
		self.m_health = p_health
		self.m_alive = True

	def draw(self, p_screen):
		self.m_renderable.draw(p_screen, self.m_collider.m_position)

	def move(self, p_keys, p_delta_time, p_window_dimensions: Vec2):
		move = Vec2()

		if p_keys[pygame.K_w]:
			move.y -= 1.0
		if p_keys[pygame.K_a]:
			move.x -= 1.0
		if p_keys[pygame.K_s]:
			move.y += 1.0
		if p_keys[pygame.K_d]:
			move.x += 1.0
		move *= self.m_speed * p_delta_time
		self.m_collider.m_position += move

		if self.m_collider.m_position.x < 0:
			self.m_collider.m_position.x = 0
		if self.m_collider.m_position.x > p_window_dimensions.x:
			self.m_collider.m_position.x = p_window_dimensions.x

		if self.m_collider.m_position.y < 0:
			self.m_collider.m_position.y = 0
		if self.m_collider.m_position.y > p_window_dimensions.y:
			self.m_collider.m_position.y = p_window_dimensions.y
