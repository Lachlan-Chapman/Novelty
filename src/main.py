import sys
import math

import pygame
pygame.init() #immediatly initialize before ANY OTHER object creation

from core.window import WINDOW
from core.time import TIME
from core.vector import Vec2

from entities.player import Player

from gameplay.weapon import Weapon
from gameplay.munition import Bullet


from systems.entity_registry import ENTITY_REGISTRY #the instance of the registry not the class
from systems.enemy_spawner import EnemySpawner


def main():
	# player = Player(
	# 	p_health = 500.0,
	# 	p_damage = 100,
	# 	p_size = Vec2(20, 20)
	# )

	# player._renderer.setColor((255, 255, 255))
	# player._armory.addWeapon(Weapon(
	# 	p_munition = Bullet,
	# 	p_magazineSize = 5,
	# 	p_reloadSpeed = 2,
	# 	p_shotCooldown = 1
	# ))
	# ENTITY_REGISTRY.add(player)


	

	running = True
	while running:
		TIME.update()

		#event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False
		
		#Gather Inputs
		keys = pygame.key.get_pressed()
		
		#Entity Actions
		#enemy_spawner.spawnEnemy()
		#ENTITY_REGISTRY.update()

		#User Input
		#player.handleInput(keys)

		#Check Collisions
		#ENTITY_REGISTRY.handleCollision()

		#Clean Up
		#ENTITY_REGISTRY.removeDead()
		
		#Render
		WINDOW._screen.fill((20, 20, 26)) #clears screen with given color
		ENTITY_REGISTRY.draw()
		pygame.display.flip() #swap graphics buffer to display the render of this loop
	
	#Safely Exit
	pygame.quit()
	sys.exit(0)

if __name__ == "__main__":
	main()

#fix player class to be able to shoot, move, have bullets ignore self
#fix enemy to shoot, target enemy
#clean entity registry
#clean enemy spawner
#fix enemy death