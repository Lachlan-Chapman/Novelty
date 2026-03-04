import pygame

from src.vector import Vec2
from src.entity import CircleEntity, RectangleEntity

class Player(RectangleEntity):	
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
		self.m_position += move

		if self.m_position.x < 0:
			self.m_position.x = 0
		if self.m_position.x > p_window_dimensions.x:
			self.m_position.x = p_window_dimensions.x

		if self.m_position.y < 0:
			self.m_position.y = 0
		if self.m_position.y > p_window_dimensions.y:
			self.m_position.y = p_window_dimensions.y
