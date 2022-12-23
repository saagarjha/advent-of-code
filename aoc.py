import collections.abc
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
	for i in self.indices()[::-1]:
		if predicate(self[i]):
			return i
	return None

def __list_reversed(self):
	return list(self)[::-1]

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
		if isinstance(e, collections.abc.Iterable):
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

def __list_sorted(self, predicate=None):
	class comparator:
		def __init__(self, object):
			self.object = object

		def __lt__(self, other):
			return predicate(self.object, other.object)

		def __gt__(self, other):
			return predicate(other.object, self.object)

		def __eq__(self, other):
			return not predicate(self.object, other.object) and not predicate(other.object, self.object)

		def __le__(self, other):
			return not predicate(other.object, self.object)

		def __ge__(self, other):
			return not predicate(self.object, other.object)

		def __ne__(self, other):
			return predicate(self.object, other.object) or predicate(other.object, self.object)

	key = None if predicate is None else comparator
	copy = list(self[:])
	copy.sort(key=key)
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

def __list_sum(self):
	return self.fold(operator.add)

__extend(object, "sj_print", __object_sj_print)

__extend(list, "str", __list_str)
__extend(list, "tuple", __list_tuple)
__extend(list, "set", __list_tuple)
__extend(list, "transpose", __list2d_transpose)
__extend(list, "diagonals", __list2d_diagonals)

for type in [list, str, tuple, set, dict, zip, range]:
	__extend(type, "len", __list_len)
	__extend(type, "map", __list_map)
	__extend(type, "filter", __list_filter)
	__extend(type, "fold", __list_fold)
	__extend(type, "reduce", __list_reduce)
	__extend(type, "window", __list_window)
	__extend(type, "chunk", __list_chunk)
	__extend(type, "chunk_by", __list_chunk_by)
	__extend(type, "str_join", __list_str_join)
	__extend(type, "has_prefix", __list_has_prefix)
	__extend(type, "has_suffix", __list_has_suffix)
	__extend(type, "intersperse", __list_intersperse)
	__extend(type, "partition", __list_partition)
	__extend(type, "flatten", __list_flatten)
	__extend(type, "compact", __list_compact)
	__extend(type, "exclude_each", __list_exclude_each)
	__extend(type, "sum", __list_sum)

for type in [list, str, tuple, set, zip, range]:
	__extend(type, "max", __list_max)
	__extend(type, "min", __list_min)
	__extend(type, "reversed", __list_reversed)
	__extend(type, "flatten", __list_flatten)

for type in [list, str, tuple, range]:
	__extend(type, "indices", __list_indices)
	__extend(type, "first", __list_first)
	__extend(type, "last", __list_last)
	__extend(type, "random", __list_random)
	__extend(type, "max_index", __list_max_index)
	__extend(type, "min_index", __list_min_index)
	__extend(type, "max_by", __list_max_by)
	__extend(type, "min_by", __list_min_by)
	__extend(type, "max_index_by", __list_max_index_by)
	__extend(type, "min_index_by", __list_min_index_by)
	__extend(type, "first_index_of", __list_first_index_of)
	__extend(type, "first_by", __list_first_by)
	__extend(type, "first_index_by", __list_first_index_by)
	__extend(type, "last_index_of", __list_last_index_of)
	__extend(type, "last_by", __list_last_by)
	__extend(type, "last_index_by", __list_last_index_by)
	__extend(type, "enumerated", __list_enumerated)
	__extend(type, "sorted", __list_sorted)

for type in [list, str, tuple]:
	__extend(type, "swap", __list_swap)
	__extend(type, "rotate", __list_rotate)

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

class Matrix:
	def __init__(self, matrix):
		self.matrix = matrix
		self.rows = matrix.len
		self.columns = matrix[0].len if self.rows else 0

	def inside(self, r, c):
		return r >= 0 and r < self.rows and c >= 0 and c < self.columns


	def __getitem__(self, index):
		return self.matrix[index[0]][index[1]] if self.inside(index[0], index[1]) else None

	def __setitem__(self, index, value):
		if self.inside(index[0], index[1]):
			self.matrix[index[0]][index[1]] = value

	def neighbors8(self, r, c):
		neighbors = []
		for row in sj_irange(r - 1, r + 1):
			for column in sj_irange(c - 1, c + 1):
				if self.inside(row, column) and (row != r or column != c):
					neighbors.append((row, column))
		return neighbors

	def neighbors4(self, r, c):
		neighbors = []
		if self.inside(r - 1, c):
			neighbors.append((r - 1, c))
		if self.inside(r, c - 1):
			neighbors.append((r, c - 1))
		if self.inside(r, c + 1):
			neighbors.append((r, c + 1))
		if self.inside(r + 1, c):
			neighbors.append((r + 1, c))
		return neighbors

	def neighbors4_diag(self, r, c):
		neighbors = []
		if self.inside(r - 1, c - 1):
			neighbors.append((r - 1, c - 1))
		if self.inside(r + 1, c - 1):
			neighbors.append((r + 1, c - 1))
		if self.inside(r - 1, c + 1):
			neighbors.append((r - 1, c + 1))
		if self.inside(r + 1, c + 1):
			neighbors.append((r + 1, c + 1))
		return neighbors

