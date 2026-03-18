import sys
import math

import pygame
pygame.init() #immediatly initialize before ANY OTHER object creation

from core.window import WINDOW
from core.time import TIME
from systems.entity_registry import ENTITY_REGISTRY

from core.vector import Vec2

from entities.enemy import Enemy
from entities.player import PLAYER

from gameplay.munition import Bullet, Missile
from gameplay.weapon import Weapon, MissileLauncher

from systems.enemy_spawner import EnemySpawner

from ui.gui import GUI

def main():

	enemy_spawner = EnemySpawner(
		p_target = PLAYER,
		p_spawnSpeed = 5,
		p_spawnRadius = WINDOW.width * 0.5
	)

	test_enemy = Enemy(
		p_position = Vec2(
			PLAYER.position.x + 350,
			PLAYER.position.y
		),
		p_radius = 20,
		p_speed = 0.0,
		p_health = 100.0,
		p_damage = 0
	)
	#ENTITY_REGISTRY.add(test_enemy)

	font = pygame.font.SysFont(None, 36)

	running = True
	while running:
		TIME.update() #set delta time and total time

		#event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False

		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			running = False

		PLAYER.handleInput(keys)

		#Move for AI
		enemy_spawner.spawnEnemy()
		ENTITY_REGISTRY.update()

		#Run Collision
		ENTITY_REGISTRY.handleCollision()

		#Clean Up
		ENTITY_REGISTRY.removeDead()

		#Render
		WINDOW.screen.fill((20, 20, 20)) #clear screen

		PLAYER._armory.debugDraw()
		ENTITY_REGISTRY.draw()

		GUI.draw() #top layer above all else
		pygame.display.flip() #show render
	#Safely Exit
	pygame.quit()
	sys.exit(0)
	
	

if __name__ == "__main__":
	main()

#fix PLAYER class to be able to shoot, move, have bullets ignore self
#fix enemy to shoot, target enemy
#clean entity registry
#clean enemy spawner
#fix enemy death