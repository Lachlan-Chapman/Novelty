import sys
import math

import pygame
pygame.init() #immediatly initialize before ANY OTHER object creation

from core.window import WINDOW
from core.time import TIME
from core.vector import Vec2

from entities.player import Player

from gameplay.munition import Bullet
from gameplay.weapon import Weapon

from systems.entity_registry import ENTITY_REGISTRY
from systems.enemy_spawner import EnemySpawner

def main():
	player = Player(
		p_rotationSpeed = math.pi,
		p_health = 500.0,
		p_damage = 100.0,
		p_size = Vec2(WINDOW.width / 25, WINDOW.width / 25)
	)

	if player._renderer is not None:
		player._renderer.setColor((255, 0, 0))

	player._armory.addWeapon(
		p_weapon = Weapon(
			p_munition = Bullet,
			p_magazineSize = 5,
			p_shotCooldown = 1,
			p_reloadSpeed = 2
		)
	)
	player._armory.addAmmo(Bullet, 100)
	ENTITY_REGISTRY.add(player)

	enemy_spawner = EnemySpawner(
		p_target = player,
		p_spawnSpeed = 5,
		p_spawnRadius = WINDOW.width * 0.5
	)

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

		player.handleInput(keys)

		#Move for AI
		enemy_spawner.spawnEnemy()
		ENTITY_REGISTRY.update()

		#Run Collision
		ENTITY_REGISTRY.handleCollision()

		#Clean Up
		ENTITY_REGISTRY.removeDead()

		#Render
		WINDOW.screen.fill((20, 20, 20))
		ENTITY_REGISTRY.draw()
		pygame.display.flip()
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