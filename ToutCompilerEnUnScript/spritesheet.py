import pygame
import os

class Sprite:
	def __init__(self, asset_folder_path):
		self.animations: list[SpriteSheet] = []
		self.animation_index = 0
		
		files = os.listdir(asset_folder_path)
		for file in files:
			frames = []
			images = os.listdir(asset_folder_path + "/" + file)
			for image in images:
				frames.append(pygame.image.load(asset_folder_path + "/" + file + "/" + image).convert_alpha())

			self.animations.append(SpriteSheet(frames))

	def set_animation(self, animation_index):
		self.animation_index = animation_index
	
	def update(self, dt):
		self.animations[self.animation_index].update(dt)
	
	def draw(self, screen, x, y):
		self.animations[self.animation_index].draw(screen, x, y)

	def get_size(self):
		return self.animations[0].frames[0].get_size()


class SpriteSheet:
	def __init__(self, frames):
		self.frames = frames
		self.elapsed_time = 0
		self.frame_count = len(frames)
		self.animation_delay = 0.1

	def get_image(self, frame, width, height, scale, colour):
		image = pygame.Surface((width, height)).convert_alpha()
		image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
		image = pygame.transform.scale(image, (width * scale, height * scale))
		image.set_colorkey(colour)

		return image

	def update(self, dt):
		self.elapsed_time += dt

		self.index = int(self.elapsed_time / self.animation_delay)
		self.index %= self.frame_count

	def draw(self, screen, x, y):
		screen.blit(self.frames[self.index], (x, y))