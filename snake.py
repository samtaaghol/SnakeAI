import pygame
import random
import sys
import time


class Game:
	def __init__(self):

		self.sw = 1000
		self.sh = 1000
		self.screen = pygame.display.set_mode((self.sw, self.sh))
		pygame.init()
		self.snake = Snake()
		self.direction = (0, 0)
		self.clock = pygame.time.Clock()
		self.foods = [Food()]

	def update_screen(self):
		pygame.display.update()

	def run(self):

		while True:

			pygame.display.get_surface().fill((0, 0, 0))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						self.snake.direction = (-1, 0)
					elif event.key == pygame.K_RIGHT:
						self.snake.direction = (1, 0)
					elif event.key == pygame.K_UP:
						self.snake.direction = (0, -1)
					elif event.key == pygame.K_DOWN:
						self.snake.direction = (0, 1)

			self.snake.move()
			if self.snake.in_self() or self.snake.out_of_bounds():
				self.quit()

			self.snake.on_food(self.foods)

			for food in self.foods:
				food.draw()

			self.update_screen()
			self.clock.tick(10)

	@staticmethod
	def quit():
		pygame.display.quit()
		pygame.quit()
		sys.exit()


class Object:

	def draw(self):
		x_cols = 8
		y_cols = 8
		sw = 1000
		sh = 1000
		column_spacing = sw / x_cols
		row_spacing = sh / y_cols
		pygame.draw.rect(pygame.display.get_surface(), self.color,
								  (self.x * column_spacing, self.y * row_spacing, column_spacing, row_spacing), 0)


class Snake:

	def __init__(self):

		self.snake = [BodyPart((random.randint(0, 7), random.randint(0, 7)))]
		self.direction = (0, 0)

	def move(self):
		x = self.snake[-1].x + self.direction[0]
		y = self.snake[-1].y + self.direction[1]
		self.snake.append(BodyPart((x, y)))
		self.snake = self.snake[1:]

		for piece in self.snake:
			piece.draw()

	def on_food(self, foods):

		head = self.snake[-1]

		for i in range(len(foods)):
			if (foods[i].x == head.x) and (foods[i].y == head.y):
				foods.remove(foods[i])
				self.add_to_tail()
				foods.append(Food())
				break



	def add_to_tail(self):

		if len(self.snake) != 1:
			self.tail_direction = (self.snake[1].x - self.snake[0].x, self.snake[1].y - self.snake[0].y)

			x = self.snake[0].x - self.tail_direction[0]
			y = self.snake[0].y - self.tail_direction[1]
		else:
			x = self.snake[0].x - self.direction[0]
			y = self.snake[0].y - self.direction[1]

		body_part = BodyPart((x, y))
		self.snake.insert(0, body_part)

	def in_self(self):
		for piece in self.snake[:-1]:
			if (piece.x == self.snake[-1].x) and (piece.y == self.snake[-1].y):
				return True
		return False

	def out_of_bounds(self):
		if self.snake[-1].x > 7:
			return True
		elif self.snake[-1].x < 0:
			return True
		elif self.snake[-1].y < 0:
			return True
		elif self.snake[-1].y > 7:
			return True
		return False


class BodyPart(Object):

	def __init__(self, position):
		self.x = position[0]
		self.y = position[1]
		self.color = (255, 255, 255)


class Food(Object):

	def __init__(self):

		self.x = random.randint(0,7)
		self.y = random.randint(0,7)

		self.color = (255, 0, 0)


game = Game()
game.run()
