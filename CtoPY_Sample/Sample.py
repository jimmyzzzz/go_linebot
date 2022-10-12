
import ctypes


clib = ctypes.CDLL('./test.so')

clib.echo.restype = ctypes.c_char_p
clib.echo.argtypes = [ctypes.c_char_p]

input_str = "hello!"
return_str = clib.echo(bytes(input_str, 'utf-8'))
return_str = return_str.decode("utf-8")
print(return_str)