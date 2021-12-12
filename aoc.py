import collections
import ctypes
import gc
import operator
import random

def __extend(cls, name, implementation):
	backing = gc.get_referents(cls.__dict__)
	assert(len(backing) == 1)
	backing = backing[0]
	backing[name] = implementation
	ctypes.pythonapi.PyType_Modified(ctypes.py_object(cls))

def __object_sj_print(self):
	print(self)

def __list_str(self):
	result = ""
	for e in self:
		result += e
	return result

def __list_tuple(self):
	tuple(self)

def __list_set(self):
	set(self)

@property
def __list_len(self):
	return len(self)

def __list_indices(self):
	return range(self.len)

@property
def __list_first(self):
	return None if not self.len else self[0]

@property
def __list_last(self):
	return None if not self.len else self[-1]

def __list_random(self):
	return None if not self.len else random.choice(self)

def __list_max(self):
	return max(self)

def __list_min(self):
	return min(self)

def __list_max_by(self, comparator):
	return None if not self.len else self[self.max_index_by(comparator)]

def __list_min_by(self, comparator):
	return None if not self.len else self[self.min_index_by(comparator)]

def __list_max_index(self):
	return None if not self.len else self.max_index_by(operator.lt)

def __list_min_index(self):
	return None if not self.len else self.min_index_by(operator.lt)

def __list_max_index_by(self, comparator):
	if not len(self):
		return None
	max_index = 0
	for i in self.indices():
		if comparator(self[max_index], self[i]):
			max_index = i
	return max_index

def __list_min_index_by(self, comparator):
	if not len(self):
		return None
	min_index = 0
	for i in self.indices():
		if comparator(self[i], self[min_index]):
			min_index = i
	return min_index

def __list_first_index_of(self, x):
	return self.first_index_by(lambda a: x == a)

def __list_first_by(self, predicate):
	index = self.first_index_by(predicate)
	return self[index] if index != None else None

def __list_first_index_by(self, predicate):
	for i in self.indices():
		if predicate(self[i]):
			return i
	return None

def __list_last_index_of(self, x):
	return self.last_index_by(lambda a: x == a)

def __list_last_by(self, predicate):
	index = self.last_index_by(predicate)
	return self[index] if index != None else None

def __list_last_index_by(self, predicate):
	for i in self.indices()[:-1]:
		if predicate(self[i]):
			return i
	return None

def __list_map(self, transform):
	results = []
	for e in self:
		results.append(transform(e))
	return results

def __list_filter(self, predicate):
	results = []
	for e in self:
		if predicate(e):
			results.append(e)
	return results

def __list_fold(self, combinator):
	iterator = iter(self)
	try:
		initial = next(iterator)
	except StopIteration:
		return None
	return list(iterator).reduce(initial, combinator)

def __list_reduce(self, initial, generator):
	for e in self:
		initial = generator(initial, e)
	return initial

def __list_enumerated(self):
	return list(zip(self.indices(), self))

def __list_flatten(self):
	result = []
	for e in self:
		if isinstance(e, collections.Iterable):
			result += e
		else:
			result.append(e)
	return result

def __list_compact(self):
	return self.filter(lambda x: x != None)

def __list_intersperse(self, spacer):
	return zip(self, [spacer] * self.len).flatten()[:-1]

def __list_window(self, size):
	window = collections.deque()
	results = []
	for e in self:
		window.append(e)
		if len(window) >= size:
			results.append(list(window))
			window.popleft()
	return results

def __list_chunk(self, size):
	results = []
	current = []
	for i, e in self.enumerated():
		current.append(e)
		if i % size == size - 1:
			results.append(current)
			current = []
	if current.len:
		results.append(current)
	return results

def __list_chunk_by(self, predicate):
	results = []
	current = []
	for e in self:
		if not current.last or (current.last and predicate(current.last, e)):
			current.append(e)
		else:
			results.append(current)
			current = [e]
	if current.len:
		results.append(current)
	return results

def __list_str_join(self, joiner=""):
	return joiner.join(self.map(str))

def __list_has_prefix(self, other):
	if self.len < other.len:
		return False

	for a, b in zip(self, other):
		if a != b:
			return False

	return True

