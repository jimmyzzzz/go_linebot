from ctypes import CDLL
from ctypes import c_char_p

def return_str(c_module, fn_name, input_str):
	c_fn = getattr(c_module, fn_name)
	c_fn.restype = c_char_p
	constrcter = c_char_p()
	constrcter.value = bytes(input_str, 'utf-8')
	return c_fn(constrcter).decode("utf-8")

#load the module file
myModule = CDLL('./Sample.so') #link to C program

for i,fn_name in enumerate(["echo", "root_return"]*100):
	print(i, return_str(
		myModule, fn_name, "hahaha"
	))

# for i in range(100):
# 	echo = getattr(myModule, "root_return") # function call
# 	echo.restype = c_char_p    # c_char_p is a pointer to a string

# 	input1 = "hello world!"
# 	constrcter = c_char_p() # char pointer constrcter
# 	constrcter.value = bytes(input1, 'utf-8') #string to byte
# 	return_str = echo(constrcter).decode("utf-8") #byte to string
# 	print(i, [return_str])

