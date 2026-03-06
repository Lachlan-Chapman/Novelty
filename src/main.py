import sys
import pygame

from src.vector import Vec2
from src.entity import RectangleEntity, CircleEntity
from src.player import Player
from src.enemy import CircleEnemy


def main():
	pygame.init()

	fps = 120

	window_dimensions = Vec2(960, 540)
	screen = pygame.display.set_mode((window_dimensions.x, window_dimensions.y))
	pygame.display.set_caption("Pygame Heartbeat")

	clock = pygame.time.Clock()

	player = Player(
		Vec2(
			window_dimensions.x // 2,
			window_dimensions.y // 2
		),
		Vec2(18, 18),
		360
	)

	player.m_renderable.setColor((255, 255, 255))

	rect = RectangleEntity(
		Vec2(
			window_dimensions.x // 4,
			window_dimensions.y // 4
		),
		Vec2(20, 30)
	)

	circ = CircleEntity(
		Vec2(
			window_dimensions.x // 3,
			window_dimensions.y // 3
		),
		15
	)

	running = True
	while running:
		delta_time = clock.tick(fps) / 1000.0

		#event handling
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False
		
		#move entities
		keys = pygame.key.get_pressed()
		player.move(
			keys,
			delta_time,
			window_dimensions
		)

		theta_prime = rect.m_theta + delta_time * 0
		rect.setRotation(theta_prime)
		
		#collision
		player.collideWith(rect)
		player.collideWith(circ)
		
		#render
		screen.fill((20, 20, 26))
		rect.draw(screen)
		circ.draw(screen)
		player.draw(screen)

		pygame.display.flip()
	
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
#OOB circle to rectangle collison allowing for rotated rects
	#convert circle into axis alligned rect space with rect at (0, 0). so we are rotating the world and shifting to make the rect the center
	#get closest point in/on rect to the circle (the closest point can be in the rect not just on the edge)
	#get distance from closest point to circle
	#check if the distance to the circle from the closest point is < radius which would mean collision
#bullet object
#shooting
#player rotation with shooting
#enemy and bullet collision
#enemy death
#remove dead enemies
#enemy spawing