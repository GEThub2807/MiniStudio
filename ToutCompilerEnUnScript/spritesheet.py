import pygame

class SpriteSheet():
	def __init__(self, image):
		self.sheet = image
		self.elapsed_time = 0

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image

	def update(self, dt):
		animation_delay = 0.2
		frame_count = 18
		self.elapsed_time += dt

		self.index = self.elapsed_time / animation_delay
		self.index %= frame_count 

	def draw(self, screen):
		screen.blit(self.sheet, (0, 0), (32 * self.index, 24, 32, 24))