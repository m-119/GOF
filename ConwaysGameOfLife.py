import numpy as np

class ConwaysGameOfLife(object):
	def __init__(self, arr: np):
		"""
		Класс манипуляций с матрицей
		:param arr: матрица со значениями 0, 1
		"""
		print("--инициализация--:")
		self.now: np = arr													# матрица текущего значения
		self.new: np = None													# матрица будущего значения
		self.size_x: int = len(self.now)									# ширина
		print(f"ширина :{self.size_x}")
		self.size_y: int = len(self.now[0])									# высота
		print(f"высота :{self.size_x}")
		self.recoord = self.recoord_set(*self.now.shape)					# рекоординирование (формат Тор)
		print(f"ConwaysGameOfLife() -> __init__: recoord_set({self.now.shape})")
		self.step = 0														# ход
		self.show = self.show("░▓")											# определение параметров отрисовки в консоль
		self.hist = [np.array([0]) for i in range(20)]						# создание очереди истории

	def recoord_set(self, size_y: int, size_x: int):
		"""
		установка выравнивания координат, для зацикливания анимации
		:param size_x: ширина поля
		:param size_y: высота поля
		:return: coord(x,y)
		"""

		def recoord_(y: int, x: int):
			"""
			пересчёт координат
			:param x: позиция x
			:param y: позиция y
			:return: x, y по текущему полю
			"""
			x_, y_ = x, y
			if x < 0:
				x_ = size_x - 1
			elif x >= size_x:
				x_ = 0
			if y < 0:
				y_ = size_y - 1
			elif y >= size_y:
				y_ = 0
			return y_, x_

		return recoord_

	def fate_num(self, x_: int, y_: int, arr: np) -> int:
		"""
		получает значение соседних ячеек
		:param x_:
		:param y_:
		:param arr:
		:return:
		"""
		l = [-1, 0, 1]
		# все подсчитываемые индексы:
		# print([(y_ + y, x_ + x) for x in l for y in l if (x, y) != (0, 0)])
		# print([(y_ + y, x_ + x) for x in l for y in l if x != 0 or y != 0])
		# print([recoord(y_ + y, x_ + x) for x in l for y in l if (x, y) != (0, 0)])
		# все возможные варианты индексов вокруг ячейки, нормализую по полю (если выхожу за пределы беру зеркальный элемент)
		# суммирую все значения по полученным индексам
		# print([(x_ + x, y_ + y) for x in l for y in l if (x, y) != (0, 0)])
		# print([recoord(x_ + x, y_ + y) for x in l for y in l if (x, y) != (0, 0)])
		compr_sum = np.sum([arr[self.recoord(x_ + x, y_ + y)] for x in l for y in l if (x, y) != (0, 0)])
		return compr_sum

	def fate(self, x_: int, y_: int, arr: np) -> int:
		"""
		определяет судьбу ячейки по соседям и возвращает записываемое значение
		:param x_:
		:param y_:
		:param arr:
		:return: значение, которое следует записать в анализируемую ячейку
		"""
		f = self.fate_num(x_, y_, arr)
		# в пустой (мёртвой) клетке, рядом с которой ровно три живые клетки, зарождается жизнь;
		if f == 3:
			return 1
		# если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить;
		elif f == 2 and arr[x_, y_] == 1:
			return 1
		# в противном случае, если соседей меньше двух или больше трёх, клетка умирает
		# («от одиночества» или «от перенаселённости») ©Википедия
		else:
			return 0

	def fate_all(self, arr: np) -> np:
		"""
		определяет судьбу всех ячеек
		:param nump:
		:return:
		"""
		sz = arr.shape
		# для корректного представления, нужна новая матрица, в которую будет собираться результат
		result = np.zeros(arr.shape, dtype=int)
		# строки
		for i in range(sz[0]):
			# столбцы
			for j in range(sz[1]):
				result[i][j] = self.fate(i, j, arr)
		return result

	# вывод в консоль
	def show(self, param="□Х"):
		"""
		параметры для отрисовки в консоли
		:param param:
		:return:
		"""
		def show_param(x):
			d = dict(enumerate(param))
			return d.get(x, str(x))
		return show_param

	def sp_print(self, matrix: np) -> None:
		"""
		отрисовка в консоли
		:param matrix:
		:return:
		"""
		for row in matrix:
			for x in row:
				print("{:1s}".format(self.show(x)), end="")
			print()

	def get_arr(self) -> np:
		"""
		Получение массива
		:return:
		"""
		return self.now

	def set_arr(self, arr: np) -> None:
		"""
		Установка массива
		:param arr:
		:return:
		"""
		# изменение размеров тора
		self.recoord = self.recoord_set(*self.arr.shape)
		# задание внутреннего массива
		self.now = arr

	def reset(self):
		# обнеуление ходов
		self.step = 0
		# обнуление истории
		self.hist = [np.array([0]) for i in range(20)]  # создание очереди истории

	def next_step(self) -> tuple:
		self.step += 1
		self.new = self.fate_all(self.now)

		# вывод в консоль, если консольный запуск
		if __name__ == '__main__':
			print(f"Ход: {self.step}")
			self.sp_print(self.new)

		if np.array_equal(self.new, self.now):
			print ("-===Колония не изменяется===-")
			return self.now, 'stable'
		elif any(np.array_equal(self.new, arr) for arr in self.hist):
			print("-===Цикл===-")
			return self.now, 'cycle'
		elif not np.sum(self.new.flatten()):
			print("-===Гибель колонии===-")
			return self.now, 'death'

		# сохраняем старое значение для отслеживания циклов
		self.hist.append(self.now)
		# купирование разрастания истории (очередь заданного размера)
		self.hist.pop(0)
		self.now = self.new
		return self.now, 0





# print(new1)
# print(new1[y_-1:y_+2, x_-1:x_+2])

# print(np.sum(new1[y_-1:y_+2, x_-1:x_+2]) - new1[y_, x_])
# print(new1[1:4, 1:4])





if __name__ == '__main__':
	# сэмпл для проверки
	sample = np.array(
			[
				[1, 0, 0, 0, 1, 1, 0, 0, 0, 0]
				, [0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
				, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
				, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
				, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
				, [0, 0, 0, 0, 1, 0, 0, 1, 0, 0]
				, [0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
				, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				, [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
				, [0, 0, 0, 0, 0, 0, 1, 0, 1, 0]
				, [0, 1, 1, 0, 0, 0, 0, 1, 1, 0]
				, [0, 1, 1, 0, 0, 0, 0, 0, 0, 1]
				, [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]]
	)
	# цикл
	sample1 = np.array(
			[
				[0, 0, 0, 0, 0]
				, [0, 0, 1, 0, 0]
				, [0, 0, 1, 0, 0]
				, [0, 0, 1, 0, 0]
				, [0, 0, 0, 0, 0]])
	# пройгрыш
	sample2 = np.array(
			[
				[0, 0, 0, 0, 0]
				, [0, 0, 0, 1, 0]
				, [0, 0, 1, 1, 0]
				, [0, 1, 1, 0, 0]
				, [0, 0, 0, 0, 0]])
	# Планер (glider)
	sample3 = np.array(
			[
				[0, 0, 1, 0, 0]
				, [0, 0, 0, 1, 0]
				, [0, 1, 1, 1, 0]
				, [0, 0, 0, 0, 0]
				, [0, 0, 0, 0, 0]])
	gol = ConwaysGameOfLife(sample3)
	gol_play = 0
	while not gol_play:
		gol_play = gol.next_step()[1]
