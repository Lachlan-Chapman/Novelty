import pygame
class Time:
	def __init__(
		self,
		p_targetFPS: float
	):
		self.m_targetFP: float = p_targetFPS
		self.m_clock = pygame.time.Clock()
		self.m_deltaTime: float = 0.0
		self.m_totalTime: float = 0.0
	
	def update(self) -> None:
		self.m_deltaTime = self.m_clock.tick(self.m_targetFPS) / 1000 #gets the true delta time but caps at the target fps | MAKE SURE TO /1000 as delta time should be in seconds
		self.m_totalTime += self.m_deltaTime

TIME: Time = Time(120.0)