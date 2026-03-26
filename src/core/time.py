import pygame
class Time:
	def __init__(
		self,
		p_targetFPS: float
	):
		self._targetFPS: float = p_targetFPS
		self._clock = pygame.time.Clock()
		self._timeScale: float = 1.0 #this adjusts speed of time so we could pause and things
		self._deltaTime: float = 0.0
		self._totalTime: float = 0.0
	
	def update(self) -> None:
		self._deltaTime = self._clock.tick(self._targetFPS) / 1000 #gets the true delta time but caps at the target fps | MAKE SURE TO /1000 as delta time should be in seconds
		self._totalTime += self._deltaTime * self.timeScale

	def setTimeScale(self, p_scale: float):
		self._timeScale = p_scale

	def reset(self) -> None:
		self._timeScale = 1.0
		self._totalTime = 0.0

	@property
	def deltaTime(self):
		return self._deltaTime * self._timeScale

	@property
	def time(self):
		return self._totalTime
	
	@property
	def timeScale(self):
		return self._timeScale

TIME: Time = Time(120.0)