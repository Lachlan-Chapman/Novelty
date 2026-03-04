import sys
import pygame

def main():
	pygame.init()

	window_width = 960
	window_height = 540
	fps = 120

	screen = pygame.display.set_mode((window_width, window_height))
	pygame.display.set_caption("Pygame Heartbeat")

	clock = pygame.time.Clock()

	player_pos_x = window_width // 2
	player_pos_y = window_height // 2
	player_speed = 320

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
		move_x = 0.0
		move_y = 0.0

		if keys[pygame.K_w]:
			move_y -= 1.0
		if keys[pygame.K_a]:
			move_x -= 1.0
		if keys[pygame.K_s]:
			move_y += 1.0
		if keys[pygame.K_d]:
			move_x += 1.0
		
		player_pos_x += int(move_x * player_speed * delta_time)
		player_pos_y += int(move_y * player_speed * delta_time)

		if player_pos_x < 0:
			player_pos_x = 0
		if player_pos_x > window_width:
			player_pos_x = window_width

		if player_pos_y < 0:
			player_pos_y = 0
		if player_pos_y > window_height:
			player_pos_y = window_height

		screen.fill((20, 20, 26))
		player_radius = 18

		pygame.draw.circle(screen, (230, 230, 240), (player_pos_x, player_pos_y), player_radius)
		pygame.display.flip()
	
	pygame.quit()
	sys.exit(0)

if __name__ == "__main__":
	main()