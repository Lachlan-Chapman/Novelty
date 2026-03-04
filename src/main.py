import sys
import pygame

from src.vector import Vec2
from src.entity import Player


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
		18,
		360
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

		screen.fill((20, 20, 26))
		player.draw(screen)

		pygame.display.flip()
	
	pygame.quit()
	sys.exit(0)

if __name__ == "__main__":
	main()