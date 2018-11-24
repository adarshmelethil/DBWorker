
def t(f):
	def ff(*a, **ka):
		f(*a, **ka)
		print("here", a[0].aa)
	print()
	return ff 

class a:
	aa = 123
	
	@t
	def tt(self, v, w=1):
		print("v={}, w={}".format(v,w))

aobj = a()

aobj.tt(345)