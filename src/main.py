import sys
import math

import pygame
pygame.init() #immediatly initialize before ANY OTHER object creation
from core.window import WINDOW

from systems.entity_registry import ENTITY_REGISTRY #the instance of the registry not the class
from core.time import TIME

from core.vector import Vec2
from entities.entity import RectangleEntity, CircleEntity

from gameplay.weapon import Weapon, Pistol
from entities.bullet import Bullet

from entities.player import Player
from entities.enemy import CircleEnemy
from systems.enemy_spawner import EnemySpawner


def main():
	player = Player(
		p_position = Vec2(
			WINDOW.m_width // 2,
			WINDOW.m_height // 2
		),
		p_dimensions = Vec2(25, 25),
		p_speed = 0.0,
		p_rotationSpeed = math.pi * 1.5,
		p_health = 500.0,
		p_damage = 100.0,
		p_maxWeaponCount = 3
	)

	player.m_renderer.setColor((255, 255, 255))
	player.addWeapon(Weapon(
		p_name = "Turret",
		p_projectile = Bullet,
		p_shootSpeed = 0.2,
		p_magazineSize = 1,
		p_reloadSpeed = 0
	))
	ENTITY_REGISTRY.add(player)

	enemy_spawner = EnemySpawner(
		p_target = player,
		p_spawnSpeed = 1.8,
		p_spawnRadius = 250
	)


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
		enemy_spawner.spawnEnemy()
		ENTITY_REGISTRY.update()
		player.shoot(keys)

		#Update Entity Positions
		player.move(keys)

		#Check Collisions
		ENTITY_REGISTRY.handleCollision()

		#Clean Up
		ENTITY_REGISTRY.removeDead()
		
		#Render
		WINDOW.m_screen.fill((20, 20, 26)) #clears screen with given color
		ENTITY_REGISTRY.draw()
		pygame.display.flip() #swap graphics buffer to display the render of this loop
	
	#Safely Exit
	pygame.quit()
	sys.exit(0)

if __name__ == "__main__":
	main()

