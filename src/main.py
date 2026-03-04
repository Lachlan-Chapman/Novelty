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

	enemy = CircleEnemy(
		Vec2(
			window_dimensions.x // 3,
			window_dimensions.y // 3
		),
		18,
		360
	)

	rect = RectangleEntity(
		Vec2(
			window_dimensions.x // 4,
			window_dimensions.y // 4
		),
		Vec2(20, 30)
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
		
		keys = pygame.key.get_pressed()
		player.move(
			keys,
			delta_time,
			window_dimensions
		)

		player.collideWith(enemy)
		player.collideWith(rect)

		screen.fill((20, 20, 26))
		player.draw(screen)
		enemy.draw(screen)
		rect.draw(screen)

		pygame.display.flip()
	
	pygame.quit()
	sys.exit(0)

if __name__ == "__main__":
	main()

#TODO
#enemy class - DONE
#collision - DONE
#bullet object
#shooting
#player rotation with shooting
#enemy and bullet collision
#enemy death
#remove dead enemies
#enemy spawing