from ctypes import *

#load the module file
myModule = CDLL('./Sample.so') #link to C program
echo = myModule.echo       # function call
echo.restype = c_char_p    # c_char_p is a pointer to a string


input1 = "hello world!"
constrcter = c_char_p() # char pointer constrcter
constrcter.value = bytes(input1, 'utf-8') #string to byte
return_str = echo(constrcter).decode("utf-8") #byte to string

print(return_str)
