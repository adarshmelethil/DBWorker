class Mapping():
	def __setitem__(self, key, item):
		print("__setitem__", key, item)
		self.__dict__[key] = item

	def __getitem__(self, key):
		print("__getitem__", key)
		return self.__dict__[key]

	def __repr__(self):
		print("__repr__")
		return repr(self.__dict__)

	def __len__(self):
		print("__len__")
		return len(self.__dict__)

	def __delitem__(self, key):
		print("__delitem__")
		del self.__dict__[key]

	def clear(self):
		print("clear")
		return self.__dict__.clear()

	def copy(self):
		print("copy")
		return self.__dict__.copy()

	def has_key(self, k):
		print("has_key")
		return k in self.__dict__

	def update(self, *args, **kwargs):
		print("update")
		return self.__dict__.update(*args, **kwargs)

	def keys(self):
		print("keys")
		return self.__dict__.keys()

	def values(self):
		print("values")
		return self.__dict__.values()

	def items(self):
		print("items")
		return self.__dict__.items()

	def pop(self, *args):
		print("pop")
		return self.__dict__.pop(*args)

	def __cmp__(self, dict_):
		print("__cmp__")
		return self.__cmp__(self.__dict__, dict_)

	def __contains__(self, item):
		print("__contains__")
		return item in self.__dict__

	def __iter__(self):
		print("__iter__")
		return iter(self.__dict__)

	def __unicode__(self):
		print("__unicode__")
		return unicode(repr(self.__dict__))


a = Mapping()
a["a"] = "A"

print("a" in a)