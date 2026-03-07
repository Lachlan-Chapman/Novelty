#similar to how unity has Time.deltaTime we should have a global single time accessee
#also stop passing in delta time as a parameter to functions its messy

import pygame
class Time:
	def __init__(self, p_targetFPS: float):
		self.m_targetFPS = p_targetFPS
		self.m_clock = pygame.time.Clock()
		self.m_deltaTime = 0.0
		self.m_totalTime = 0.0
	
	def update(self):
		self.m_deltaTime = self.m_clock.tick(self.m_targetFPS) / 1000 #gets the true delta time but caps at the target fps | MAKE SURE TO /1000 as delta time should be in seconds
		self.m_totalTime += self.m_deltaTime

TIME = Time(120.0)