def __list_has_suffix(self, other):
	if self.len < other.len:
		return False

	for a, b in zip(self[::-1], other[::-1]):
		if a != b:
			return False

	return True

def __list_partition(self, predicate):
	included = []
	excluded = []
	for e in self:
		if predicate(e):
			included.append(e)
		else:
			excluded.append(e)
	return (included, excluded)

def __list_exclude_each(self):
	elements = list(self)
	results = []
	for i in elements.indices():
		results.append(elements[:i] + elements[i + 1:])
	return results

def __list_swap(self, i, j):
	(self[i], self[j]) = (self[j], self[i])

def __list_sorted(self):
	copy = list(self[:])
	copy.sort()
	return copy

def __list_rotate(self, index):
	return self[index:] + self[:index]

def __list2d_transpose(self):
	return zip(*self).map(list)

def __list2d_diagonals(self):
	if not self.len:
		return ([], [])
	for r in self:
		if r.len != self.len:
			return None
	diagonal11 = self.indices().map(lambda i: self[i][i])
	diagonal12 = self.indices().map(lambda i: self[i][-(i + 1)])
	return (diagonal11, diagonal12)

__extend(object, 'sj_print', __object_sj_print)

__extend(list, 'str', __list_str)
__extend(list, 'tuple', __list_tuple)
__extend(list, 'set', __list_tuple)
__extend(list, 'transpose', __list2d_transpose)
__extend(list, 'diagonals', __list2d_diagonals)

for type in [list, str, tuple, set, dict, zip, range]:
	__extend(type, 'len', __list_len)
	__extend(type, 'map', __list_map)
	__extend(type, 'filter', __list_filter)
	__extend(type, 'fold', __list_fold)
	__extend(type, 'reduce', __list_reduce)
	__extend(type, 'window', __list_window)
	__extend(type, 'chunk', __list_chunk)
	__extend(type, 'chunk_by', __list_chunk_by)
	__extend(type, 'str_join', __list_str_join)
	__extend(type, 'has_prefix', __list_has_prefix)
	__extend(type, 'has_suffix', __list_has_suffix)
	__extend(type, 'intersperse', __list_intersperse)
	__extend(type, 'partition', __list_partition)
	__extend(type, 'flatten', __list_flatten)
	__extend(type, 'compact', __list_compact)
	__extend(type, 'exclude_each', __list_exclude_each)

for type in [list, str, tuple]:
	__extend(type, 'indices', __list_indices)
	__extend(type, 'first', __list_first)
	__extend(type, 'last', __list_last)
	__extend(type, 'random', __list_random)
	__extend(type, 'max', __list_max)
	__extend(type, 'min', __list_min)
	__extend(type, 'max_index', __list_max_index)
	__extend(type, 'min_index', __list_min_index)
	__extend(type, 'max_by', __list_max_by)
	__extend(type, 'min_by', __list_min_by)
	__extend(type, 'max_index_by', __list_max_index_by)
	__extend(type, 'min_index_by', __list_min_index_by)
	__extend(type, 'first_index_of', __list_first_index_of)
	__extend(type, 'first_by', __list_first_by)
	__extend(type, 'first_index_by', __list_first_index_by)
	__extend(type, 'last_index_of', __list_last_index_of)
	__extend(type, 'last_by', __list_last_by)
	__extend(type, 'last_index_by', __list_last_index_by)
	__extend(type, 'enumerated', __list_enumerated)
	__extend(type, 'swap', __list_swap)
	__extend(type, 'sorted', __list_sorted)
	__extend(type, 'rotate', __list_rotate)

__extend(set, 'min', __list_len)
__extend(set, 'max', __list_len)
__extend(set, 'flatten', __list_flatten)

def __sj_irange(min, max, stride):
	result = []
	i = min
	while True:
		result.append(i)
		i += stride
		if i > max:
			return result

def sj_irange(min, max, stride=1):
	return __sj_irange(min, max, stride) if min <= max else __sj_irange(-min, -max, stride).map(operator.neg)

def sj_range(min, max, stride=1):
	return list(range(min, max, stride)) if min <= max else range(-min, -max, stride).map(operator.neg)
