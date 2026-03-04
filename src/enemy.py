import pygame

from src.entity import CircleEntity
from src.player import Player

class CircleEnemy(CircleEntity):
	def target(self, p_other: Player):
		self.m_target = p_other
		