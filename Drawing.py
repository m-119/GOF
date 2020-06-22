from time import sleep
from tkinter import *
import numpy as np
from ConwaysGameOfLife import ConwaysGameOfLife

class Drawing(object):
	def __init__(
				self,
				dot_width: int = 10,
				dot_height: int = 10,
				dot_cnv_width: int = 40,
				dot_cnv_height: int = 20,
				arr: np = None):
		"""
		:param dot_width: ширина точки
		:param dot_height: высота точки
		:param dot_cnv_width: ширина канвы в точках
		:param dot_cnv_height: высота канвы в точках
		"""
		self.dot_width: int = dot_width
		self.dot_height: int = dot_height
		self.dot_cnv_width: int = dot_cnv_width
		self.dot_cnv_height: int = dot_cnv_height
		self.arr = arr
		# играть
		self.play = False
		# Статус
		self.status = "-"
		# инициализация меню
		self.menu = Menu(tearoff=0)
		self.menu.add_command(command=self.game_start, label="▶")		# первоначальная установка в меню
		root.bind("<Button-3>", self.menu_popup)						# действие ПКМ
		root.title(self.status)
		# начальные значения, в зависимости от массива:
		if arr is None:
			self.arr = np.zeros((self.dot_cnv_height, self.dot_cnv_width), int)
		elif arr is not None:
			self.dot_cnv_width = len(arr[0])
			self.dot_cnv_height = len(arr)

		# подключение игры
		self.gol = ConwaysGameOfLife(np.zeros((self.dot_cnv_height, self.dot_cnv_width), int))
		# получение ссылки на массив игры
		self.arr = self.gol.get_arr()

		# перевод в пиксели
		self.c_width = self.dot_cnv_width * self.dot_width  # ширина канвы в пикселях
		self.c_height = self.dot_cnv_height * self.dot_height  # высота канвы в пикселях

		self.cnv = Canvas(root, width=self.c_width, height=self.c_height, bg="white")
		self.cnv.bind("<Button-1>", self.click)
		self.cnv.pack()
		self.draw_dots()

	def calc_xy(self, x=0, y=0):
		"""
		Вычисление позиции элемента с учётом размеров
		:param x:
		:param y:
		:return:
		"""
		# print(x, y)
		print(x//self.dot_width, y//self.dot_height)
		return x // self.dot_width, y // self.dot_height

	def set_color(self, s: int):
		"""
		Определяет цвет рисуемого квадрата
		:return:
		"""
		# print(f"set_color({s})")
		return "#090" if s == 1 else "#1ff"

	def draw_dot(self, x=0, y=0):
		# цвет квадрата
		color = self.set_color(self.arr[y][x])
		# позиция точек квадрата
		x0 = x * self.dot_width + 2
		x1 = x0 + self.dot_width
		y0 = y * self.dot_height + 2
		y1 = y0 + self.dot_height
		# print(x0, y0, x1, y1)
		self.cnv.create_rectangle(x0, y0, x1, y1,
								  outline="", fill=color)

	def draw_dots(self):
		# очистка поля
		# где-то было упоминание, про утечку памяти при рисовании поверх
		# При одиночных кликах это не очень критично, но при массовой перерисовке,
		# могут возникнуть сложности
		self.cnv.delete("All")
		for y in range(len(self.arr)):
			# print(f"y: {y}")
			for x in range(len(self.arr[y])):
				# print(f"x: {x}")
				# print(f"draw_dots -> draw_dot({x}, {y})")
				self.draw_dot(x, y)

	def arr_edit(self, x: int=0, y: int=0) -> None:
		"""
		Обработка изменений массива игры
		:param x:
		:param y:
		:return:
		"""
		self.arr[y][x] = not self.arr[y][x]
		self.gol.reset()
		#print(self.arr)

	# print(arr)

	def click(self, event):
		"""
		Обработка клика по канве
		:param event:
		:return:
		"""

		# выравнивание максимальных позиций
		if event.x >= self.c_width:
			x = self.c_width-1
			print(x)
		else:
			x = event.x

		if event.y >= self.c_height:
			y = self.c_height-1
			print(y)
		else:
			y = event.y
		# ----------------------------------

		# x,y в точках
		x_, y_ = self.calc_xy(x, y)

		# модификация нампи
		self.arr_edit(x_, y_)

		# рисуем квадрат
		self.draw_dot(x_, y_)

		self.status = "-"
		root.title(self.status)

		if self.play:
			self.animation_start()

	def game_start(self):
		#print(f"old_play: {self.play}")
		self.play = not self.play
		#print(f"new_play: {self.play}")
		self.animation_start()


	def menu_popup(self, event):
		# всплывающее меню
		# это взял отсюда:
		# https://younglinux.info/tkinter/menu.php
		# изменить лэйбл
		self.menu.add_command(command=self.game_start, label="⏸" if self.play else "▶")
		self.menu.delete(0)
		self.menu.post(event.x_root, event.y_root)

	def animation_start(self):
		while self.play and self.status == "-":
			self.arr = self.gol.next_step()[0]
			self.status = "-" if not self.gol.next_step()[1] else self.gol.next_step()[1]
			sleep(0.1)
			self.draw_dots()
			root.update()
		root.title(self.status)


if __name__ == '__main__':

	# тестовые данные
	ar = np.array([
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
		[0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 1, 0, 0, 0, 1, 0, 0]])
	root = Tk()

	obj = Drawing()
	root.mainloop()
