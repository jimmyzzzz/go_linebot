
import ctypes

class ROOT:
	def __init__(self, path):
		self.clib = ctypes.CDLL(path)

	def echo(self, input_str):
		self.clib.echo.restype = ctypes.c_char_p
		self.clib.echo.argtypes = [ctypes.c_char_p]

		return_str = self.clib.echo(bytes(input_str, 'utf-8'))
		return return_str.decode("utf-8")

	def fn_call(self, fn_name, input_str):
		fn = getattr(self.clib, fn_name)
		fn.restype = ctypes.c_char_p
		fn.argtypes = [ctypes.c_char_p]

		return_str = fn(bytes(input_str, 'utf-8'))
		return return_str.decode("utf-8")

path = './test.so'
root = ROOT(path)

for i in range(20):
	print(i, root.echo("hello!"))
	print(i, root.fn_call("echo", "world!"))