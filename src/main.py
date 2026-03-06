import sys
import math

import pygame
pygame.init() #immediatly initialize before ANY OTHER object creation
from src.window import WINDOW

from src.entityRegistry import ENTITY_REGISTRY #the instance of the registry not the class
from src.time import TIME

from src.vector import Vec2
from src.entity import RectangleEntity, CircleEntity

from src.weapon import Pistol
from src.bullet import Bullet

from src.player import Player
from src.enemy import CircleEnemy


def main():
	player = Player(
		p_position = Vec2(
			WINDOW.m_width // 2,
			WINDOW.m_height // 2
		),
		p_dimensions = Vec2(18, 18),
		p_speed = 0.0,
		p_rotationSpeed = math.pi,
		p_health = 500.0,
		p_maxWeaponCount = 3
	)

	player.m_renderable.setColor((255, 255, 255))
	player.addWeapon(Pistol(Bullet))
	ENTITY_REGISTRY.add(player)

	rect = RectangleEntity(
		p_position = Vec2(
			WINDOW.m_width // 2,
			WINDOW.m_height // 1.75
		),
		p_dimensions = Vec2(20, 30)
	)
	ENTITY_REGISTRY.add(rect)

	circ = CircleEntity(
		p_position = Vec2(
			WINDOW.m_width // 3,
			WINDOW.m_height // 3
		),
		p_radius = 15
	)
	ENTITY_REGISTRY.add(circ)

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

#TODO
#enemy class - DONE
#SAT (seperated axis theorem) collision - DONE
	#get shape vertices
	#get shape edge normals
	#filter duplicate normals (maybe)
	#filter opposing normals (maybe)
	#for each axis, 
		#for each shape
			#project all vertices of a shape to it
			#find the min and max then we have shape as an interval for that axis
		#compare min and max of shapes together, if there is no overlap return False (no collision)
		#if there is a collision on this axis, continue
	#return True
#OOB circle to rectangle collison allowing for rotated rects - DONE
	#convert circle into axis alligned rect space with rect at (0, 0). so we are rotating the world and shifting to make the rect the center
	#get closest point in/on rect to the circle (the closest point can be in the rect not just on the edge)
	#get distance from closest point to circle
	#check if the distance to the circle from the closest point is < radius which would mean collision
#gobal list of all entities - DONE
	#sweep to draw, update pos etc
	#naive (o^2) check for collison
	#sweep any 0 health enemies delete || outside the window
#gobal time - DONE
#global window - DONE
#engine level damage gating - DONE
#bullet object - DONE
#shooting - DONE
#player rotation with shooting
#enemy and bullet collision
#enemy death
#remove dead enemies
#enemy spawing