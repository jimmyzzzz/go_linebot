
import traceback
from ctypes import CDLL
from ctypes import c_char_p
import os


class sample_c_root_wapper:

    def __init__(self, root_name, root_path):
        self.root_name = root_name
        self.so_module = CDLL(os.path.join(root_path, f"{root_name}.so"))
        print(os.path.join(root_path, f"{root_name}.so"))
        print(self.so_module)

    def run(self, user_id, root_cmd, user_cmds):
        
        so_fn = getattr(self.so_module, "echo")
        so_fn.restype = c_char_p
        constrcter = c_char_p() # char pointer constrcter
        constrcter.value = bytes(user_cmds, 'utf-8') #string to byte
        return_str1 = so_fn(constrcter).decode("utf-8") #byte to string
        
        so_fn = getattr(self.so_module, "root_return")
        so_fn.restype = c_char_p
        constrcter = c_char_p() # char pointer constrcter
        constrcter.value = bytes(user_cmds, 'utf-8') #string to byte
        return_str2 = so_fn(constrcter).decode("utf-8") #byte to string
        
        # success, return_info = self.so_fn_call("get_user_id", user_id)
        # success, return_info = self.so_fn_call("get_root_cmd", root_cmd)
        # success, return_info = self.so_fn_call("get_user_id", user_cmds)
        # success, return_info = self.so_fn_call("root_return", " ")
        return return_str1, return_str2
    
#     def run(self, user_id, root_cmd, user_cmds):

#         run_order = [
#             ("get_user_id", user_id),
#             ("get_root_cmd", root_cmd),
#             ("get_user_cmds", user_cmds)
#         ]
#         for fn_name, input_str in run_order:
#             success, return_info = self.so_fn_call(fn_name, input_str)
#             print(success, return_info)
#             if success: continue
#             if fn_name in {"get_user_id", "get_root_cmd", "get_user_cmds"}:
#                 continue
#             return f"ERROR[{self.root_name}]: {fn_name} not find"
        
#         success, return_info = self.so_fn_call("root_return", " ")
#         return return_info

#     def so_fn_call(self, fn_name, input_str):
#         try:
#             so_fn = getattr(self.so_module, fn_name)
#         except AttributeError as error:
#             success = False
#             return (success, error)

#         success = True
#         so_fn.restype = c_char_p
#         constrcter = c_char_p() # char pointer constrcter
#         constrcter.value = bytes(input_str, 'utf-8') #string to byte
#         return_str = so_fn(constrcter).decode("utf-8") #byte to string
#         return (success, return_str)

class c_root_wapper:
    pass 