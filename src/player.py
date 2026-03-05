import pygame

from src.vector import Vec2
from src.entity import CircleEntity, RectangleEntity

class Player(RectangleEntity):	
	def move(self, p_keys, p_delta_time, p_window_dimensions: Vec2):
		move = Vec2()
		#get keyboard input directions
		if p_keys[pygame.K_w]:
			move.y -= 1.0
		if p_keys[pygame.K_a]:
			move.x -= 1.0
		if p_keys[pygame.K_s]:
			move.y += 1.0
		if p_keys[pygame.K_d]:
			move.x += 1.0
		move *= self.m_speed * p_delta_time
		move_prime = self.m_position + move
		if move_prime == self.m_position: #idk if float error will make this always false | but no movement shouldnt bother updating position and there on geometry
			return
		
		#screen boundary check using center only cuz shape isnt decided to add ether half dimensions or radius
		if move_prime.x < 0:
			move_prime.x = 0
		if move_prime.x > p_window_dimensions.x:
			move_prime.x = p_window_dimensions.x

		if move_prime.y < 0:
			move_prime.y = 0
		if move_prime.y > p_window_dimensions.y:
			move_prime.y = p_window_dimensions.y
		
		self.setPosition(move_prime) #go via this interface so it updates geometry 