class UnevaluatedProxy:
	def __init__(self, expression):
		self.__expression = expression

	def __unevaluate_arguments(f):
		def trampoline(*args):
			new_args = []
			for arg in args:
				if not hasattr(arg, "__"):
					new_args.append(UnevaluatedProxy(lambda *args: arg))
				else:
					new_args.append(arg)
			return f(*new_args)
		return trampoline

	def __eval(self, *args):
		return self.__expression(*args)

	def __(self, *_args):
		return UnevaluatedProxy(lambda *args: self.__expression(*args)(*_args))

	def __call__(self, *args):
		return self.__expression(*args)

	@property
	def _unflatten(self):
		return UnevaluatedProxy(lambda *args: UnevaluatedProxy(lambda *args: self.__eval(*args[0])))()

	@property
	def _int(self):
		return UnevaluatedProxy(lambda *args: int(self.__eval(*args)))

	@property
	def _str(self):
		return UnevaluatedProxy(lambda *args: str(self.__eval(*args)))

	@__unevaluate_arguments
	def __eq__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) == other.__eval(*args))

	@__unevaluate_arguments
	def __ne__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) != other.__eval(*args))

	@__unevaluate_arguments
	def __lt__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) < other.__eval(*args))

	@__unevaluate_arguments
	def __gt__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) > other.__eval(*args))

	@__unevaluate_arguments
	def __le__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) <= other.__eval(*args))

	@__unevaluate_arguments
	def __ge__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) >= other.__eval(*args))

	@__unevaluate_arguments
	def __pos__(self):
		return UnevaluatedProxy(lambda *args: +self.__eval(*args))

	@__unevaluate_arguments
	def __neg__(self):
		return UnevaluatedProxy(lambda *args: -self.__eval(*args))

	@__unevaluate_arguments
	def __abs__(self):
		return UnevaluatedProxy(lambda *args: abs(self.__eval(*args)))

	@__unevaluate_arguments
	def __invert__(self):
		return UnevaluatedProxy(lambda *args: ~self.__eval(*args))

	@__unevaluate_arguments
	def __round__(self, n):
		return UnevaluatedProxy(lambda *args: round(self.__eval(*args), n.__eval(*args)))

	@__unevaluate_arguments
	def __floor__(self):
		return UnevaluatedProxy(lambda *args: math.floor(self.__eval(*args)))

	@__unevaluate_arguments
	def __ceil__(self):
		return UnevaluatedProxy(lambda *args: math.ceil(self.__eval(*args)))

	@__unevaluate_arguments
	def __trunc__(self):
		return UnevaluatedProxy(lambda *args: math.trunc(self.__eval(*args)))

	@__unevaluate_arguments
	def __add__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) + other.__eval(*args))

	@__unevaluate_arguments
	def __sub__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) - other.__eval(*args))

	@__unevaluate_arguments
	def __mul__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) * other.__eval(*args))

	@__unevaluate_arguments
	def __floordiv__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) // other.__eval(*args))

	@__unevaluate_arguments
	def __div__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) / other.__eval(*args))

	@__unevaluate_arguments
	def __mod__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) % other.__eval(*args))

	@__unevaluate_arguments
	def __divmod__(self, other):
		return UnevaluatedProxy(lambda *args: divmod(self.__eval(*args), other.__eval(*args)))

	@__unevaluate_arguments
	def __pow__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) ** other.__eval(*args))

	@__unevaluate_arguments
	def __lshift__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) << other.__eval(*args))

	@__unevaluate_arguments
	def __rshift__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) >> other.__eval(*args))

	@__unevaluate_arguments
	def __and__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) & other.__eval(*args))

	@__unevaluate_arguments
	def __or__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) | other.__eval(*args))

	@__unevaluate_arguments
	def __xor__(self, other):
		return UnevaluatedProxy(lambda *args: self.__eval(*args) ^ other.__eval(*args))

	@__unevaluate_arguments
	def __radd__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) + self.__eval(*args))

	@__unevaluate_arguments
	def __rsub__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) - self.__eval(*args))

	@__unevaluate_arguments
	def __rmul__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) * self.__eval(*args))

	@__unevaluate_arguments
	def __rfloordiv__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) // self.__eval(*args))

	@__unevaluate_arguments
	def __rdiv__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) / self.__eval(*args))

	@__unevaluate_arguments
	def __rmod__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) % self.__eval(*args))

	@__unevaluate_arguments
	def __rdivmod__(self, other):
		return UnevaluatedProxy(lambda *args: divmod(other.__eval(*args), self.__eval(*args)))

	@__unevaluate_arguments
	def __rpow__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) ** self.__eval(*args))

	@__unevaluate_arguments
	def __rlshift__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) << self.__eval(*args))

	@__unevaluate_arguments
	def __rrshift__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) >> self.__eval(*args))

	@__unevaluate_arguments
	def __rand__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) & self.__eval(*args))

	@__unevaluate_arguments
	def __ror__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) | self.__eval(*args))

	@__unevaluate_arguments
	def __rxor__(self, other):
		return UnevaluatedProxy(lambda *args: other.__eval(*args) ^ self.__eval(*args))

	@__unevaluate_arguments
	def __str__(self):
		return UnevaluatedProxy(lambda *args: str(self.__eval(*args)))

	@__unevaluate_arguments
	def __repr__(self):
		return UnevaluatedProxy(lambda *args: repr(self.__eval(*args)))

	@__unevaluate_arguments
	def __unicode__(self):
		return UnevaluatedProxy(lambda *args: unicode(self.__eval(*args)))

	@__unevaluate_arguments
	def __format__(self, formatstr):
		return UnevaluatedProxy(lambda *args: format(self.__eval(*args), formatstr.__eval(*args)))

	@__unevaluate_arguments
	def __hash__(self):
		return UnevaluatedProxy(lambda *args: hash(self.__eval(*args)))

	@__unevaluate_arguments
	def __nonzero__(self):
		return UnevaluatedProxy(lambda *args: not not self.__eval(*args))

	@__unevaluate_arguments
	def __dir__(self):
		return UnevaluatedProxy(lambda *args: dir(self.__eval(*args)))

	@__unevaluate_arguments
	def __sizeof__(self):
		return UnevaluatedProxy(lambda *args: sys.getsizeof(self.__eval(*args)))

	@__unevaluate_arguments
	def __getattr__(self, attr):
		return UnevaluatedProxy(lambda *args: getattr(self.__eval(*args), attr.__eval(*args)))

	@__unevaluate_arguments
	def __len__(self):
		return UnevaluatedProxy(lambda *args: len(self.__eval(*args)))

	@__unevaluate_arguments
	def __getitem__(self, key):
		return UnevaluatedProxy(lambda *args: self.__eval(*args)[key.__eval(*args)])

	@__unevaluate_arguments
	def __iter__(self):
		return UnevaluatedProxy(lambda *args: iter(self.__eval(*args)))

	@__unevaluate_arguments
	def __reversed__(self):
		return UnevaluatedProxy(lambda *args: reversed(self.__eval(*args)))

	@__unevaluate_arguments
	def __contains__(self, item):
		return UnevaluatedProxy(lambda *args: item.__eval(*args) in self.__eval(*args))

	@__unevaluate_arguments
	def __missing__(self, key):
		return UnevaluatedProxy(lambda *args: self.__eval(*args)[key.__eval(*args)])

	@__unevaluate_arguments
	def __instancecheck__(self, instance):
		return UnevaluatedProxy(lambda *args: isinstance(instance.__eval(*args), self.__eval(*args)[key]))

	@__unevaluate_arguments
	def __subclasscheck__(self, subclass):
		return UnevaluatedProxy(lambda *args: issubclass(subclass.__eval(*args), self.__eval(*args)[key]))

	@__unevaluate_arguments
	def __copy__(self):
		return UnevaluatedProxy(lambda *args: copy.copy(self.__eval(*args)))

	@__unevaluate_arguments
	def __deepcopy__(self, memodict={}):
		return UnevaluatedProxy(lambda *args: copy.deepcopy(self.__eval(*args), memodict.__eval(*args)))

for i in range(10):
	__builtins__[f"_{i}"] = UnevaluatedProxy(lambda *args, i = i: args[i])
