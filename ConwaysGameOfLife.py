import os
import numpy as np
import time

def recoord_set(size_y, size_x):
	"""
	установка выравнивания координат
	:param size_x: ширина поля
	:param size_y: высота поля
	:return: coord(x,y)
	"""

	def recoord_(y, x):
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


def fate_num(x_, y_, arr):
	"""
	получает значение соседних ячеек
	:param x_:
	:param y_:
	:return: сумма соседей
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
	compr_sum = np.sum([arr[recoord(x_ + x, y_ + y)] for x in l for y in l if (x, y) != (0, 0)])
	return compr_sum


def fate(x_, y_, arr):
	"""
	определяет судьбу по соседним ячейкам и возвращает записываемое значение
	:param x_:
	:param y_:
	:return: значение, которое следует записать в анализируемую ячейку
	"""
	f = fate_num(x_, y_, arr)
	# в пустой (мёртвой) клетке, рядом с которой ровно три живые клетки, зарождается жизнь;
	if f == 3:
		return 1
	# если у живой клетки есть две или три живые соседки, то эта клетка продолжает жить;
	elif f == 2 and arr[x_, y_] == 1:
		return 1
	# в противном случае, если соседей меньше двух или больше трёх, клетка умирает («от одиночества» или «от перенаселённости»)
	else:
		return 0


def fate_all(arr):
	"""
	:param nump:
	:return:
	"""
	sz = arr.shape
	result = np.zeros(arr.shape, dtype=int)
	# строки
	for i in range(sz[0]):
		# столбцы
		for j in range(sz[1]):
			result[i][j] = fate(i, j, arr)
	return result


# print(new1)
# print(new1[y_-1:y_+2, x_-1:x_+2])

# print(np.sum(new1[y_-1:y_+2, x_-1:x_+2]) - new1[y_, x_])
# print(new1[1:4, 1:4])


#вывод
def show(param="□Х"):
	def show_param(x):
		d = dict(enumerate(param))
		return d.get(x, str(x))
	return show_param
show = show("░▓")


def sp_print ( matrix ):
	for row in matrix:
		for x in row:
			print ( "{:1s}".format(show(x)), end = "")
		print()


if __name__ == '__main__':
	hist = [np.array([0]) for i in range(20)]
	# сэмпл для проверки
	sample = np.array(
			[ [1, 0, 0, 0, 1, 1, 0, 0, 0, 0]
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
			[[0, 0, 0, 0, 0]
			, [0, 0, 1, 0, 0]
			, [0, 0, 1, 0, 0]
			, [0, 0, 1, 0, 0]
			, [0, 0, 0, 0, 0]])
	# пройгрыш
	sample2 = np.array(
			[[0, 0, 0, 0, 0]
			, [0, 0, 0, 1, 0]
			, [0, 0, 1, 1, 0]
			, [0, 1, 1, 0, 0]
			, [0, 0, 0, 0, 0]])
	# Планер (glider)
	sample3 = np.array(
			[[0, 0, 1, 0, 0]
			, [0, 0, 0, 1, 0]
			, [0, 1, 1, 1, 0]
			, [0, 0, 0, 0, 0]
			, [0, 0, 0, 0, 0]])

	now = sample3
	recoord = recoord_set(*now.shape)
	sp_print(now)
	step = 0
	while True:
		step += 1
		print(f"Ход: {step}")
		new = fate_all(now)
		sp_print(new)
		if np.array_equal(new, now):
			print ("-===Колония не изменяется===-")
			break
		elif any(np.array_equal(new,arr) for arr in hist):
			print("-===Цикл===-")
			break
		elif not np.sum(new.flatten()):
			print("-===Гибель колонии===-")
			break

		# сохраняем старое значение для отслеживания циклов
		hist.append(now)
		hist.pop(0)
		now = new

		time.sleep(0.1)
		os.system('cls')