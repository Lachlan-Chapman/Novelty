import sys
import math

import pygame
pygame.init() #immediatly initialize before ANY OTHER object creation

from core.window import WINDOW
from core.time import TIME
from core.controls import Actions, INPUT_STATE
from core.console import CONSOLE

from systems.entity_registry import ENTITY_REGISTRY

from entities.player import PLAYER

from systems.enemy_spawner import EnemySpawner

from ui.gui import GUI



def reset_game() -> EnemySpawner:
	CONSOLE.info("Game Reset")
	ENTITY_REGISTRY.clear() #remove all entities
	TIME.reset() #time back to 0
	PLAYER.reset() #restore health and ammo


	ENTITY_REGISTRY.add(PLAYER)
	return EnemySpawner(
		p_target = PLAYER,
		p_spawnTime = 3,
		p_spawnRadius = WINDOW.height * 0.65
	)

def main():
	enemy_spawner: EnemySpawner = reset_game()
	running = True
	game_over = False
	while running:
		TIME.update() #set delta time and total time

		#event handling
		INPUT_STATE.update()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		if INPUT_STATE.isPressed(Actions.EXIT):
			running = False
		if INPUT_STATE.isPressed(Actions.RESET):
			enemy_spawner = reset_game()
			

		keys = pygame.key.get_pressed()
		if keys[pygame.K_ESCAPE]:
			running = False

		PLAYER.handleInput()

		#Move for AI
		enemy_spawner.spawnEnemy()
		ENTITY_REGISTRY.update()

		#Run Collision
		ENTITY_REGISTRY.handleCollision()

		#Clean Up
		ENTITY_REGISTRY.removeDead()

		if not PLAYER.alive:
			game_over = True
			TIME._timeScale = 0.0 #stop all time
		else:
			game_over = False

		#Render
		WINDOW.screen.fill((20, 20, 20)) #clear screen

		PLAYER._armory.debugDraw()
		ENTITY_REGISTRY.draw()

		GUI.draw() #top layer above all else
		if game_over is True:
			GUI.drawGameOver()

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